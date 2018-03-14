# -*- coding: utf-8 -*-
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
           "args" : [],
           "block" : [
              {
                 "args" : [
                    "1024"
                 ],
                 "line" : 2,
                 "directive" : "worker_connections"
              }
           ],
           "line" : 1,
           "directive" : "events"
        },
        {
           "directive" : "#",
           "line" : 4,
           "comment" : "comment",
           "args" : []
        },
        {
           "directive" : "http",
           "block" : [
              {
                 "args" : [],
                 "line" : 6,
                 "block" : [
                    {
                       "args" : [
                          "127.0.0.1:8080"
                       ],
                       "line" : 7,
                       "directive" : "listen"
                    },
                    {
                       "directive" : "#",
                       "line" : 7,
                       "comment" : "listen",
                       "args" : []
                    },
                    {
                       "args" : [
                          "default_server"
                       ],
                       "directive" : "server_name",
                       "line" : 8
                    },
                    {
                       "args" : [
                          "/"
                       ],
                       "directive" : "location",
                       "line" : 9,
                       "block" : [
                          {
                             "args" : [],
                             "directive" : "#",
                             "line" : 9,
                             "comment" : "# this is brace"
                          },
                          {
                             "directive" : "#",
                             "comment" : " location /",
                             "line" : 10,
                             "args" : []
                          },
                          {
                             "directive" : "#",
                             "comment" : " is here",
                             "line" : 11,
                             "args" : []
                          },
                          {
                             "args" : [
                                "200",
                                "foo bar baz"
                             ],
                             "line" : 11,
                             "directive" : "return"
                          }
                       ]
                    }
                 ],
                 "directive" : "server"
              }
           ],
           "line" : 5,
           "args" : []
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


def test_compare_parsed_and_built_simple(tmpdir):
    compare_parsed_and_built('simple', 'nginx.conf', tmpdir)


def test_compare_parsed_and_built_messy(tmpdir):
    compare_parsed_and_built('messy', 'nginx.conf', tmpdir)


def test_compare_parsed_and_built_messy_with_comments(tmpdir):
    compare_parsed_and_built('with-comments', 'nginx.conf', tmpdir, comments=True)
