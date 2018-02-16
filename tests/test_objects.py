# -*- coding: utf-8 -*-
import os
import copy

import crossplane

here = os.path.dirname(__file__)


def test_load_simple():
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    xconfig = crossplane.load(config)
    assert xconfig is not None
    assert isinstance(xconfig, crossplane.objects.CrossplaneConfig)
    assert len(xconfig.configs) == 1

    # only one file
    xconfigfile = xconfig.get(config)
    assert isinstance(xconfigfile, crossplane.objects.NginxConfigFile)
    for directive in ('events', 'http'):
        assert directive in xconfigfile
        assert len(xconfigfile.get(directive)) == 1

    events = xconfigfile.get('events')[0]
    assert isinstance(events, crossplane.objects.NginxBlockDirective)
    assert len(events.get('worker_connections')) > 0
    assert events.get('worker_connections')[0].args == ['1024']

    server = xconfigfile.get('http')[0].get('server')[0]
    assert isinstance(server, crossplane.objects.NginxBlockDirective)
    assert server.get('listen')[0].args == ['127.0.0.1:8080']
    assert server.get('server_name')[0].args == ['default_server']

    location = server.get('location')[0]
    assert isinstance(location, crossplane.objects.NginxBlockDirective)
    assert location.args == ['/']
    assert location.get('return')[0].args == ['200', 'foo bar baz']

    # some higher level primitives
    assert location.file == config

    location_ctx, ctx_parent = location.environment('server_name', 'listen')
    assert location_ctx is not None
    assert ctx_parent is not None
    # found server_name and listen from nearest parent
    assert 'default_server' in location_ctx['server_name']
    assert '127.0.0.1:8080' in location_ctx['listen']
    # ctx_parent is returned as the actual object containing the environment
    # (actual mapped object)
    assert ctx_parent == server


def test_load_build_cycle_simple(tmpdir):
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    xconfig = crossplane.load(config)

    build_config = crossplane.build(
        xconfig.to_crossplane()['config'][0]['parsed']
    )
    build_file = tmpdir.join('build1.conf')
    build_file.write(build_config)
    build_xconfig = crossplane.load(build_file.strpath)

    assert build_xconfig is not None
    assert isinstance(build_xconfig, crossplane.objects.CrossplaneConfig)
    assert len(build_xconfig.configs) == 1

    # only one file
    xconfigfile = build_xconfig.get(build_file)
    assert isinstance(xconfigfile, crossplane.objects.NginxConfigFile)
    for directive in ('events', 'http'):
        assert directive in xconfigfile
        assert len(xconfigfile.get(directive)) == 1

    events = xconfigfile.get('events')[0]
    assert isinstance(events, crossplane.objects.NginxBlockDirective)
    assert len(events.get('worker_connections')) > 0
    assert events.get('worker_connections')[0].args == ['1024']

    server = xconfigfile.get('http')[0].get('server')[0]
    assert isinstance(server, crossplane.objects.NginxBlockDirective)
    assert server.get('listen')[0].args == ['127.0.0.1:8080']
    assert server.get('server_name')[0].args == ['default_server']

    location = server.get('location')[0]
    assert isinstance(location, crossplane.objects.NginxBlockDirective)
    assert location.args == ['/']
    assert location.get('return')[0].args == ['200', 'foo bar baz']


def test_load_build_cycle_with_changes_simple(tmpdir):
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    xconfig = crossplane.load(config)
    xconfigfile = xconfig.get(config)

    # change events worker_connections
    xconfigfile.get('events')[0].get('worker_connections')[0].args = ['2048']

    build_config = crossplane.build(
        xconfig.to_crossplane()['config'][0]['parsed']
    )
    build_file = tmpdir.join('build1.conf')
    build_file.write(build_config)
    build_xconfig = crossplane.load(build_file.strpath)

    assert build_xconfig is not None
    assert isinstance(build_xconfig, crossplane.objects.CrossplaneConfig)
    assert len(build_xconfig.configs) == 1

    # only one file
    xconfigfile = build_xconfig.get(build_file)
    assert isinstance(xconfigfile, crossplane.objects.NginxConfigFile)
    for directive in ('events', 'http'):
        assert directive in xconfigfile
        assert len(xconfigfile.get(directive)) == 1

    events = xconfigfile.get('events')[0]
    assert isinstance(events, crossplane.objects.NginxBlockDirective)
    assert len(events.get('worker_connections')) > 0
    assert events.get('worker_connections')[0].args == ['2048']  # changed!

    server = xconfigfile.get('http')[0].get('server')[0]
    assert isinstance(server, crossplane.objects.NginxBlockDirective)
    assert server.get('listen')[0].args == ['127.0.0.1:8080']
    assert server.get('server_name')[0].args == ['default_server']

    location = server.get('location')[0]
    assert isinstance(location, crossplane.objects.NginxBlockDirective)
    assert location.args == ['/']
    assert location.get('return')[0].args == ['200', 'foo bar baz']


