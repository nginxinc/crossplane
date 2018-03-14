# -*- coding: utf-8 -*-
import crossplane


def test_state_directive():
    fname = '/path/to/nginx.conf'

    stmt = {
        'directive': 'state',
        'args': ['/path/to/state/file.conf'],
        'line': 5  # this is arbitrary
    }

    # the state directive should not cause errors if it's in these contexts
    good_contexts = set([
        ('http', 'upstream'),
        ('stream', 'upstream'),
        ('some_third_party_context',)
    ])

    for ctx in good_contexts:
        crossplane.analyzer.analyze(fname, stmt, term=';', ctx=ctx)

    # the state directive should not be in any of these contexts
    bad_contexts = set(crossplane.analyzer.CONTEXTS) - good_contexts

    for ctx in bad_contexts:
        try:
            crossplane.analyzer.analyze(fname, stmt, term=';', ctx=ctx)
            raise Exception("bad context for 'state' passed: " + repr(ctx))
        except crossplane.errors.NgxParserDirectiveContextError:
            continue


def test_flag_directive_args():
    fname = '/path/to/nginx.conf'
    ctx = ('events',)

    # an NGINX_CONF_FLAG directive
    stmt = {
        'directive': 'accept_mutex',
        'line': 2  # this is arbitrary
    }

    good_args = [['on'], ['off'], ['On'], ['Off'], ['ON'], ['OFF']]

    for args in good_args:
        stmt['args'] = args
        crossplane.analyzer.analyze(fname, stmt, term=';', ctx=ctx)

    bad_args = [['1'], ['0'], ['true'], ['okay'], ['']]

    for args in bad_args:
        stmt['args'] = args
        try:
            crossplane.analyzer.analyze(fname, stmt, term=';', ctx=ctx)
            raise Exception('bad args for flag directive: ' + repr(args))
        except crossplane.errors.NgxParserDirectiveArgumentsError as e:
            assert e.strerror.endswith('it must be "on" or "off"')
