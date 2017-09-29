# -*- coding: utf-8 -*-
import sys
import contextlib
from io import open

try:
    import simplejson as json
except ImportError:
    import json

PY2 = (sys.version_info[0] == 2)
PY3 = (sys.version_info[0] == 3)

if PY2:
    from cStringIO import StringIO
elif PY3:
    from io import StringIO


def open_file(filename, mode='r'):
    return open(filename, mode=mode, encoding='utf-8')


def open_string(string):
    if PY2:
        string = unicode(string).encode('utf-8')
    return contextlib.closing(StringIO(string))
