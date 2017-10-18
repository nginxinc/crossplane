#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from argparse import ArgumentParser, FileType, RawDescriptionHelpFormatter
from traceback import format_exception

from .lexer import lex as lex_file
from .parser import parse as parse_file
from .errors import NgxParserBaseException
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
    arg = str(arg.encode('utf-8') if PY2 else arg)
    if _needs_quotes(arg):
        arg = repr(arg.decode('string_escape') if PY2 else arg)
    return arg


def _dump_payload(obj, fp, indent):
    kwargs = {'indent': indent}
    if indent is None:
        kwargs['separators'] = ',', ':'
    fp.write(json.dumps(obj, **kwargs) + '\n')


def parse(filename, out, indent=None, catch=None, tb_onerror=None):
    def callback(e):
        exc = sys.exc_info() + (10,)
        return ''.join(format_exception(*exc)).rstrip()

    kwargs = {'catch_errors': catch}
    if tb_onerror:
        kwargs['onerror'] = callback

    payload = parse_file(filename, **kwargs)
    _dump_payload(payload, out, indent=indent)


def lex(filename, out, indent=None, line_numbers=False):
    payload = list(lex_file(filename))
    if not line_numbers:
        payload = [token for token, lineno in payload]
    _dump_payload(payload, out, indent=indent)


def minify(filename, out):
    prev, token = '', ''
    for token, __ in lex_file(filename):
        token = _enquote(token)
        if prev and not (prev in DELIMITERS or token in DELIMITERS):
            token = ' ' + token
        out.write(token)
        prev = token
    out.write('\n')


def format(filename, out, indent=None, tabs=False):
    padding = '\t' if tabs else ' ' * indent

    def _format(objs, depth):
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
                for line in _format(obj['block'], depth=depth+1):
                    yield line
                yield margin + '}'

    payload = parse_file(filename)

    if payload['status'] == 'ok':
        config = payload['config'][0]['parsed']
        lines = _format(config, depth=0)
        out.write('\n'.join(lines) + '\n')
    else:
        e = payload['errors'][0]
        raise NgxParserBaseException(e['error'], e['file'], e['line'])


class _SubparserHelpFormatter(RawDescriptionHelpFormatter):
    def _format_action(self, action):
        line = super(RawDescriptionHelpFormatter, self)._format_action(action)

        if action.nargs == 'A...':
            line = line.split('\n', 1)[-1]

        if line.startswith('    ') and line[4] != ' ':
            parts = filter(len, line.lstrip().partition(' '))
            line = '  ' + ' '.join(parts)

        return line


def parse_args(args=None):
    parser = ArgumentParser(
        formatter_class=_SubparserHelpFormatter,
        description='various operations for nginx config files',
        usage='%(prog)s <command> [options]'
    )
    subparsers = parser.add_subparsers(title='commands')

    def create_subparser(function, help):
        name = function.__name__
        prog = 'crossplane ' + name
        p = subparsers.add_parser(name, prog=prog, help=help, description=help)
        p.set_defaults(_subcommand=function)
        return p

    p = create_subparser(parse, 'parses a json payload for an nginx config')
    p.add_argument('filename', help='the nginx config file')
    p.add_argument('-o', '--out', type=FileType('w'), default='-', help='write output to a file')
    p.add_argument('-i', '--indent', type=int, metavar='NUM', help='number of spaces to indent output')
    p.add_argument('--no-catch', action='store_false', dest='catch', help='only collect first error in file')
    p.add_argument('--tb-onerror', action='store_true', help='include tracebacks in config errors')

    p = create_subparser(lex, 'lexes tokens from an nginx config file')
    p.add_argument('filename', help='the nginx config file')
    p.add_argument('-o', '--out', type=FileType('w'), default='-', help='write output to a file')
    p.add_argument('-i', '--indent', type=int, metavar='NUM', help='number of spaces to indent output')
    p.add_argument('-n', '--line-numbers', action='store_true', help='include line numbers in json payload')

    p = create_subparser(minify, 'removes all whitespace from an nginx config')
    p.add_argument('filename', help='the nginx config file')
    p.add_argument('-o', '--out', type=FileType('w'), default='-', help='write output to a file')

    p = create_subparser(format, 'formats an nginx config file')
    p.add_argument('filename', help='the nginx config file')
    p.add_argument('-o', '--out', type=FileType('w'), default='-', help='write output to a file')
    g = p.add_mutually_exclusive_group()
    g.add_argument('-i', '--indent', type=int, metavar='NUM', help='number of spaces to indent output', default=4)
    g.add_argument('-t', '--tabs', action='store_true', help='indent with tabs instead of spaces')

    def help(command):
        if command not in parser._actions[1].choices:
            parser.error('unknown command %r' % command)
        else:
            parser._actions[1].choices[command].print_help()

    p = create_subparser(help, 'show help for commands')
    p.add_argument('command', help='command to show help for')

    parsed = parser.parse_args(args=args)

    # this addresses a bug  that was added to argparse in Python 3.3
    if not parsed.__dict__:
        parser.error('too few arguments')

    return parsed


def main():
    kwargs = parse_args().__dict__
    func = kwargs.pop('_subcommand')
    func(**kwargs)


if __name__ == '__main__':
    main()
