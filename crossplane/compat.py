# -*- coding: utf-8 -*-
import sys

try:
    import simplejson as json
except ImportError:
    import json

PY2 = (sys.version_info[0] == 2)
PY3 = (sys.version_info[0] == 3)

if PY2:
    input = raw_input
    basestring = basestring
else:
    input = input
    basestring = str
