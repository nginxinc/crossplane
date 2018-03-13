# -*- coding: utf-8 -*-
import codecs
import os

from .lexer import lex
from .analyzer import analyze, enter_block_ctx
from .errors import NgxParserDirectiveError
from .compat import PY2, json

DELIMITERS = ('{', '}', ';')
EXTERNAL_BUILDERS = {}

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
    state = {
        'prev_obj': None,
        'depth': -1
    }

    def _put_line(line, obj):
        margin = padding * state['depth']

        # don't need put \n on first line and after comment
        if state['prev_obj'] is None:
            return margin + line

        # trailing comments have to be without \n
        if obj['directive'] == '#' and obj['line'] == state['prev_obj']['line']:
            return ' ' + line

        return '\n' + margin + line

    def _build_lines(objs):
        state['depth'] = state['depth'] + 1

        for obj in objs:
            directive = obj['directive']

            if directive in EXTERNAL_BUILDERS:
                external_builder = EXTERNAL_BUILDERS[directive]
                built = external_builder(obj, padding, state, indent, tabs)
                yield _put_line(built, obj)
                continue

            if directive == '#':
                yield _put_line('#' + obj['comment'], obj)
                continue

            args = [_enquote(arg) for arg in obj['args']]

            if directive == 'if':
                line = 'if (' + ' '.join(args) + ')'
            elif args:
                line = directive + ' ' + ' '.join(args)
            else:
                line = directive

            if obj.get('block') is None:
                yield _put_line(line + ';', obj)
            else:
                yield _put_line(line + ' {', obj)

                # set prev_obj to propper indentation in block
                state['prev_obj'] = obj
                for line in _build_lines(obj['block']):
                    yield line
                yield _put_line('}', obj)

            state['prev_obj'] = obj
        state['depth'] = state['depth'] - 1

    lines = _build_lines(payload)
    return ''.join(lines)


def register_external_builder(builder, directives):
    for directive in directives:
        EXTERNAL_BUILDERS[directive] = builder
