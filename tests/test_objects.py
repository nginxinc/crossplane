# -*- coding: utf-8 -*-
import os

import crossplane

here = os.path.dirname(__file__)


def test_ximport_simple():
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    xconfig = crossplane.ximport(config)
    assert xconfig is not None
    assert isinstance(xconfig, crossplane.objects.CrossplaneConfig)
    assert len(xconfig.configs) == 1

    # only one file
    xconfigfile = xconfig.get(config)
    assert isinstance(xconfigfile, crossplane.objects.NGXConfigFile)
    for directive in ('events', 'http'):
        assert directive in xconfigfile
        assert len(xconfigfile.get(directive)) == 1

    events = xconfigfile.get('events')[0]
    assert isinstance(events, crossplane.objects.NGXBlockDirective)
    assert events.worker_connections is not None
    assert events.worker_connections[0].args == ['1024']

    server = xconfigfile.http[0].server[0]
    assert isinstance(server, crossplane.objects.NGXBlockDirective)
    assert server.listen[0].args == ['127.0.0.1:8080']
    assert server.server_name[0].args == ['default_server']

    location = server.location[0]
    assert isinstance(location, crossplane.objects.NGXBlockDirective)
    assert location.args == ['/']
    assert location.get('return')[0].args == ['200', 'foo bar baz']


def test_ximport_build_cycle_simple(tmpdir):
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    xconfig = crossplane.ximport(config)

    build_config = crossplane.build(xconfig.dict()['config'][0]['parsed'])
    build_file = tmpdir.join('build1.conf')
    build_file.write(build_config)
    build_xconfig = crossplane.ximport(build_file.strpath)

    assert build_xconfig is not None
    assert isinstance(build_xconfig, crossplane.objects.CrossplaneConfig)
    assert len(build_xconfig.configs) == 1

    # only one file
    xconfigfile = build_xconfig.get(build_file)
    assert isinstance(xconfigfile, crossplane.objects.NGXConfigFile)
    for directive in ('events', 'http'):
        assert directive in xconfigfile
        assert len(xconfigfile.get(directive)) == 1

    events = xconfigfile.get('events')[0]
    assert isinstance(events, crossplane.objects.NGXBlockDirective)
    assert events.worker_connections is not None
    assert events.worker_connections[0].args == ['1024']

    server = xconfigfile.http[0].server[0]
    assert isinstance(server, crossplane.objects.NGXBlockDirective)
    assert server.listen[0].args == ['127.0.0.1:8080']
    assert server.server_name[0].args == ['default_server']

    location = server.location[0]
    assert isinstance(location, crossplane.objects.NGXBlockDirective)
    assert location.args == ['/']
    assert location.get('return')[0].args == ['200', 'foo bar baz']


def test_ximport_build_cycle_with_changes_simple(tmpdir):
    dirname = os.path.join(here, 'configs', 'simple')
    config = os.path.join(dirname, 'nginx.conf')

    xconfig = crossplane.ximport(config)
    xconfigfile = xconfig.get(config)

    # change events worker_connections
    xconfigfile.get('events')[0].worker_connections[0].args = ['2048']

    build_config = crossplane.build(xconfig.dict()['config'][0]['parsed'])
    build_file = tmpdir.join('build1.conf')
    build_file.write(build_config)
    build_xconfig = crossplane.ximport(build_file.strpath)

    assert build_xconfig is not None
    assert isinstance(build_xconfig, crossplane.objects.CrossplaneConfig)
    assert len(build_xconfig.configs) == 1

    # only one file
    xconfigfile = build_xconfig.get(build_file)
    assert isinstance(xconfigfile, crossplane.objects.NGXConfigFile)
    for directive in ('events', 'http'):
        assert directive in xconfigfile
        assert len(xconfigfile.get(directive)) == 1

    events = xconfigfile.get('events')[0]
    assert isinstance(events, crossplane.objects.NGXBlockDirective)
    assert events.worker_connections is not None
    assert events.worker_connections[0].args == ['2048']  # changed!

    server = xconfigfile.http[0].server[0]
    assert isinstance(server, crossplane.objects.NGXBlockDirective)
    assert server.listen[0].args == ['127.0.0.1:8080']
    assert server.server_name[0].args == ['default_server']

    location = server.location[0]
    assert isinstance(location, crossplane.objects.NGXBlockDirective)
    assert location.args == ['/']
    assert location.get('return')[0].args == ['200', 'foo bar baz']
