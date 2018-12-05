# -*- coding: utf-8 -*-
import codecs
import os
import re

from .compat import PY2

DELIMITERS = ('{', '}', ';')
EXTERNAL_BUILDERS = {}
ESCAPE_SEQUENCES_RE = re.compile(r'(\\x[0-9a-f]{2}|\\[0-7]{1,3})')


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

    # lexer should throw an error when variable expansion syntax
    # is messed up, but just wrap it in quotes for now I guess
    chars = _escape(string)

    # arguments can't start with variable expansion syntax
    char = next(chars)
    if char.isspace() or char in ('{', '}', ';', '"', "'", '${'):
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


def _replace_escape_sequences(match):
    return match.group(1).decode('string-escape')


def _enquote(arg):
    if not _needs_quotes(arg):
        return arg

    if PY2:
        arg = codecs.encode(arg, 'utf-8') if isinstance(arg, unicode) else arg
        arg = codecs.decode(arg, 'raw-unicode-escape')
        arg = repr(arg).replace('\\\\', '\\').lstrip('u')
        arg = ESCAPE_SEQUENCES_RE.sub(_replace_escape_sequences, arg)
        arg = unicode(arg, 'utf-8')
    else:
        arg = codecs.decode(arg, 'unicode-internal')
        arg = repr(arg).replace('\\\\', '\\')

    return arg


def build(payload, indent=4, tabs=False, header=False):
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
            directive = _enquote(obj['directive'])

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

    if header:
        lines = [
            '# This config was built from JSON using NGINX crossplane.\n',
            '# If you encounter any bugs please report them here:\n',
            '# https://github.com/nginxinc/crossplane/issues\n',
            '\n'
        ]
    else:
        lines = []

    lines += _build_lines(payload)
    return ''.join(lines)


def build_files(payload, dirname=None, indent=4, tabs=False, header=False):
    """
    Uses a full nginx config payload (output of crossplane.parse) to build
    config files, then writes those files to disk.
    """
    if dirname is None:
        dirname = os.getcwd()

    for config in payload['config']:
        path = config['file']
        if not os.path.isabs(path):
            path = os.path.join(dirname, path)

        # make directories that need to be made for the config to be built
        dirpath = os.path.dirname(path)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        # build then create the nginx config file using the json payload
        parsed = config['parsed']
        output = build(parsed, indent=indent, tabs=tabs, header=header)
        output = output.rstrip() + '\n'
        with codecs.open(path, 'w', encoding='utf-8') as fp:
            fp.write(output)


def register_external_builder(builder, directives):
    for directive in directives:
        EXTERNAL_BUILDERS[directive] = builder
