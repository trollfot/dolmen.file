# -*- coding: utf-8 -*-

import grok
from zope.size import byteDisplay
from zope.app.form import browser
from zope.component import getMultiAdapter
from zope.cachedescriptors.property import Lazy
from zope.app.form.browser import widget, DisplayWidget
from zope.traversing.browser.absoluteurl import absoluteURL

_marker = object()


class FileWidgetMixin(object):

    def url(self):
        url = absoluteURL(self.context.context, self.request)
        return '%s/++download++%s' % (url, self.context.__name__)

    def namespace(self):
        return {}

    def default_namespace(self):
        namespace = {}
        namespace['request'] = self.request
        namespace['view'] = self
        namespace['file'] = None
        namespace['field'] = dict(
            name = self.name,
            required = self.context.required,
            cooked_name = '%s:int' % getattr(self, "_modified_name", u"")
            )

        if self._data and self._data is not self._data_marker:
            namespace['file'] = dict(
                name = self._data.filename,
                url = self.url(),
                size = byteDisplay(self._data.getSize())
                )
        return namespace


class FileDownloadWidget(FileWidgetMixin, DisplayWidget):
    """Widget capable of downloading file.
    """
    def __call__(self):
        return grok.PageTemplateFile('templates/display.pt').render(self)
    

class FileUploadWidget(FileWidgetMixin, widget.SimpleInputWidget):
    """This widget renders a file upload widget. It also allows you to
    delete, keep or override the current uploaded file.
    """
    def __call__(self):
        if not self._data or self._data is self._data_marker:
            return grok.PageTemplateFile('templates/add.pt').render(self)
        return grok.PageTemplateFile('templates/edit.pt').render(self)

    def _getFormInput(self):
        if not self.chosen_option:
            return None
        return self.request.get(self.name, None) or None

    def hasInput(self):
        return bool(self.chosen_option)

    @Lazy
    def chosen_option(self):
        return int(self.request.get(self._modified_name, 0))

    @Lazy
    def _modified_name(self):
        return "_modify_%s" % self.name
