# -*- coding: utf-8 -*-

from dolmen.file import NamedFile


_marker = object()

class FileProperty(object):
    """Stores the given file data in a NamedFile
    """
    def __init__(self, field, name=None):
        if name is None:
            name = field.__name__

        self.__field = field
        self.__name = name

    def __set__(self, inst, value):
        name = self.__name
        field = self.__field.bind(inst)
        fields = inst.__dict__
        
        if field.readonly and field.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')

        if value is not None:
            filename = getattr(value, 'filename', None)
            file = NamedFile(data=value, filename=filename)
        else:
            file = None
            
        fields[name] = file
        inst._p_changed = True

    def __get__(self, inst, klass):
        if inst is None:
            return self

        value = inst.__dict__.get(self.__name, _marker)
        if value is _marker:
            field = self.__field.bind(inst)
            value = getattr(field, 'default', _marker)
            if value is _marker:
                raise AttributeError(self.__name)
        return value

    def __getattr__(self, name):
        return getattr(self.__field, name)
