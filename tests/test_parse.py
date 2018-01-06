# -*- coding: utf-8 -*-
import os

import crossplane

here = os.path.dirname(__file__)


def test_includes_regular():
    dirname = os.path.join(here, 'configs', 'includes-regular')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config)
    assert payload == {
        'status': 'failed',
        'errors': [
            {
                'file': os.path.join(dirname, 'conf.d', 'server.conf'),
                'error': '[Errno 2] No such file or directory: %r' % os.path.join(dirname, 'bar.conf'),
                'line': 5
            }
        ],
        'config': [
            {
                'file': os.path.join(dirname, 'nginx.conf'),
                'status': 'ok',
                'errors': [],
                'parsed': [
                    {
                        'directive': 'events',
                        'line': 1,
                        'args': [],
                        'block': []
                    },
                    {
                        'directive': 'http',
                        'line': 2,
                        'args': [],
                        'block': [
                            {
                                'directive': 'include',
                                'line': 3,
                                'args': ['conf.d/server.conf'],
                                'includes': [1]
                            }
                        ]
                    }
                ]
            },
            {
                'file': os.path.join(dirname, 'conf.d', 'server.conf'),
                'status': 'failed',
                'errors': [
                    {
                        'error': '[Errno 2] No such file or directory: %r' % os.path.join(dirname, 'bar.conf'),
                        'line': 5
                    }
                ],
                'parsed': [
                    {
                        'directive': 'server',
                        'line': 1,
                        'args': [],
                        'block': [
                            {
                                'directive': 'listen',
                                'line': 2,
                                'args': ['127.0.0.1:8080']
                            },
                            {
                                'directive': 'server_name',
                                'line': 3,
                                'args': ['default_server']
                            },
                            {
                                'directive': 'include',
                                'line': 4,
                                'args': ['foo.conf'],
                                'includes': [2]
                            },
                            {
                                'directive': 'include',
                                'line': 5,
                                'args': ['bar.conf'],
                                'includes': []
                            }
                        ]
                    }
                ]
            },
            {
                'file': os.path.join(dirname, 'foo.conf'),
                'status': 'ok',
                'errors': [],
                'parsed': [
                    {
                        'directive': 'location',
                        'line': 1,
                        'args': ['/foo'],
                        'block': [
                            {
                                'directive': 'return',
                                'line': 2,
                                'args': ['200', 'foo']
                            }
                        ]
                    }
                ]
            }
        ]
    }


def test_includes_globbed():
    dirname = os.path.join(here, 'configs', 'includes-globbed')
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
                        'directive': 'events',
                        'line': 1,
                        'args': [],
                        'block': []
                    },
                    {
                        'directive': 'include',
                        'line': 2,
                        'args': ['http.conf'],
                        'includes': [1]
                    }
                ]
            },
            {
                'file': os.path.join(dirname, 'http.conf'),
                'status': 'ok',
                'errors': [],
                'parsed': [
                    {
                        'directive': 'http',
                        'args': [],
                        'line': 1,
                        'block': [
                            {
                                'directive': 'include',
                                'line': 2,
                                'args': ['servers/*.conf'],
                                'includes': [2, 3]
                            }
                        ]
                    }
                ]
            },
            {
                'file': os.path.join(dirname, 'servers', 'server1.conf'),
                'status': 'ok',
                'errors': [],
                'parsed': [
                    {
                        'directive': 'server',
                        'args': [],
                        'line': 1,
                        'block': [
                            {
                                'directive': 'listen',
                                'args': ['8080'],
                                'line': 2
                            },
                            {
                                'directive': 'include',
                                'args': ['locations/*.conf'],
                                'line': 3,
                                'includes': [4, 5]
                            }
                        ]
                    }
                ]
            },
            {
                'file': os.path.join(dirname, 'servers', 'server2.conf'),
                'status': 'ok',
                'errors': [],
                'parsed': [
                    {
                        'directive': 'server',
                        'args': [],
                        'line': 1,
                        'block': [
                            {
                                'directive': 'listen',
                                'args': ['8081'],
                                'line': 2
                            },
                            {
                                'directive': 'include',
                                'args': ['locations/*.conf'],
                                'line': 3,
                                'includes': [4, 5]
                            }
                        ]
                    }
                ]
            },
            {
                'file': os.path.join(dirname, 'locations', 'location1.conf'),
                'status': 'ok',
                'errors': [],
                'parsed': [
                    {
                        'directive': 'location',
                        'args': ['/foo'],
                        'line': 1,
                        'block': [
                            {
                                'directive': 'return',
                                'args': ['200', 'foo'],
                                'line': 2
                            }
                        ]
                    }
                ]
            },
            {
                'file': os.path.join(dirname, 'locations', 'location2.conf'),
                'status': 'ok',
                'errors': [],
                'parsed': [
                    {
                        'directive': 'location',
                        'args': ['/bar'],
                        'line': 1,
                        'block': [
                            {
                                'directive': 'return',
                                'args': ['200', 'bar'],
                                'line': 2
                            }
                        ]
                    }
                ]
            }
        ]
    }


def test_includes_single():
    dirname = os.path.join(here, 'configs', 'includes-regular')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config, single=True)
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
                        'directive': 'events',
                        'line': 1,
                        'args': [],
                        'block': []
                    },
                    {
                        'directive': 'http',
                        'line': 2,
                        'args': [],
                        'block': [
                            {
                                'directive': 'include',
                                'line': 3,
                                'args': ['conf.d/server.conf']
                                # no 'includes' key
                            }
                        ]
                    }
                ]
            }
            # single config parsed
        ]
    }


def test_ignore_directives():
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    # check that you can ignore multiple directives
    payload = crossplane.parse(config, ignore=['listen', 'server_name'])
    assert payload == {
        "status": "ok",
        "errors": [],
        "config": [
            {
                "file": os.path.join(dirname, 'nginx.conf'),
                "status": "ok",
                "errors": [],
                "parsed": [
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
                                        "directive": "location",
                                        "line": 9,
                                        "args": ["/"],
                                        "block": [
                                            {
                                                "directive": "return",
                                                "line": 10,
                                                "args": ["200", "foo bar baz"]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # check that you can also ignore block directives
    payload = crossplane.parse(config, ignore=['events', 'server'])
    assert payload == {
        "status": "ok",
        "errors": [],
        "config": [
            {
                "file": os.path.join(dirname, 'nginx.conf'),
                "status": "ok",
                "errors": [],
                "parsed": [
                    {
                        "directive": "http",
                        "line": 5,
                        "args": [],
                        "block": []
                    }
                ]
            }
        ]
    }
