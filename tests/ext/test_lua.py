# -*- coding: utf-8 -*-
import os

import crossplane
from .. import compare_parsed_and_built, here as tests_dir


def test_lex_lua_block_simple():
    dirname = os.path.join(tests_dir, 'configs', 'lua-block-simple')
    config = os.path.join(dirname, 'nginx.conf')
    tokens = crossplane.lex(config)
    assert list((token, line) for token, line, quoted in tokens) == [
        ('http', 1),
        ('{', 1),
        ('init_by_lua_block', 2),
        ('\n        print("Lua block code with curly brace str {")\n    ', 4),
        (';', 4),
        ('init_worker_by_lua_block', 5),
        ('\n        print("Work that every worker")\n    ', 7),
        (';', 7),
        ('body_filter_by_lua_block', 8),
        ('\n        local data, eof = ngx.arg[1], ngx.arg[2]\n    ', 10),
        (';', 10),
        ('header_filter_by_lua_block', 11),
        ('\n        ngx.header["content-length"] = nil\n    ', 13),
        (';', 13),
        ('server', 14),
        ('{', 14),
        ('listen', 15),
        ('127.0.0.1:8080', 15),
        (';', 15),
        ('location', 16),
        ('/', 16),
        ('{', 16),
        ('content_by_lua_block', 17),
        ('\n                ngx.say("I need no extra escaping here, for example: \\r\\nblah")\n            ', 19),
        (';', 19),
        ('return', 20),
        ('200', 20),
        ('foo bar baz', 20),
        (';', 20),
        ('}', 21),
        ('ssl_certificate_by_lua_block', 22),
        ('\n            print("About to initiate a new SSL handshake!")\n        ', 24),
        (';', 24),
        ('location', 25),
        ('/a', 25),
        ('{', 25),
        ('client_max_body_size', 26),
        ('100k', 26),
        (';', 26),
        ('client_body_buffer_size', 27),
        ('100k', 27),
        (';', 27),
        ('}', 28),
        ('}', 29),
        ('upstream', 31),
        ('foo', 31),
        ('{', 31),
        ('server', 32),
        ('127.0.0.1', 32),
        (';', 32),
        ('balancer_by_lua_block', 33),
        ('\n            -- use Lua to do something interesting here\n        ', 35),
        (';', 35),
        ('log_by_lua_block', 36),
        ('\n            print("I need no extra escaping here, for example: \\r\\nblah")\n        ', 38),
        (';', 38),
        ('}', 39),
        ('}', 40)
    ]


def test_lex_lua_block_larger():
    dirname = os.path.join(tests_dir, 'configs', 'lua-block-larger')
    config = os.path.join(dirname, 'nginx.conf')
    tokens = crossplane.lex(config)
    assert list((token, line) for token, line, quoted in tokens) == [
        ('http', 1),
        ('{', 1),
        ('content_by_lua_block', 2),
        (
            '\n        ngx.req.read_body()  -- explicitly read the req body'
            '\n        local data = ngx.req.get_body_data()'
            '\n        if data then'
            '\n            ngx.say("body data:")'
            '\n            ngx.print(data)'
            '\n            return'
            '\n        end'
            '\n'
            '\n        -- body may get buffered in a temp file:'
            '\n        local file = ngx.req.get_body_file()'
            '\n        if file then'
            '\n            ngx.say("body is in file ", file)'
            '\n        else'
            '\n            ngx.say("no body found")'
            '\n        end'
            '\n    ',
            18
        ),
        (';', 18),
        ('access_by_lua_block', 19),
        (
            '\n        -- check the client IP address is in our black list'
            '\n        if ngx.var.remote_addr == "132.5.72.3" then'
            '\n            ngx.exit(ngx.HTTP_FORBIDDEN)'
            '\n        end'
            '\n'
            '\n        -- check if the URI contains bad words'
            '\n        if ngx.var.uri and'
            '\n               string.match(ngx.var.request_body, "evil")'
            '\n        then'
            '\n            return ngx.redirect("/terms_of_use.html")'
            '\n        end'
            '\n'
            '\n        -- tests passed'
            '\n    ',
            33
        ),
        (';', 33),
        ('}', 34)
    ]


