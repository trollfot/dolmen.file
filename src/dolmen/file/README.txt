===========
dolmen.file
===========

``dolmen.file`` is a layer above ``zope.app.file.file.File``, adding a
notion of filename, missing in the original implementation.


Compatibility
=============

In order to make sure that our `File` implementation is complete and
functional, we test it against the original functionalities of the
`zope.app.file` version::

    >>> from zope.app.file.file import FileChunk
    >>> from zope.app.file.interfaces import IFile
    >>> from dolmen.file import NamedFile, INamedFile

Let's test the constructor::

    >>> file = NamedFile()
    >>> file.contentType
    ''
    >>> file.data
    ''

    >>> file = NamedFile('Foobar')
    >>> file.contentType
    ''
    >>> file.data
    'Foobar'

    >>> file = NamedFile('Foobar', 'text/plain')
    >>> file.contentType
    'text/plain'
    >>> file.data
    'Foobar'

    >>> file = NamedFile(data='Foobar', contentType='text/plain')
    >>> file.contentType
    'text/plain'
    >>> file.data
    'Foobar'

Let's test the mutators::

    >>> file = NamedFile()
    >>> file.contentType = 'text/plain'
    >>> file.contentType
    'text/plain'

    >>> file.data = 'Foobar'
    >>> file.data
    'Foobar'

    >>> file.data = None
    Traceback (most recent call last):
    ...
    TypeError: Cannot set None data on a file.


Let's test large data input::

    >>> file = NamedFile()

    Insert as string:

    >>> file.data = 'Foobar'*60000
    >>> file.getSize()
    360000
    >>> file.data == 'Foobar'*60000
    True

Insert data as FileChunk::

    >>> fc = FileChunk('Foobar'*4000)
    >>> file.data = fc
    >>> file.getSize()
    24000
    >>> file.data == 'Foobar'*4000
    True

Insert data from file object::

    >>> import cStringIO
    >>> sio = cStringIO.StringIO()
    >>> sio.write('Foobar'*100000)
    >>> sio.seek(0)
    >>> file.data = sio
    >>> file.getSize()
    600000
    >>> file.data == 'Foobar'*100000
    True

Last, but not least, verify the two interfaces::

    >>> from zope.interface.verify import verifyClass
    >>> INamedFile.extends(IFile)
    True
    >>> INamedFile.implementedBy(NamedFile)
    True
    >>> verifyClass(INamedFile, NamedFile)
    True


Naming
======

When no name is provided, the fallback is a simple empty unicode
string::

    >>> file = NamedFile('Foobar')
    >>> file.contentType
    ''
    >>> file.data
    'Foobar'
    >>> file.filename
    u''

To specifiy a filename, we can give it to the constructor::
    
    >>> file = NamedFile('Foobar', filename='foobar.txt')
    >>> file.data
    'Foobar'
    >>> file.filename
    u'foobar.txt'

The filename can be both unicode or simple string::

    >>> file = NamedFile('Foobar', filename=u'foobar.txt')
    >>> file.data
    'Foobar'
    >>> file.filename
    u'foobar.txt'

The filename provided had an extension : 'txt'. This extension is used
by the NamedFile, while instanciated, to try and guess the mimetype of
the data::

    >>> file.contentType
    'text/plain'

    The filename can be set later, but this won't trigger the mime
    type guess::
    
    >>> file.filename = u"something.zip"
    >>> file.filename
    u'something.zip'
    >>> file.contentType
    'text/plain'


Access
======

In order to access our file, ``dolmen.file`` provides a view called
`file_publish` that sets the proper headers and returns the
data. Let's set up a simple environment to test that behavior::

    >>> from zope.component import getMultiAdapter
    >>> from zope.publisher.browser import TestRequest

    >>> root = getRootFolder()
    >>> root['myfile'] = NamedFile('Foobar', filename='foobar.txt')
    >>> myfile = root['myfile']

    The `file_publish` view will adapt a IFile and a request and, when
    called, will return the data.

    >>> request = TestRequest()
    >>> view = getMultiAdapter((myfile, request), name='file_publish')
    >>> view
    <dolmen.file.access.FilePublisher object at ...>


In the update of the view, the headers are set properly, using the
info of the file::

    >>> view.update()
    >>> for key, value in view.response.getHeaders(): print key, repr(value)
    X-Powered-By 'Zope (www.zope.org), Python (www.python.org)'
    Content-Length '6'
    Content-Type 'text/plain'
    Content-Disposition 'attachment; filename="foobar.txt"'
    >>> view.render()
    'Foobar'


Field, download and security
============================

In a site, the file object is rarely accessed directly. Often, it's
just a part of a more complex object. For that matter, we have three
dedicated components: the field, the property and the traverser.


Field and Property
------------------

A self-explanatory exemple::

    >>> from persistent import Persistent
    >>> from dolmen.file import FileProperty, FileField
    >>> from zope.interface import Interface, implements

    >>> class IContent(Interface):
    ...     binary = FileField(title=u"Binary data")

    >>> class MyContent(Persistent):
    ...     implements(IContent)
    ...     binary = FileProperty(IContent['binary'])

    >>> root['mammoth'] = MyContent()
    >>> manfred = root['mammoth']
    >>> manfred.binary = FileChunk('Foobar')
    >>> manfred.binary
    <dolmen.file.file.NamedFile object at ...>

    >>> manfred.binary.data
    'Foobar'

There are two fields provided by `dolmen.file`: the FileField and the
ImageField. They are just logical separation but have a common base::  

    >>> from dolmen.file import IImageField, IFileField, ImageField
    >>> IImageField.extends(IFileField)
    True
    >>> isinstance(ImageField(), FileField)
    True


Traversal
---------

The traverser will take care of both the fetching and the security
checking, while accessing your data. The basic permission used to
check the availability of the data, is `zope.View`.

Here, we set up two principals to test this. 'jason' is a logged in
member with no rights while 'judith' has the `zope.View` permission
granted::

    >>> import zope.security.management as security  
    >>> from zope.traversing.interfaces import ITraversable
    >>> from zope.security.testing import Principal, Participation

    >>> judith = Principal('zope.judith', 'Judith')
    >>> jason = Principal('zope.jason', 'Jason')

We create the interaction and try to traverse to our binary data::

    >>> security.newInteraction(Participation(jason))
    >>> traverser = getMultiAdapter(
    ...              (manfred, request), ITraversable, 'download')
    >>> traverser
    <dolmen.file.access.DownloadTraverser object at ...>
    >>> traverser.traverse('binary')
    Traceback (most recent call last):
    ...
    Unauthorized: binary
    >>> security.endInteraction()

It fails. An Unauthorized Error is raised. We now try with Judith::

    >>> security.newInteraction(Participation(judith))
    >>> traverser.traverse('binary')
    <dolmen.file.access.FilePublisher object at ...>

Our data is returned, wrapped in a `FilePublisher` view, ready to be
rendered (see the Access section, for more information).

What if we traverse to an unknown field ? Let's try::

    >>> traverser.traverse('zorglub')
    Traceback (most recent call last):
    ...
    NotFound: Object: <MyContent object at ...>, name: 'zorglub'


Everything is fine : a NotFound error has been raised. If we try to
access a file that is not an IFile, we get another error::

    >>> traverser.traverse('__name__')
    Traceback (most recent call last):
    ...
    LocationError: '__name__ is not a valid IFile'

We gracefully end our tests::

    >>> security.endInteraction()

Enjoy !
