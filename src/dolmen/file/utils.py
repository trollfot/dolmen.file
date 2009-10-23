# -*- coding: utf-8 -*-

import re

_nameFinder = re.compile(r'(.*[\\/:])?(.+)')

def clean_filename(name):
    match = _nameFinder.match(name)
    if match is not None:
        match = match.group(2)
    return unicode(match, 'utf-8')
