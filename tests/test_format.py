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
        r'# hello\n\\n\\\n worlddd  \#\\#\\\# dfsf\n \\n \\\n ',
        'events {',
        '    worker_connections 2048;',
        '}',
        'http { #forteen',
        '    # this is a comment',
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
        '        } # hello',
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


def test_format_align_option():
    dirname = os.path.join(here, 'configs', 'many-directives')
    config = os.path.join(dirname, 'nginx.conf')
    output = crossplane.format(config, align=True)
    assert output == '\n'.join([
        'server {',
        '    listen              443 ssl;',
        '    ssl_certificate     fullchain.pem;',
        '    ssl_certificate_key privite.pem;',
        '    server_name         _;',
        '    index               index.html;',
        '    root                /public;',
        '    charset             utf-8;',
        '    expires             $expires;',
        '}',
    ])


def test_format_just_spacious_option():
    dirname = os.path.join(here, 'configs', 'many-directives')
    config = os.path.join(dirname, 'with-blocks.conf')
    output = crossplane.format(config, spacious=True)
    assert output == '\n'.join([
        'server {',
        '    location ~ \d {',
        '        image_filter_buffer 5M;',
        '        image_filter_interlace on;',
        '        image_filter_jpeg_quality 75;',
        '    }',
        '',
        '    location ~ \d {',
        '        image_filter_buffer 5M;',
        '        image_filter_interlace on;',
        '        image_filter_jpeg_quality 75;',
        '    }',
        '}',
    ])


def test_format_spacious_option_with_align():
    dirname = os.path.join(here, 'configs', 'many-directives')
    config = os.path.join(dirname, 'with-blocks.conf')
    output = crossplane.format(config, align=True, spacious=True)
    assert output == '\n'.join([
        'server {',
        '    location ~ \d {',
        '        image_filter_buffer       5M;',
        '        image_filter_interlace    on;',
        '        image_filter_jpeg_quality 75;',
        '    }',
        '',
        '    location ~ \d {',
        '        image_filter_buffer       5M;',
        '        image_filter_interlace    on;',
        '        image_filter_jpeg_quality 75;',
        '    }',
        '}',
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


def test_format_with_comments():
    dirname = os.path.join(here, 'configs', 'with-comments')
    config = os.path.join(dirname, 'nginx.conf')
    output = crossplane.format(config)
    assert output == '\n'.join([
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
        "            return 200 'foo bar baz';",
        '        }',
        '    }',
        '}'
    ])
