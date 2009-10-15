# -*- coding: utf-8 -*-

from zope.schema import TextLine
from zope.interface import implements
from zope.contenttype import guess_content_type
from zope.app.file import File
from zope.app.file.interfaces import IFile


def cleanupFileName(filename):
    return filename.split('\\')[-1].split('/')[-1]


class INamedFile(IFile):
    """Defines a file that is aware of its filename.
    """
    filename = TextLine(
        title = u"Name of file",
        required = True
        )

class NamedFile(File):
    """A simple INamedFile implementation that can guess the content type
    from the value and the filename.
    """
    implements(INamedFile)
    filename = u"attached file"
    
    def __init__(self, data='', contentType='', filename=u''):
        self.data = data
        self.filename = cleanupFileName(filename)
        if not contentType and filename:
            # If we handle large files, we don't want them read just
            # to guess the content type. We provide only the filename.
            self.contentType = guess_content_type(name=filename)
        else:
            self.contentType = contentType
