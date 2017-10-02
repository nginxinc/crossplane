# -*- coding: utf-8 -*-
import os

from nginx_conf.parse import parse_file


def test_relative_includes():
    here = os.path.dirname(__file__)
    dirname = os.path.join(here, 'configs', 'relative-includes')
    config = os.path.join(dirname, 'nginx.conf')
    payload = parse_file(config)
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
                        'includes': [
                            os.path.join(dirname, 'http.conf')
                        ]
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
                                'includes': [
                                    os.path.join(dirname, 'servers', 'server1.conf'),
                                    os.path.join(dirname, 'servers', 'server2.conf')
                                ]
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
                                'includes': [
                                    os.path.join(dirname, 'locations', 'location1.conf'),
                                    os.path.join(dirname, 'locations', 'location2.conf')
                                ]
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
                                'includes': [
                                    os.path.join(dirname, 'locations', 'location1.conf'),
                                    os.path.join(dirname, 'locations', 'location2.conf')
                                ]
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
