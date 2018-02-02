#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from argparse import ArgumentParser, FileType, RawDescriptionHelpFormatter
from traceback import format_exception

from . import __version__
from .lexer import lex as lex_file
from .parser import parse as parse_file
from .builder import build as build_file, _enquote, DELIMITERS
from .errors import NgxParserBaseException
from .compat import PY2, json, input


def _prompt_yes():
    try:
        return input('overwrite? (y/n [n]) ').lower().startswith('y')
    except (KeyboardInterrupt, EOFError):
        sys.exit(1)


def _dump_payload(obj, fp, indent):
    kwargs = {'indent': indent}
    if indent is None:
        kwargs['separators'] = ',', ':'
    fp.write(json.dumps(obj, **kwargs) + '\n')


def parse(filename, out, indent=None, catch=None, tb_onerror=None, ignore='', single=False, comments=False):
    ignore = ignore.split(',') if ignore else []

    def callback(e):
        exc = sys.exc_info() + (10,)
        return ''.join(format_exception(*exc)).rstrip()

    kwargs = {'catch_errors': catch, 'ignore': ignore, 'single': single, 'comments': comments}
    if tb_onerror:
        kwargs['onerror'] = callback

    payload = parse_file(filename, **kwargs)
    _dump_payload(payload, out, indent=indent)


def build(filename, dirname, force, indent, tabs, header, stdout, verbose):
    with open(filename, 'r') as fp:
        payload = json.load(fp)

    if dirname is None:
        dirname = os.getcwd()

    existing = []
    dirs_to_make = []

    # find which files from the json payload will overwrite existing files and
    # which directories need to be created in order for the config to be built
    for config in payload['config']:
        path = config['file']
        if not os.path.isabs(path):
            path = os.path.join(dirname, path)
        dirpath = os.path.dirname(path)
        if os.path.exists(path):
            existing.append(path)
        elif not os.path.exists(dirpath) and dirpath not in dirs_to_make:
            dirs_to_make.append(dirpath)

    # ask the user if it's okay to overwrite existing files
    if existing and not force and not stdout:
        print('building {} would overwrite these files:'.format(filename))
        print('\n'.join(existing))
        if not _prompt_yes():
            print('not overwritten')
            return

    # make directories necessary for the config to be built
    for dirpath in dirs_to_make:
        os.makedirs(dirpath)

    # build the nginx configuration file from the json payload
    for config in payload['config']:
        path = os.path.join(dirname, config['file'])

        if header:
            output = (
                '# This config was built from JSON using NGINX crossplane.\n'
                '# If you encounter any bugs please report them here:\n'
                '# https://github.com/nginxinc/crossplane/issues\n'
                '\n'
            )
        else:
            output = ''

        parsed = config['parsed']
        output += build_file(parsed, indent, tabs) + '\n'

        if stdout:
            print('# ' + path + '\n' + output)
        else:
            with open(path, 'w') as fp:
                fp.write(output)
            if verbose:
                print('wrote to ' + path)


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
    payload = parse_file(filename)
    parsed = payload['config'][0]['parsed']
    if payload['status'] == 'ok':
        output = build_file(parsed, indent, tabs) + '\n'
        out.write(output)
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
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)
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
    p.add_argument('--ignore', metavar='DIRECTIVES', default='', help='ignore directives (comma-separated)')
    p.add_argument('--no-catch', action='store_false', dest='catch', help='only collect first error in file')
    p.add_argument('--tb-onerror', action='store_true', help='include tracebacks in config errors')
    p.add_argument('--single-file', action='store_true', dest='single', help='do not include other config files')
    p.add_argument('--include-comments', action='store_true', dest='comments', help='include comments in json')

    p = create_subparser(build, 'builds an nginx config from a json payload')
    p.add_argument('filename', help='the file with the config payload')
    p.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    p.add_argument('-d', '--dir', metavar='PATH', default=None, dest='dirname', help='the base directory to build in')
    p.add_argument('-f', '--force', action='store_true', help='overwrite existing files')
    g = p.add_mutually_exclusive_group()
    g.add_argument('-i', '--indent', type=int, metavar='NUM', help='number of spaces to indent output', default=4)
    g.add_argument('-t', '--tabs', action='store_true', help='indent with tabs instead of spaces')
    p.add_argument('--no-headers', action='store_false', dest='header', help='do not write header to configs')
    p.add_argument('--stdout', action='store_true', help='write configs to stdout instead')

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
        if command not in parser._actions[-1].choices:
            parser.error('unknown command %r' % command)
        else:
            parser._actions[-1].choices[command].print_help()

    p = create_subparser(help, 'show help for commands')
    p.add_argument('command', help='command to show help for')

    parsed = parser.parse_args(args=args)

    # this addresses a bug that was added to argparse in Python 3.3
    if not parsed.__dict__:
        parser.error('too few arguments')

    return parsed


def main():
    kwargs = parse_args().__dict__
    func = kwargs.pop('_subcommand')
    func(**kwargs)


if __name__ == '__main__':
    main()
