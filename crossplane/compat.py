# -*- coding: utf-8 -*-
import typing as t
import functools
import sys

try:
    import simplejson as json
except ImportError:
    import json  # type: ignore[no-redef]

PY2 = (sys.version_info[0] == 2)
PY3 = (sys.version_info[0] == 3)

if PY2:
    input = raw_input
    basestring = basestring
else:
    input = input
    basestring = str


def fix_pep_479(generator: t.Any) -> t.Any:
    """
    Python 3.7 breaks crossplane's lexer because of PEP 479
    Read more here: https://www.python.org/dev/peps/pep-0479/
    """
    @functools.wraps(generator)
    def _wrapped_generator(*args: t.Any, **kwargs: t.Any) -> t.Generator[t.Any, None, None]:
        try:
            for x in generator(*args, **kwargs):
                yield x
        except RuntimeError:
            return

    return _wrapped_generator

__all__ = ['PY2', 'PY3', 'input', 'basestring', 'fix_pep_479', 'json']
