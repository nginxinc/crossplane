# -*- coding: utf-8 -*-


import os
import crossplane
from crossplane.objects import NginxDirective
from crossplane.ext.lua import LuaBlockDirective
from ..test_build import compare_parsed_and_built

tests_dir = os.path.dirname(__file__) + "/" + os.path.pardir


def test_lex_lua_block_simple():
    dirname = os.path.join(tests_dir, 'configs', 'lua-block-simple')
    config = os.path.join(dirname, 'nginx.conf')
    tokens = crossplane.lex(config)
    assert list(tokens) == [
        (u'http', 1), (u'{', 1),
        (u'init_by_lua_block', 2), (u'\n        print("Lua block code with curly brace str {")\n    ', 4), (u';', 4),
        (u'init_worker_by_lua_block', 5), (u'\n        print("Work that every worker")\n    ', 7), (u';', 7),
        (u'body_filter_by_lua_block', 8), (u'\n        local data, eof = ngx.arg[1], ngx.arg[2]\n    ', 10), (u';', 10),
        (u'header_filter_by_lua_block', 11), (u'\n        ngx.header["content-length"] = nil\n    ', 13),  (u';', 13),
        (u'server', 14), (u'{', 14), (u'listen', 15), (u'127.0.0.1:8080', 15), (u';', 15),
        (u'location', 16), (u'/', 16), (u'{', 16),
        (u'content_by_lua_block', 17), (u'\n                ngx.say("I need no extra escaping here, for example: \\r\\nblah")\n            ', 19),(u';', 19),
        (u'return', 20), (u'200', 20), (u'foo bar baz', 20), (u';', 20), (u'}', 21),
        (u'ssl_certificate_by_lua_block', 22), (u'\n            print("About to initiate a new SSL handshake!")\n        ', 24), (u';', 24),
        (u'location', 25), (u'/a', 25), (u'{', 25), (u'client_max_body_size', 26), (u'100k', 26), (u';', 26),
        (u'client_body_buffer_size', 27), (u'100k', 27), (u';', 27), (u'}', 28), (u'}', 29),
        (u'upstream', 31), (u'foo', 31), (u'{', 31), (u'server', 32), (u'127.0.0.1', 32), (u';', 32),
        (u'balancer_by_lua_block', 33), (u'\n            -- use Lua to do something interesting here\n        ', 35), (u';', 35),
        (u'log_by_lua_block', 36), (u'\n            print("I need no extra escaping here, for example: \\r\\nblah")\n        ', 38),
        (u';', 38), (u'}', 39), (u'}', 40)
    ]


def test_lex_lua_block_larger():
    dirname = os.path.join(tests_dir, 'configs', 'lua-block-larger')
    config = os.path.join(dirname, 'nginx.conf')
    tokens = crossplane.lex(config)
    assert list(tokens) == [
        (u'http', 1), (u'{', 1),
        (u'content_by_lua_block', 2),
        (
            u'\n        ngx.req.read_body()  -- explicitly read the req body\n        local data = ngx.req.get_body_data()\n        if data then\n            ngx.say("body data:")\n            ngx.print(data)\n            return\n        end\n\n        -- body may get buffered in a temp file:\n        local file = ngx.req.get_body_file()\n        if file then\n            ngx.say("body is in file ", file)\n        else\n            ngx.say("no body found")\n        end\n    ',
            18), (u';', 18),
        (u'access_by_lua_block', 19),
        (
            u'\n        -- check the client IP address is in our black list\n        if ngx.var.remote_addr == "132.5.72.3" then\n            ngx.exit(ngx.HTTP_FORBIDDEN)\n        end\n\n        -- check if the URI contains bad words\n        if ngx.var.uri and\n               string.match(ngx.var.request_body, "evil")\n        then\n            return ngx.redirect("/terms_of_use.html")\n        end\n\n        -- tests passed\n    ',
            33), (u';', 33), (u'}', 34)
    ]


