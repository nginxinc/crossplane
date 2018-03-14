# -*- coding: utf-8 -*-
import os

import crossplane
from . import here


def test_simple_config():
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')
    tokens = crossplane.lex(config)
    assert list(tokens) == [
        ('events', 1), ('{', 1), ('worker_connections', 2), ('1024', 2),
        (';', 2), ('}', 3), ('http', 5), ('{', 5), ('server', 6), ('{', 6),
        ('listen', 7), ('127.0.0.1:8080', 7), (';', 7), ('server_name', 8),
        ('default_server', 8), (';', 8), ('location', 9), ('/', 9), ('{', 9),
        ('return', 10), ('200', 10), ('foo bar baz', 10), (';', 10), ('}', 11),
        ('}', 12), ('}', 13)
    ]

def test_with_config_comments():
    dirname = os.path.join(here, 'configs', 'with-comments')
    config = os.path.join(dirname, 'nginx.conf')
    tokens = crossplane.lex(config)
    assert list(tokens) == [
        (u'events', 1), (u'{', 1), (u'worker_connections', 2), (u'1024', 2),
        (u';', 2), (u'}', 3),(u'#comment', 4), (u'http', 5), (u'{', 5),
        (u'server', 6), (u'{', 6), (u'listen', 7), (u'127.0.0.1:8080', 7),
        (u';', 7), (u'#listen', 7), (u'server_name', 8),
        (u'default_server', 8),(u';', 8), (u'location', 9), (u'/', 9),
        (u'{', 9), (u'## this is brace', 9), (u'# location /', 10), (u'return', 11), (u'200', 11),
        (u'foo bar baz', 11), (u';', 11), (u'}', 12), (u'}', 13), (u'}', 14)
    ]

def test_messy_config():
   dirname = os.path.join(here, 'configs', 'messy')
   config = os.path.join(dirname, 'nginx.conf')
   tokens = crossplane.lex(config)
   assert list(tokens) == [(u'user', 1), (u'nobody', 1), (u';', 1),
        (u'# hello\\n\\\\n\\\\\\n worlddd  \\#\\\\#\\\\\\# dfsf\\n \\\\n \\\\\\n ', 2),
        (u'events', 3), (u'{', 3), (u'worker_connections', 3), (u'2048', 3),
        (u';', 3), (u'}', 3), (u'http', 5), (u'{', 5), (u'#forteen', 5),
        (u'# this is a comment', 6),(u'access_log', 7), (u'off', 7), (u';', 7),
        (u'default_type', 7), (u'text/plain', 7), (u';', 7), (u'error_log', 7),
        (u'off', 7), (u';', 7), (u'server', 8), (u'{', 8), (u'listen', 9),
        (u'8083', 9), (u';', 9), (u'return', 10), (u'200', 10),
        (u'Ser" \' \' ver\\\\ \\ $server_addr:\\$server_port\\n\\nTime: $time_local\\n\\n', 10),
        (u';', 10), (u'}', 11), (u'server', 12), (u'{', 12), (u'listen', 12),
        (u'8080', 12), (u';', 12), (u'root', 13), (u'/usr/share/nginx/html', 13),
        (u';', 13), (u'location', 14), (u'~', 14), (u'/hello/world;', 14),
        (u'{', 14), (u'return', 14), (u'301', 14), (u'/status.html', 14),
        (u';', 14), (u'}', 14), (u'location', 15), (u'/foo', 15),
        (u'{', 15), (u'}', 15), (u'location', 15), (u'/bar', 15),
        (u'{', 15), (u'}', 15), (u'location', 16), (u'/\\{\\;\\}\\ #\\ ab', 16),
        (u'{', 16), (u'}', 16), (u'# hello', 16), (u'if', 17),
        (u'($request_method', 17), (u'=', 17), (u'P\\{O\\)\\###\\;ST', 17),
        (u')', 17), (u'{', 17), (u'}', 17), (u'location', 18), (u'/status.html', 18),
        (u'{', 18), (u'try_files', 19), (u'/abc/${uri} /abc/${uri}.html', 19),
        (u'=404', 19), (u';', 19), (u'}', 20), (u'location', 21),
        (u'/sta;\n                    tus', 21), (u'{', 22), (u'return', 22),
        (u'302', 22), (u'/status.html', 22), (u';', 22), (u'}', 22),
        (u'location', 23), (u'/upstream_conf', 23), (u'{', 23),
        (u'return', 23), (u'200', 23), (u'/status.html', 23), (u';', 23),
        (u'}', 23), (u'}', 23), (u'server', 24), (u'{', 25), (u'}', 25),
        (u'}', 25)]
