# -*- coding: utf-8 -*-

import grok
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.app.file.interfaces import IFile
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.http import IHTTPRequest
from zope.security.interfaces import Unauthorized
from zope.security.management import checkPermission


class FilePublisher(grok.View):
    grok.name('file_publish')
    grok.context(IFile)

    def render(self):
        if getattr(self.context, "filename", None):
            self.response.setHeader(
                'Content-Disposition',
                'attachment; filename="%s"' % self.context.filename.encode('utf-8')
                )
        self.response.setHeader('Content-Type', self.context.contentType[0])
        self.response.setHeader('Content-Length', self.context.getSize())
        return self.context.data


class FileTraverser(grok.MultiAdapter):
    grok.baseclass()
    grok.provides(ITraversable)
    
    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        self.response = request.response

    def get_file(self):
        raise NotImplementedError("Provide your own get_file method")

    def traverse(self, name, ignore):
        obj = self.get_file(name)
        if file is not None:
            return getMultiAdapter((obj, self.request), name='file_publish')
        raise NotFound(self.context, name, self.request)


class DownloadTraverser(FileTraverser):
    grok.name('download')
    grok.adapts(Interface, IHTTPRequest)

    def get_file(self, name):
        if not checkPermission('zope.View', self.context):
            raise Unauthorized(name)
        return getattr(self.context, name, None)
