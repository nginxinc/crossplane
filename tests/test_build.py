# -*- coding: utf-8 -*-
import os

import crossplane
from . import compare_parsed_and_built


def test_build_nested_and_multiple_args():
    payload = [
        {
            "directive": "events",
            "args": [],
            "block": [
                {
                    "directive": "worker_connections",
                    "args": ["1024"]
                }
            ]
        },
        {
            "directive": "http",
            "args": [],
            "block": [
                {
                    "directive": "server",
                    "args": [],
                    "block": [
                        {
                            "directive": "listen",
                            "args": ["127.0.0.1:8080"]
                        },
                        {
                            "directive": "server_name",
                            "args": ["default_server"]
                        },
                        {
                            "directive": "location",
                            "args": ["/"],
                            "block": [
                                {
                                    "directive": "return",
                                    "args": ["200", "foo bar baz"]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    built = crossplane.build(payload, indent=4, tabs=False)

    assert built == '\n'.join([
        'events {',
        '    worker_connections 1024;',
        '}',
        'http {',
        '    server {',
        '        listen 127.0.0.1:8080;',
        '        server_name default_server;',
        '        location / {',
        "            return 200 'foo bar baz';",
        '        }',
        '    }',
        '}'
    ])


def test_build_with_comments():
    payload = [
        {
            "directive": "events",
            "line": 1,
            "args": [],
            "block": [
                {
                    "directive": "worker_connections",
                    "line": 2,
                    "args": ["1024"]
                }
            ]
        },
        {
            "directive": "#",
            "line": 4,
            "args": [],
            "comment": "comment"
        },
        {
            "directive": "http",
            "line": 5,
            "args": [],
            "block": [
                {
                    "directive": "server",
                    "line": 6,
                    "args": [],
                    "block": [
                        {
                            "directive": "listen",
                            "line": 7,
                            "args": ["127.0.0.1:8080"]
                        },
                        {
                            "directive": "#",
                            "line": 7,
                            "args": [],
                            "comment": "listen"
                        },
                        {
                            "directive": "server_name",
                            "line": 8,
                            "args": ["default_server"]
                        },
                        {
                            "directive": "location",
                            "line": 9,
                            "args": ["/"],
                            "block": [
                                {
                                    "directive": "#",
                                    "line": 9,
                                    "args": [],
                                    "comment": "# this is brace"
                                },
                                {
                                    "directive": "#",
                                    "line": 10,
                                    "args": [],
                                    "comment": " location /"
                                },
                                {
                                    "directive": "#",
                                    "line": 11,
                                    "args": [],
                                    "comment": " is here"
                                },
                                {
                                    "directive": "return",
                                    "line": 12,
                                    "args": ["200", "foo bar baz"]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    built = crossplane.build(payload, indent=4, tabs=False)

    assert built == '\n'.join([
        'events {',
        '    worker_connections 1024;',
        '}',
        '#comment',
        'http {',
        '    server {',
        '        listen 127.0.0.1:8080; #listen',
        '        server_name default_server;',
        '        location / { ## this is brace',
        '            # location /',
        '            # is here',
        "            return 200 'foo bar baz';",
        '        }',
        '    }',
        '}'
    ])


def test_build_with_quoted_unicode():
    payload = [
        {
            "directive": "env",
            "line": 1,
            "args": ["русский текст"],
        }
    ]

    built = crossplane.build(payload, indent=4, tabs=False)

    assert built == u"env 'русский текст';"


def test_build_files_with_missing_status_and_errors(tmpdir):
    assert len(tmpdir.listdir()) == 0
    payload = {
        "config": [
            {
                "file": "nginx.conf",
                "parsed": [
                    {
                        "directive": "user",
                        "line": 1,
                        "args": ["nginx"],
                    }
                ]
            }
        ]
    }
    crossplane.builder.build_files(payload, dirname=tmpdir.strpath)
    built_files = tmpdir.listdir()
    assert len(built_files) == 1
    assert built_files[0].strpath == os.path.join(tmpdir.strpath, 'nginx.conf')
    assert built_files[0].read_text('utf-8') == 'user nginx;\n'


def test_build_files_with_unicode(tmpdir):
    assert len(tmpdir.listdir()) == 0
    payload = {
        "status": "ok",
        "errors": [],
        "config": [
            {
                "file": "nginx.conf",
                "status": "ok",
                "errors": [],
                "parsed": [
                    {
                        "directive": "user",
                        "line": 1,
                        "args": [u"測試"],
                    }
                ]
            }
        ]
    }
    crossplane.builder.build_files(payload, dirname=tmpdir.strpath)
    built_files = tmpdir.listdir()
    assert len(built_files) == 1
    assert built_files[0].strpath == os.path.join(tmpdir.strpath, 'nginx.conf')
    assert built_files[0].read_text('utf-8') == u'user 測試;\n'


def test_compare_parsed_and_built_simple(tmpdir):
    compare_parsed_and_built('simple', 'nginx.conf', tmpdir)


def test_compare_parsed_and_built_messy(tmpdir):
    compare_parsed_and_built('messy', 'nginx.conf', tmpdir)


def test_compare_parsed_and_built_messy_with_comments(tmpdir):
    compare_parsed_and_built('with-comments', 'nginx.conf', tmpdir, comments=True)


def test_compare_parsed_and_built_empty_map_values(tmpdir):
    compare_parsed_and_built('empty-value-map', 'nginx.conf', tmpdir)


def test_compare_parsed_and_built_russian_text(tmpdir):
    compare_parsed_and_built('russian-text', 'nginx.conf', tmpdir)


def test_compare_parsed_and_built_quoted_right_brace(tmpdir):
    compare_parsed_and_built('quoted-right-brace', 'nginx.conf', tmpdir)


def test_compare_parsed_and_built_directive_with_space(tmpdir):
    compare_parsed_and_built('directive-with-space', 'nginx.conf', tmpdir)
