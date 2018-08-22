# -*- coding: utf-8 -*-
import os

import crossplane
from . import here


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


def test_includes_globbed_combined():
    dirname = os.path.join(here, 'configs', 'includes-globbed')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config, combine=True)
    assert payload == {
        "status": "ok",
        "errors": [],
        "config": [
            {
                "file": os.path.join(dirname, "nginx.conf"),
                "status": "ok",
                "errors": [],
                "parsed": [
                    {
                        "directive": "events",
                        "args": [],
                        "file": os.path.join(dirname, "nginx.conf"),
                        "line": 1,
                        "block": []
                    },
                    {
                        "directive": "http",
                        "args": [],
                        "file": os.path.join(dirname, "http.conf"),
                        "line": 1,
                        "block": [
                            {
                                "directive": "server",
                                "args": [],
                                "file": os.path.join(dirname, "servers", "server1.conf"),
                                "line": 1,
                                "block": [
                                    {
                                        "directive": "listen",
                                        "args": ["8080"],
                                        "file": os.path.join(dirname, "servers", "server1.conf"),
                                        "line": 2
                                    },
                                    {
                                        "directive": "location",
                                        "args": ["/foo"],
                                        "file": os.path.join(dirname, "locations", "location1.conf"),
                                        "line": 1,
                                        "block": [
                                            {
                                                "directive": "return",
                                                "args": ["200", "foo"],
                                                "file": os.path.join(dirname, "locations", "location1.conf"),
                                                "line": 2
                                            }
                                        ]
                                    },
                                    {
                                        "directive": "location",
                                        "args": ["/bar"],
                                        "file": os.path.join(dirname, "locations", "location2.conf"),
                                        "line": 1,
                                        "block": [
                                            {
                                                "directive": "return",
                                                "args": ["200", "bar"],
                                                "file": os.path.join(dirname, "locations", "location2.conf"),
                                                "line": 2
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "directive": "server",
                                "args": [],
                                "file": os.path.join(dirname, "servers", "server2.conf"),
                                "line": 1,
                                "block": [
                                    {
                                        "directive": "listen",
                                        "args": ["8081"],
                                        "file": os.path.join(dirname, "servers", "server2.conf"),
                                        "line": 2
                                    },
                                    {
                                        "directive": "location",
                                        "args": ["/foo"],
                                        "file": os.path.join(dirname, "locations", "location1.conf"),
                                        "line": 1,
                                        "block": [
                                            {
                                                "directive": "return",
                                                "args": ["200", "foo"],
                                                "file": os.path.join(dirname, "locations", "location1.conf"),
                                                "line": 2
                                            }
                                        ]
                                    },
                                    {
                                        "directive": "location",
                                        "args": ["/bar"],
                                        "file": os.path.join(dirname, "locations", "location2.conf"),
                                        "line": 1,
                                        "block": [
                                            {
                                                "directive": "return",
                                                "args": ["200", "bar"],
                                                "file": os.path.join(dirname, "locations", "location2.conf"),
                                                "line": 2
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


def test_config_with_comments():
    dirname = os.path.join(here, 'configs', 'with-comments')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config, comments=True)
    assert payload == {
       "errors" : [],
       "status" : "ok",
       "config" : [
          {
             "errors" : [],
             "parsed" : [
                {
                   "block" : [
                      {
                         "directive" : "worker_connections",
                         "args" : [
                            "1024"
                         ],
                         "line" : 2
                      }
                   ],
                   "line" : 1,
                   "args" : [],
                   "directive" : "events"
                },
                {
                   "line" : 4,
                   "directive": "#",
                   "args": [],
                   "comment" : "comment"
                },
                {
                   "block" : [
                      {
                         "args" : [],
                         "directive" : "server",
                         "line" : 6,
                         "block" : [
                            {
                               "args" : [
                                  "127.0.0.1:8080"
                               ],
                               "directive" : "listen",
                               "line" : 7
                            },
                            {
                               "args": [],
                               "directive": "#",
                               "comment" : "listen",
                               "line" : 7
                            },
                            {
                               "args" : [
                                  "default_server"
                               ],
                               "directive" : "server_name",
                               "line" : 8
                            },
                            {
                               "block" : [
                                  {
                                     "args": [],
                                     "directive": "#",
                                     "line" : 9,
                                     "comment" : "# this is brace"
                                  },
                                  {
                                     "args": [],
                                     "directive": "#",
                                     "line" : 10,
                                     "comment" : " location /"
                                  },
                                  {
                                     "line" : 11,
                                     "directive" : "return",
                                     "args" : [
                                        "200",
                                        "foo bar baz"
                                     ]
                                  }
                               ],
                               "line" : 9,
                               "directive" : "location",
                               "args" : [
                                  "/"
                               ]
                            }
                         ]
                      }
                   ],
                   "line" : 5,
                   "args" : [],
                   "directive" : "http"
                }
             ],
             "status" : "ok",
             "file" : os.path.join(dirname, 'nginx.conf')
          }
       ]
    }


def test_config_without_comments():
    dirname = os.path.join(here, 'configs', 'with-comments')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config, comments=False)
    assert payload == {
       "errors" : [],
       "status" : "ok",
       "config" : [
          {
             "errors" : [],
             "parsed" : [
                {
                   "block" : [
                      {
                         "directive" : "worker_connections",
                         "args" : [
                            "1024"
                         ],
                         "line" : 2
                      }
                   ],
                   "line" : 1,
                   "args" : [],
                   "directive" : "events"
                },
                {
                   "block" : [
                      {
                         "args" : [],
                         "directive" : "server",
                         "line" : 6,
                         "block" : [
                            {
                               "args" : [
                                  "127.0.0.1:8080"
                               ],
                               "directive" : "listen",
                               "line" : 7
                            },
                            {
                               "args" : [
                                  "default_server"
                               ],
                               "directive" : "server_name",
                               "line" : 8
                            },
                            {
                               "block" : [
                                  {
                                     "line" : 11,
                                     "directive" : "return",
                                     "args" : [
                                        "200",
                                        "foo bar baz"
                                     ]
                                  }
                               ],
                               "line" : 9,
                               "directive" : "location",
                               "args" : [
                                  "/"
                               ]
                            }
                         ]
                      }
                   ],
                   "line" : 5,
                   "args" : [],
                   "directive" : "http"
                }
             ],
             "status" : "ok",
             "file" : os.path.join(dirname, 'nginx.conf')
          }
       ]
    }


def test_parse_strict():
    dirname = os.path.join(here, 'configs', 'spelling-mistake')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config, comments=True, strict=True)
    assert payload == {
        'status' : 'failed',
        'errors' : [
            {
                'file': os.path.join(dirname, 'nginx.conf'),
                'error': 'unknown directive "proxy_passs" in %s:7' % os.path.join(dirname, 'nginx.conf'),
                'line': 7
            }
        ],
        'config' : [
           {
              'file' : os.path.join(dirname, 'nginx.conf'),
              'status' : 'failed',
              'errors' : [
                  {
                     'error': 'unknown directive "proxy_passs" in %s:7' % os.path.join(dirname, 'nginx.conf'),
                     'line': 7
                  }
              ],
              'parsed' : [
                 {
                    'directive' : 'events',
                    'line' : 1,
                    'args' : [],
                    'block' : []
                 },
                 {
                    'directive' : 'http',
                    'line' : 3,
                    'args' : [],
                    'block' : [
                       {
                          'directive' : 'server',
                          'line' : 4,
                          'args' : [],
                          'block' : [
                             {
                                'directive' : 'location',
                                'line' : 5,
                                'args' : ['/'],
                                'block' : [
                                   {
                                       'directive' : '#',
                                       'line' : 6,
                                       'args' : [],
                                       'comment': 'directive is misspelled'
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


def test_parse_missing_semicolon():
    dirname = os.path.join(here, 'configs', 'missing-semicolon')

    # test correct error is raised when broken proxy_pass is in upper block
    above_config = os.path.join(dirname, 'broken-above.conf')
    above_payload = crossplane.parse(above_config)
    assert above_payload == {
        "status": "failed",
        "errors": [
            {
                "file": above_config,
                "error": "directive \"proxy_pass\" is not terminated by \";\" in %s:4" % above_config,
                "line": 4
            }
        ],
        "config": [
            {
                "file": above_config,
                "status": "failed",
                "errors": [
                    {
                        "error": "directive \"proxy_pass\" is not terminated by \";\" in %s:4" % above_config,
                        "line": 4
                    }
                ],
                "parsed": [
                    {
                        "directive": "http",
                        "line": 1,
                        "args": [],
                        "block": [
                            {
                                "directive": "server",
                                "line": 2,
                                "args": [],
                                "block": [
                                    {
                                        "directive": "location",
                                        "line": 3,
                                        "args": ["/is-broken"],
                                        "block": []
                                    },
                                    {
                                        "directive": "location",
                                        "line": 6,
                                        "args": ["/not-broken"],
                                        "block": [
                                            {
                                                "directive": "proxy_pass",
                                                "line": 7,
                                                "args": ["http://not.broken.example"]
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

    # test correct error is raised when broken proxy_pass is in lower block
    below_config = os.path.join(dirname, 'broken-below.conf')
    below_payload = crossplane.parse(below_config)
    assert below_payload == {
        "status": "failed",
        "errors": [
            {
                "file": below_config,
                "error": "directive \"proxy_pass\" is not terminated by \";\" in %s:7" % below_config,
                "line": 7
            }
        ],
        "config": [
            {
                "file": below_config,
                "status": "failed",
                "errors": [
                    {
                        "error": "directive \"proxy_pass\" is not terminated by \";\" in %s:7" % below_config,
                        "line": 7
                    }
                ],
                "parsed": [
                    {
                        "directive": "http",
                        "line": 1,
                        "args": [],
                        "block": [
                            {
                                "directive": "server",
                                "line": 2,
                                "args": [],
                                "block": [
                                    {
                                        "directive": "location",
                                        "line": 3,
                                        "args": ["/not-broken"],
                                        "block": [
                                            {
                                                "directive": "proxy_pass",
                                                "line": 4,
                                                "args": ["http://not.broken.example"]
                                            }
                                        ]
                                    },
                                    {
                                        "directive": "location",
                                        "line": 6,
                                        "args": ["/is-broken"],
                                        "block": []
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }


def test_combine_parsed_missing_values():
    dirname = os.path.join(here, 'configs', 'includes-regular')
    config = os.path.join(dirname, 'nginx.conf')
    separate = {
        "config": [
            {
                "file": "example1.conf",
                "parsed": [
                    {
                        "directive": "include",
                        "line": 1,
                        "args": ["example2.conf"],
                        "includes": [1]
                    }
                ]
            },
            {
                "file": "example2.conf",
                "parsed": [
                    {
                        "directive": "events",
                        "line": 1,
                        "args": [],
                        "block": []
                    },
                    {
                        "directive": "http",
                        "line": 2,
                        "args": [],
                        "block": []
                    }
                ]
            }
        ]
    }
    combined = crossplane.parser._combine_parsed_configs(separate)
    assert combined == {
        "status": "ok",
        "errors": [],
        "config": [
            {
                "file": "example1.conf",
                "status": "ok",
                "errors": [],
                "parsed": [
                    {
                        "directive": "events",
                        "line": 1,
                        "args": [],
                        "block": []
                    },
                    {
                        "directive": "http",
                        "line": 2,
                        "args": [],
                        "block": []
                    }
                ]
            }
        ]
    }