def test_lex_lua_block_tricky():
    dirname = os.path.join(tests_dir, 'configs', 'lua-block-tricky')
    config = os.path.join(dirname, 'nginx.conf')
    tokens = crossplane.lex(config)
    assert list(tokens) == [
        (u'http', 1), (u'{', 1), (u'server', 2), (u'{', 2), (u'listen', 3), (u'127.0.0.1:8080', 3), (u';', 3),
        (u'server_name', 4), (u'content_by_lua_block', 4), (u';', 4),
        (u"# make sure this doesn't trip up lexers", 4),
        (u'set_by_lua_block', 5), (u'$res', 5),
        (
        u'  # irregular lua block directive\n            local a = 32\n            local b = 56\n\n            ngx.var.diff = a - b;  -- write to $diff directly\n            return a + b;          -- return the $sum value normally\n        ',
        11),
        (u';', 11),
        (u'rewrite_by_lua_block', 12),
        (
        u' # have valid braces in Lua code\n            do_something("hello, world!\\nhiya\\n")\n            a = { 1, 2, 3 }\n            btn = iup.button({title="ok"})\n        ',
        16),
        (u';', 16),
        (u'}', 17),
        (u'}', 18)
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
                                                'args': ['\n                ngx.say("I need no extra escaping here, for example: \\r\\nblah")\n            '],
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
                                        'args': ['\n            print("About to initiate a new SSL handshake!")\n        '],
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
                                'args': [ 'foo' ],
                                'block': [
                                    {
                                        'line': 32,
                                        'args': ['127.0.0.1'],
                                        'directive': 'server'
                                    },
                                    {
                                        'line': 33,
                                        'args': ['\n            -- use Lua to do something interesting here\n        '],
                                        'directive': 'balancer_by_lua_block'
                                    },
                                    {
                                        'line': 36,
                                        'args': ['\n            print("I need no extra escaping here, for example: \\r\\nblah")\n        '], 'directive': 'log_by_lua_block'}],
                                'directive': 'upstream'
                            }
                        ],
                        'directive': 'http'
                    }
                ],
                'file': os.path.join(dirname, 'nginx.conf')
            }
        ]
    }


def test_parse_lua_block_tricky():
    dirname = os.path.join(tests_dir, 'configs', 'lua-block-tricky')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config)
    assert payload == {
        'status': 'ok',
        'errors': [],
        'config': [
            {
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
                                        'line': 5,
                                        'args': ['$res', '  # irregular lua block directive\n            local a = 32\n            local b = 56\n\n            ngx.var.diff = a - b;  -- write to $diff directly\n            return a + b;          -- return the $sum value normally\n        '],
                                        'directive': 'set_by_lua_block'
                                    },
                                    {
                                        'line': 12,
                                        'args': [' # have valid braces in Lua code\n            do_something("hello, world!\\nhiya\\n")\n            a = { 1, 2, 3 }\n            btn = iup.button({title="ok"})\n        '],
                                        'directive': 'rewrite_by_lua_block'
                                    }
                                ],
                                'directive': 'server'
                            }
                        ],
                        'directive': 'http'
                    }
                ],
                'file': os.path.join(dirname, 'nginx.conf')
            }
        ]
    }


def test_build_lua_blocks_simple(tmpdir):
    compare_parsed_and_built('lua-block-simple', 'nginx.conf', tmpdir)


def test_build_lua_blocks_larger(tmpdir):
    compare_parsed_and_built('lua-block-larger', 'nginx.conf', tmpdir)


def test_build_lua_blocks_tricky(tmpdir):
    compare_parsed_and_built('lua-block-tricky', 'nginx.conf', tmpdir)


def test_load_lua_blocks_tricky():
    config = os.path.join(tests_dir, 'configs', 'lua-block-tricky', 'nginx.conf')

    xconfig = crossplane.load(config)
    assert xconfig is not None
    assert isinstance(xconfig, crossplane.objects.CrossplaneConfig)
    assert len(xconfig.configs) == 1

    server = xconfig.configs[0].get('http')[0].get('server')[0]
    set_by_lua_block = server.get('set_by_lua_block')[0]
    assert isinstance(set_by_lua_block, LuaBlockDirective)
    assert len(set_by_lua_block.args) == 2
    assert set_by_lua_block.args == ['$res', '  # irregular lua block directive\n            local a = 32\n            local b = 56\n\n            ngx.var.diff = a - b;  -- write to $diff directly\n            return a + b;          -- return the $sum value normally\n        ']

    server_name = server.get('server_name')[0]
    assert isinstance(server_name, NginxDirective)
    assert server_name.args == ['content_by_lua_block']

    rewrite_by_lua_block = server.get('rewrite_by_lua_block')[0]
    assert isinstance(rewrite_by_lua_block, LuaBlockDirective)
    assert rewrite_by_lua_block.args == [' # have valid braces in Lua code\n            do_something("hello, world!\\nhiya\\n")\n            a = { 1, 2, 3 }\n            btn = iup.button({title="ok"})\n        ']
