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


def test_parse_string_simple_matches_file():
    dirname = os.path.join(here, 'configs', 'simple')
    config_path = os.path.join(dirname, 'nginx.conf')
    with open(config_path, 'r') as f:
        text = f.read()
    payload_file = crossplane.parse(config_path)
    payload_string = crossplane.parse_string(text, filename=config_path)
    assert payload_file == payload_string


def test_parse_string_includes_regular_matches_file():
    dirname = os.path.join(here, 'configs', 'includes-regular')
    config_path = os.path.join(dirname, 'nginx.conf')
    with open(config_path, 'r') as f:
        text = f.read()
    payload_file = crossplane.parse(config_path)
    payload_string = crossplane.parse_string(text, filename=config_path)
    assert payload_file == payload_string


def test_parse_string_includes_globbed_combined_matches_file():
    dirname = os.path.join(here, 'configs', 'includes-globbed')
    config_path = os.path.join(dirname, 'nginx.conf')
    with open(config_path, 'r') as f:
        text = f.read()
    payload_file = crossplane.parse(config_path, combine=True)
    payload_string = crossplane.parse_string(text, filename=config_path, combine=True)
    assert payload_file == payload_string


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
             "file" : config
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


def test_parse_string_unterminated_directive_at_eof(tmp_path):
    filename = str(tmp_path / 'nginx.conf')
    payload = crossplane.parse_string('user nobody', filename=filename)
    assert payload['status'] == 'failed'
    assert payload['errors'] == [
        {
            'file': filename,
            'error': 'directive "user" is not terminated by ";" in %s:1' % filename,
            'line': 1
        }
    ]


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


def test_comments_between_args():
    dirname = os.path.join(here, 'configs', 'comments-between-args')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config, comments=True)
    assert payload == {
        'status': 'ok',
        'errors': [],
        'config': [
            {
                'file': config,
                'status': 'ok',
                'errors': [],
                'parsed': [
                    {
                        'directive': 'http',
                        'line': 1,
                        'args': [],
                        'block': [
                            {
                                'directive': '#',
                                'line': 1,
                                'args': [],
                                'comment': 'comment 1'
                            },
                            {
                                'directive': 'log_format',
                                'line': 2,
                                'args': ['\\#arg\\ 1', '#arg 2']
                            },
                            {
                                'directive': '#',
                                'line': 2,
                                'args': [],
                                'comment': 'comment 2'
                            },
                            {
                                'directive': '#',
                                'line': 2,
                                'args': [],
                                'comment': 'comment 3'
                            },
                            {
                                'directive': '#',
                                'line': 2,
                                'args': [],
                                'comment': 'comment 4'
                            },
                            {
                                'directive': '#',
                                'line': 2,
                                'args': [],
                                'comment': 'comment 5'
                            }
                        ]
                    }
                ]
            }
        ]
    }

def test_non_unicode():
    dirname = os.path.join(here, 'configs', 'non-unicode')
    config = os.path.join(dirname, 'nginx.conf')

    payload = crossplane.parse(config, comments=True)

    assert payload == {
        "errors": [],
        "status": "ok",
        "config": [
            {
                "status": "ok",
                "errors": [],
                "file": os.path.join(dirname, 'nginx.conf'),
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
                                        "args": [
                                            "/city"
                                        ],
                                        "block": [
                                            {
                                                "directive": "#",
                                                "line": 4,
                                                "args": [],
                                                "comment": u" M\ufffdlln"
                                            },
                                            {
                                                "directive": "return",
                                                "line": 5,
                                                "args": [
                                                    "200",
                                                    u"M\ufffdlln\\n"
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
        ]
    }


def test_includes_regular_combined():
    """Test that directives after includes have correct file attribute when combine=True.

    This tests for a variable scope leak bug where the `fname` loop variable in the
    include-handling block would shadow the outer `fname`, causing directives after
    includes to have incorrect `file` attributes.
    """
    dirname = os.path.join(here, 'configs', 'includes-regular-combined')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config, combine=True)
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
                        'file': os.path.join(dirname, 'nginx.conf'),
                        'line': 1,
                        'args': [],
                        'block': []
                    },
                    {
                        'directive': 'http',
                        'file': os.path.join(dirname, 'nginx.conf'),
                        'line': 2,
                        'args': [],
                        'block': [
                            {
                                'directive': 'server',
                                'file': os.path.join(dirname, 'server.conf'),
                                'line': 1,
                                'args': [],
                                'block': [
                                    {
                                        'directive': 'listen',
                                        'file': os.path.join(dirname, 'server.conf'),
                                        'line': 2,
                                        'args': ['8080']
                                    }
                                ]
                            },
                            {
                                'directive': 'default_type',
                                'file': os.path.join(dirname, 'nginx.conf'),
                                'line': 4,
                                'args': ['text/plain']
                            }
                        ]
                    }
                ]
            }
        ]
    }


def test_parse_map_strict():
    """Test that map blocks parse correctly in strict mode."""
    dirname = os.path.join(here, 'configs', 'map')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config, strict=True)
    assert payload['status'] == 'ok'
    assert payload['errors'] == []

    # verify the structure
    http_block = payload['config'][0]['parsed'][1]
    assert http_block['directive'] == 'http'

    # check first map block
    map1 = http_block['block'][0]
    assert map1['directive'] == 'map'
    assert map1['args'] == ['$uri', '$new']
    assert len(map1['block']) == 3  # default, ~^/news, ~^/blog

    # check second map block has hostnames
    map2 = http_block['block'][1]
    assert map2['directive'] == 'map'
    assert map2['args'] == ['$http_host', '$backend']
    assert len(map2['block']) == 3  # hostnames, default, *.example.com


def test_parse_types_strict():
    """Test that types blocks parse correctly in strict mode."""
    dirname = os.path.join(here, 'configs', 'types')
    config = os.path.join(dirname, 'nginx.conf')
    payload = crossplane.parse(config, strict=True)
    assert payload['status'] == 'ok'
    assert payload['errors'] == []

    # verify the structure
    http_block = payload['config'][0]['parsed'][1]
    assert http_block['directive'] == 'http'

    # check types block
    types_block = http_block['block'][0]
    assert types_block['directive'] == 'types'
    assert len(types_block['block']) == 4  # text/html, text/css, application/javascript, image/png

    # verify some MIME type entries
    mime_entries = {stmt['directive']: stmt['args'] for stmt in types_block['block']}
    assert mime_entries['text/html'] == ['html', 'htm']
    assert mime_entries['text/css'] == ['css']
