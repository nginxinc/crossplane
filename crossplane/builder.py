# -*- coding: utf-8 -*-
import codecs
import os

from .lexer import lex
from .analyzer import analyze, enter_block_ctx
from .errors import NgxParserDirectiveError
from .compat import PY2, json

DELIMITERS = ('{', '}', ';')


def _escape(string):
    prev, char = '', ''
    for char in string:
        if prev == '\\' or prev + char == '${':
            prev += char
            yield prev
            continue
        if prev == '$':
            yield prev
        if char not in ('\\', '$'):
            yield char
        prev = char
    if char in ('\\', '$'):
        yield char


def _needs_quotes(string):
    if string == '':
        return True
    elif string in DELIMITERS:
        return False

    # lexer should throw an error when variable expansion syntax
    # is messed up, but just wrap it in quotes for now I guess
    chars = _escape(string)

    # arguments can't start with variable expansion syntax
    char = next(chars)
    if char.isspace() or char in ('{', ';', '"', "'", '${'):
        return True

    expanding = False
    for char in chars:
        if char.isspace() or char in ('{', ';', '"', "'"):
            return True
        elif char == ('${' if expanding else '}'):
            return True
        elif char == ('}' if expanding else '${'):
            expanding = not expanding

    return char in ('\\', '$') or expanding


def _enquote(arg):
    if _needs_quotes(arg):
        arg = repr(codecs.decode(arg, 'raw_unicode_escape'))
        arg = arg.replace('\\\\', '\\').lstrip('u')
    return arg


def build(payload, indent=4, tabs=False):
    padding = '\t' if tabs else ' ' * indent

    def _build_lines(objs, depth):
        margin = padding * depth

        for obj in objs:
            directive = obj['directive']
            args = [_enquote(arg) for arg in obj['args']]

            if directive == 'if':
                line = 'if (' + ' '.join(args) + ')'
            elif args:
                line = directive + ' ' + ' '.join(args)
            else:
                line = directive

            if obj.get('block') is None:
                yield margin + line + ';'
            else:
                yield margin + line + ' {'
                for line in _build_lines(obj['block'], depth+1):
                    yield line
                yield margin + '}'

    lines = _build_lines(payload, depth=0)
    return '\n'.join(lines)