def test_eq_simple():
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    xconfig = crossplane.load(config)

    # only one file
    configfile = xconfig.get(config)
    assert configfile == copy.deepcopy(configfile)

    # block equals
    events = configfile.get('events')[0]
    assert events == crossplane.objects.NginxBlockDirective(
        directive=u'events',
        args=[],
        block=[
            {
                'directive': u'worker_connections',
                'args': [u'1024']
            }
        ]
    )
    assert events != crossplane.objects.NginxBlockDirective(
        directive=u'events',
        args=[],
        block=[
            {
                'directive': u'worker_connections',
                'args': [u'2048']
            }
        ]
    )

    # block with sub-block equals
    server = configfile.get('http')[0].get('server')[0]
    assert server == crossplane.objects.NginxBlockDirective(
        directive=u'server',
        args=[],
        block=[
            {
                'directive': u'listen',
                'args': [u'127.0.0.1:8080']
            },
            {
                'directive': u'server_name',
                'args': [u'default_server']
            },
            {
                'directive': u'location',
                'args': [u'/'],
                'block': [
                    {
                        'directive': u'return',
                        'args': [u'200', u'foo bar baz']
                    }
                ]
            }
        ]
    )
    assert server != crossplane.objects.NginxBlockDirective(
        directive=u'server',
        args=[],
        block=[
            {
                'directive': u'listen',
                'args': [u'127.0.0.1:8000']
            },
            {
                'directive': u'server_name',
                'args': [u'default_server']
            },
            {
                'directive': u'location',
                'args': [u'/'],
                'block': [
                    {
                        'directive': u'return',
                        'args': [u'200', u'foo bar baz']
                    }
                ]
            }
        ]
    )
    assert server != crossplane.objects.NginxBlockDirective(
        directive=u'server',
        args=[],
        block=[
            {
                'directive': u'listen',
                'args': [u'127.0.0.1:8080']
            },
            {
                'directive': u'server_name',
                'args': [u'default_server']
            },
            {
                'directive': u'location',
                'args': [u'/'],
                'block': [
                    {
                        'directive': u'return',
                        'args': [u'200', u'foo bar bang']
                    }
                ]
            }
        ]
    )

    # single directive equals
    listen = server.get('listen')[0]
    assert listen == crossplane.objects.NginxDirective(
        directive=u'listen',
        args=[u'127.0.0.1:8080']
    )
    assert listen != crossplane.objects.NginxDirective(
        directive=u'listen',
        args=[u'127.0.0.1:8000']
    )


def test_modify_simple():
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    xconfig = crossplane.load(config)

    # only one file
    configfile = xconfig.get(config)
    assert configfile == copy.deepcopy(configfile)

    # block equals
    events = configfile.get('events')[0]
    assert events == crossplane.objects.NginxBlockDirective(
        directive=u'events',
        args=[],
        block=[
            {
                'directive': u'worker_connections',
                'args': [u'1024']
            }
        ]
    )
    events.get('worker_connections')[0].args = u'2048'
    assert events == events
    assert events != crossplane.objects.NginxBlockDirective(
        directive=u'events',
        args=[],
        block=[
            {
                'directive': u'worker_connections',
                'args': [u'1024']
            }
        ]
    )

    # block with sub-block equals
    server = configfile.get('http')[0].get('server')[0]
    assert server == crossplane.objects.NginxBlockDirective(
        directive=u'server',
        args=[],
        block=[
            {
                'directive': u'listen',
                'args': [u'127.0.0.1:8080']
            },
            {
                'directive': u'server_name',
                'args': [u'default_server']
            },
            {
                'directive': u'location',
                'args': [u'/'],
                'block': [
                    {
                        'directive': u'return',
                        'args': [u'200', u'foo bar baz']
                    }
                ]
            }
        ]
    )
    server.get('listen')[0].args = u'127.0.0.1:8000'
    assert server == server
    assert server != crossplane.objects.NginxBlockDirective(
        directive=u'server',
        args=[],
        block=[
            {
                'directive': u'listen',
                'args': [u'127.0.0.1:8080']
            },
            {
                'directive': u'server_name',
                'args': [u'default_server']
            },
            {
                'directive': u'location',
                'args': [u'/'],
                'block': [
                    {
                        'directive': u'return',
                        'args': [u'200', u'foo bar baz']
                    }
                ]
            }
        ]
    )

    # single directive equals
    listen = server.get('listen')[0]
    assert listen == crossplane.objects.NginxDirective(
        directive=u'listen',
        args=[u'127.0.0.1:8000']  # changed from above!
    )
    listen.args = u'127.0.0.1:8080'
    assert listen == listen
    assert listen != crossplane.objects.NginxDirective(
        directive=u'listen',
        args=[u'127.0.0.1:8000']
    )


def test_modify_with_build_simple():
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    xconfig = crossplane.load(config)

    built = crossplane.build(
        xconfig.to_crossplane()['config'][0]['parsed'],
        indent=4,
        tabs=False
    )

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

    # only one file
    configfile = xconfig.get(config)

    # block equals
    events = configfile.get('events')[0]
    events.get('worker_connections')[0].args = u'2048'

    # block with sub-block equals
    server = configfile.get('http')[0].get('server')[0]
    server.get('listen')[0].args = u'127.0.0.1:8000'
    server.get('location')[0].args = '/new'

    built = crossplane.build(
        xconfig.to_crossplane()['config'][0]['parsed'],
        indent=4,
        tabs=False
    )

    assert built == '\n'.join([
        'events {',
        '    worker_connections 2048;',
        '}',
        'http {',
        '    server {',
        '        listen 127.0.0.1:8000;',
        '        server_name default_server;',
        '        location /new {',
        "            return 200 'foo bar baz';",
        '        }',
        '    }',
        '}'
    ])