def test_lex_lua_block_tricky():
    dirname = os.path.join(tests_dir, 'configs', 'lua-block-tricky')
    config = os.path.join(dirname, 'nginx.conf')
    tokens = crossplane.lex(config)
    assert list((token, line) for token, line, quoted in tokens) == [
        ('http', 1),
        ('{', 1),
        ('server', 2),
        ('{', 2),
        ('listen', 3),
        ('127.0.0.1:8080', 3),
        (';', 3),
        ('server_name', 4),
        ('content_by_lua_block', 4),
        (';', 4),
        ("# make sure this doesn't trip up lexers", 4),
        ('set_by_lua_block', 5),
        ('$res', 5),
        (
            ' -- irregular lua block directive'
            '\n            local a = 32'
            '\n            local b = 56'
            '\n'
            '\n            ngx.var.diff = a - b;  -- write to $diff directly'
            '\n            return a + b;          -- return the $sum value normally'
            '\n        ',
            11
        ),
        (';', 11),
        ('rewrite_by_lua_block', 12),
        (
            ' -- have valid braces in Lua code and quotes around directive'
            '\n            do_something("hello, world!\\nhiya\\n")'
            '\n            a = { 1, 2, 3 }'
            '\n            btn = iup.button({title="ok"})'
            '\n        ',
            16
        ),
        (';', 16),
        ('}', 17),
        ('upstream', 18),
        ('content_by_lua_block', 18),
        ('{', 18),
        ('# stuff', 19),
        ('}', 20),
        ('}', 21)
    ]


def test_parse_lua_block_simple():
    dirname = os.path.join(tests_dir, 'configs', 'lua-block-simple')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config)
    assert payload == {
        'status': 'ok',
        'errors': [],
        'config': [
            {
                'file': os.path.join(dirname, 'nginx.conf'),
                'status': 'ok',
                'errors': [],
                'parsed': [
                    {
                        'line': 1,
                        'args': [],
                        'block': [
                            {
                                'line': 2,
                                'args': ['\n        print("Lua block code with curly brace str {")\n    '],
                                'directive': 'init_by_lua_block'
                            },
                            {
                                'line': 5,
                                'args': ['\n        print("Work that every worker")\n    '],
                                'directive': 'init_worker_by_lua_block'
                            },
                            {
                                'line': 8,
                                'args': ['\n        local data, eof = ngx.arg[1], ngx.arg[2]\n    '],
                                'directive': 'body_filter_by_lua_block'
                            },
                            {
                                'line': 11,
                                'args': ['\n        ngx.header["content-length"] = nil\n    '],
                                'directive': 'header_filter_by_lua_block'
                            },
                            {
                                'line': 14,
                                'args': [],
                                'block': [
                                    {
                                        'line': 15,
                                        'args': ['127.0.0.1:8080'],
                                        'directive': 'listen'
                                    },
                                    {
                                        'line': 16,
                                        'args': ['/'],
                                        'block': [
                                            {
                                                'line': 17,
                                                'args': [
                                                    '\n                ngx.say("I need no extra escaping here, for example: \\r\\nblah")'
                                                    '\n            '
                                                ],
                                                'directive': 'content_by_lua_block'
                                            },
                                            {
                                                'line': 20,
                                                'args': ['200', 'foo bar baz'],
                                                'directive': 'return'
                                            }
                                        ],
                                        'directive': 'location'
                                    },
                                    {
                                        'line': 22,
                                        'args': [
                                            '\n            print("About to initiate a new SSL handshake!")'
                                            '\n        '
                                        ],
                                        'directive': 'ssl_certificate_by_lua_block'
                                    },
                                    {
                                        'line': 25,
                                        'args': ['/a'],
                                        'block': [
                                            {
                                                'line': 26,
                                                'args': ['100k'],
                                                'directive': 'client_max_body_size'
                                            },
                                            {
                                                'line': 27,
                                                'args': ['100k'],
                                                'directive': 'client_body_buffer_size'
                                            }
                                        ],
                                        'directive': 'location'
                                    }
                                ],
                                'directive': 'server'
                            },
                            {
                                'line': 31,
                                'args': ['foo'],
                                'block': [
                                    {
                                        'line': 32,
                                        'args': ['127.0.0.1'],
                                        'directive': 'server'
                                    },
                                    {
                                        'line': 33,
                                        'args': [
                                            '\n            -- use Lua to do something interesting here'
                                            '\n        '
                                        ],
                                        'directive': 'balancer_by_lua_block'
                                    },
                                    {
                                        'line': 36,
                                        'args': [
                                            '\n            print("I need no extra escaping here, for example: \\r\\nblah")'
                                            '\n        '
                                        ],
                                        'directive': 'log_by_lua_block'
                                    }
                                ],
                                'directive': 'upstream'
                            }
                        ],
                        'directive': 'http'
                    }
                ]
            }
        ]
    }


