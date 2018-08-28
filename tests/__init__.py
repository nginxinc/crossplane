# -*- coding: utf-8 -*-
import os

from crossplane.compat import basestring
from crossplane.parser import parse
from crossplane.builder import build, _enquote

here = os.path.dirname(__file__)


def assert_equal_payloads(a, b, ignore_keys=()):
    assert type(a) == type(b)
    if isinstance(a, list):
        assert len(a) == len(b)
        for args in zip(a, b):
            assert_equal_payloads(*args, ignore_keys=ignore_keys)
    elif isinstance(a, dict):
        keys = set(a.keys()) | set(b.keys())
        keys.difference_update(ignore_keys)
        for key in keys:
            assert_equal_payloads(a[key], b[key], ignore_keys=ignore_keys)
    elif isinstance(a, basestring):
        assert _enquote(a) == _enquote(b)
    else:
        assert a == b


def compare_parsed_and_built(conf_dirname, conf_basename, tmpdir, **kwargs):
    original_dirname = os.path.join(here, 'configs', conf_dirname)
    original_path = os.path.join(original_dirname, conf_basename)
    original_payload = parse(original_path, **kwargs)
    original_parsed = original_payload['config'][0]['parsed']

    build1_config = build(original_parsed)
    build1_file = tmpdir.join('build1.conf')
    build1_file.write_text(build1_config, encoding='utf-8')
    build1_payload = parse(build1_file.strpath, **kwargs)
    build1_parsed = build1_payload['config'][0]['parsed']

    assert_equal_payloads(original_parsed, build1_parsed, ignore_keys=['line'])

    build2_config = build(build1_parsed)
    build2_file = tmpdir.join('build2.conf')
    build2_file.write_text(build2_config, encoding='utf-8')
    build2_payload = parse(build2_file.strpath, **kwargs)
    build2_parsed = build2_payload['config'][0]['parsed']

    assert build1_config == build2_config
    assert_equal_payloads(build1_parsed, build2_parsed, ignore_keys=[])
