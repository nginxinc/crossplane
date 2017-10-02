#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys
import traceback

from nginx_conf.parse import parse_file


def tb_onerror(e):
    cls, exc, tb = sys.exc_info()
    try:
        return traceback.format_exception(cls, exc, tb, 10)
    finally:
        del cls, exc, tb


def parse_args():
    from argparse import ArgumentParser

    # create parser and parse arguments
    parser = ArgumentParser(description='Print the new style config parser payload for a given nginx config')
    parser.add_argument('filename')
    parser.add_argument('--no-catch', action='store_false', dest='catch', help='only collect first error in file')
    parser.add_argument('--tb-onerror', action='store_true', help='include tracebacks in config errors')
    parser.add_argument('-i', '--indent', type=int, metavar='num', help='number of spaces to indent output')
    args = parser.parse_args()

    # prepare filename argument
    args.filename = os.path.expanduser(args.filename)
    args.filename = os.path.abspath(args.filename)
    if not os.path.isfile(args.filename):
        parser.error('filename: No such file or directory')

    return args


def main():
    args = parse_args()

    kwargs = {'catch_errors': args.catch}
    if args.use_onerror:
        kwargs['onerror'] = tb_onerror

    payload = parse_file(args.filename, **kwargs)

    # use no-space separators if not indenting for a dense json dump
    separators = (',', ':') if args.indent is None else (', ', ': ')

    print json.dumps(payload, indent=args.indent, separators=separators, sort_keys=True)

if __name__ == '__main__':
    main()
