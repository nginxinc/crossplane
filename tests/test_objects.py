# -*- coding: utf-8 -*-
import os

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
    assert location.location == (config, 9)

    location_ctx, ctx_parent = location.context('server_name', 'listen')
    assert location_ctx is not None
    assert ctx_parent is not None
    # found server_name and listen from nearest parent
    assert 'default_server' in location_ctx['server_name']
    assert '127.0.0.1:8080' in location_ctx['listen']
    # ctx_parent is returned as the actual object containing the context
    # (actual mapped object)
    assert ctx_parent == server


def test_load_build_cycle_simple(tmpdir):
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    xconfig = crossplane.load(config)

    build_config = crossplane.build(xconfig.dict()['config'][0]['parsed'])
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

    build_config = crossplane.build(xconfig.dict()['config'][0]['parsed'])
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
