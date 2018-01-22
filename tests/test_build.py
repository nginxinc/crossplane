# -*- coding: utf-8 -*-

import crossplane


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
