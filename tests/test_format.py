# -*- coding: utf-8 -*-
import os

import crossplane
from . import here


def test_format_messy_config():
    dirname = os.path.join(here, 'configs', 'messy')
    config = os.path.join(dirname, 'nginx.conf')
    output = crossplane.format(config)
    assert output == '\n'.join([
        'user nobody;',
        'events {',
        '    worker_connections 2048;',
        '}',
        'http {',
        '    access_log off;',
        '    default_type text/plain;',
        '    error_log off;',
        '    server {',
        '        listen 8083;',
        r"""        return 200 'Ser" \' \' ver\\ \ $server_addr:\$server_port\n\nTime: $time_local\n\n';""",
        '    }',
        '    server {',
        '        listen 8080;',
        '        root /usr/share/nginx/html;',
        "        location ~ '/hello/world;' {",
        '            return 301 /status.html;',
        '        }',
        '        location /foo {',
        '        }',
        '        location /bar {',
        '        }',
        '        location /\{\;\}\ #\ ab {',
        '        }',
        '        if ($request_method = P\{O\)\###\;ST) {',
        '        }',
        '        location /status.html {',
        "            try_files '/abc/${uri} /abc/${uri}.html' =404;",
        '        }',
        r"        location '/sta;\n                    tus' {",
        '            return 302 /status.html;',
        '        }',
        '        location /upstream_conf {',
        '            return 200 /status.html;',
        '        }',
        '    }',
        '    server {',
        '    }',
        '}'
    ])


def test_format_not_main_file():
    dirname = os.path.join(here, 'configs', 'includes-globbed', 'servers')
    config = os.path.join(dirname, 'server1.conf')
    output = crossplane.format(config)
    assert output == '\n'.join([
        'server {',
        '    listen 8080;',
        '    include locations/*.conf;',
        '}'
    ])


def test_format_args_not_analyzed():
    dirname = os.path.join(here, 'configs', 'bad-args')
    config = os.path.join(dirname, 'nginx.conf')
    output = crossplane.format(config)
    assert output == '\n'.join([
        'user;',
        'events {',
        '}',
        'http {',
        '}'
    ])