def test_parse_lua_block_tricky():
    dirname = os.path.join(tests_dir, 'configs', 'lua-block-tricky')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config, comments=True)
    assert payload == {
        'status': 'ok',
        'errors': [],
        'config': [
            {
                'file': os.path.join(dirname, 'nginx.conf'),
                'status': 'ok',
                'errors': [],
                'parsed': [
                    {
                        'line': 1,
                        'args': [],
                        'block': [
                            {
                                'line': 2,
                                'args': [],
                                'block': [
                                    {
                                        'line': 3,
                                        'args': ['127.0.0.1:8080'],
                                        'directive': 'listen'
                                    },
                                    {
                                        'line': 4,
                                        'args': ['content_by_lua_block'],
                                        'directive': 'server_name'
                                    },
                                    {
                                        'comment': u" make sure this doesn't trip up lexers",
                                        'line': 4,
                                        'args': [],
                                        'directive': '#'
                                    },
                                    {
                                        'line': 5,
                                        'args': [
                                            '$res',
                                            ' -- irregular lua block directive'
                                            '\n            local a = 32'
                                            '\n            local b = 56'
                                            '\n'
                                            '\n            ngx.var.diff = a - b;  -- write to $diff directly'
                                            '\n            return a + b;          -- return the $sum value normally'
                                            '\n        '
                                        ],
                                        'directive': 'set_by_lua_block'
                                    },
                                    {
                                        'line': 12,
                                        'args': [
                                            ' -- have valid braces in Lua code and quotes around directive'
                                            '\n            do_something("hello, world!\\nhiya\\n")'
                                            '\n            a = { 1, 2, 3 }'
                                            '\n            btn = iup.button({title="ok"})'
                                            '\n        '
                                        ],
                                        'directive': 'rewrite_by_lua_block'
                                    }
                                ],
                                'directive': 'server'
                            },
                            {
                                'line': 18,
                                'args': ['content_by_lua_block'],
                                'block': [
                                    {
                                        'comment': ' stuff',
                                        'line': 19,
                                        'args': [],
                                        'directive': '#'
                                    }
                                ],
                                'directive': 'upstream'
                            }
                        ],
                        'directive': 'http'
                    }
                ]
            }
        ]
    }


def test_build_lua_blocks_simple(tmpdir):
    compare_parsed_and_built('lua-block-simple', 'nginx.conf', tmpdir)


def test_build_lua_blocks_larger(tmpdir):
    compare_parsed_and_built('lua-block-larger', 'nginx.conf', tmpdir)


def test_build_lua_blocks_tricky(tmpdir):
    compare_parsed_and_built('lua-block-tricky', 'nginx.conf', tmpdir)
