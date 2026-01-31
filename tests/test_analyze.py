# -*- coding: utf-8 -*-
import pytest

import crossplane
from crossplane.analyzer import (
    DIRECTIVES,
    CONTEXTS,
    enter_block_ctx,
    analyze,
    NGX_CONF_NOARGS,
    NGX_CONF_TAKE1,
    NGX_CONF_1MORE,
    NGX_CONF_BLOCK,
)
from crossplane.errors import (
    NgxParserDirectiveUnknownError,
    NgxParserDirectiveContextError,
    NgxParserDirectiveArgumentsError,
)


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


def test_map_freeform_directives():
    """Test that arbitrary directives are allowed inside map blocks."""
    fname = '/path/to/nginx.conf'
    ctx = ('http', 'map')

    # test various map entries that would fail if treated as regular directives
    freeform_stmts = [
        {'directive': 'default', 'args': ['0'], 'line': 1},
        {'directive': '~^/news', 'args': ['1'], 'line': 2},
        {'directive': '*.example.com', 'args': ['backend1'], 'line': 3},
        {'directive': 'hostnames', 'args': [], 'line': 4},
        {'directive': '/api', 'args': ['api_backend'], 'line': 5},
    ]

    for stmt in freeform_stmts:
        # should not raise any errors even in strict mode
        crossplane.analyzer.analyze(fname, stmt, term=';', ctx=ctx, strict=True)


def test_types_freeform_directives():
    """Test that arbitrary MIME type directives are allowed inside types blocks."""
    fname = '/path/to/nginx.conf'
    ctx = ('http', 'types')

    # test various types entries that would fail if treated as regular directives
    freeform_stmts = [
        {'directive': 'text/html', 'args': ['html', 'htm'], 'line': 1},
        {'directive': 'text/css', 'args': ['css'], 'line': 2},
        {'directive': 'application/javascript', 'args': ['js'], 'line': 3},
        {'directive': 'image/png', 'args': ['png'], 'line': 4},
    ]

    for stmt in freeform_stmts:
        # should not raise any errors even in strict mode
        crossplane.analyzer.analyze(fname, stmt, term=';', ctx=ctx, strict=True)


def test_geo_freeform_directives():
    """Test that arbitrary directives are allowed inside geo blocks."""
    fname = '/path/to/nginx.conf'
    ctx = ('http', 'geo')

    freeform_stmts = [
        {'directive': 'default', 'args': ['0'], 'line': 1},
        {'directive': '127.0.0.1', 'args': ['1'], 'line': 2},
        {'directive': '10.0.0.0/8', 'args': ['internal'], 'line': 3},
    ]

    for stmt in freeform_stmts:
        crossplane.analyzer.analyze(fname, stmt, term=';', ctx=ctx, strict=True)


def test_charset_map_freeform_directives():
    """Test that arbitrary directives are allowed inside charset_map blocks."""
    fname = '/path/to/nginx.conf'
    ctx = ('http', 'charset_map')

    freeform_stmts = [
        {'directive': '2F', 'args': ['/', '%2F'], 'line': 1},  # hex code mappings
    ]

    for stmt in freeform_stmts:
        crossplane.analyzer.analyze(fname, stmt, term=';', ctx=ctx, strict=True)


class TestNoargsDirective:
    """Tests for NGX_CONF_NOARGS directives."""

    def test_noargs_directive_accepts_zero_args(self):
        """Test that NOARGS directive accepts zero arguments."""
        fname = '/path/to/nginx.conf'
        ctx = ('http', 'server', 'if')  # context where 'break' is allowed
        stmt = {'directive': 'break', 'args': [], 'line': 1}
        # Should not raise
        analyze(fname, stmt, term=';', ctx=ctx)

    def test_noargs_directive_rejects_args(self):
        """Test that NOARGS directive rejects arguments."""
        fname = '/path/to/nginx.conf'
        ctx = ('http', 'server', 'if')
        stmt = {'directive': 'break', 'args': ['unexpected'], 'line': 1}
        with pytest.raises(NgxParserDirectiveArgumentsError):
            analyze(fname, stmt, term=';', ctx=ctx)


class TestTake1Directive:
    """Tests for NGX_CONF_TAKE1 directives."""

    def test_take1_directive_accepts_one_arg(self):
        """Test that TAKE1 directive accepts exactly one argument."""
        fname = '/path/to/nginx.conf'
        ctx = ('http', 'server')
        stmt = {'directive': 'server_name', 'args': ['example.com'], 'line': 1}
        # Should not raise
        analyze(fname, stmt, term=';', ctx=ctx)

    def test_take1_directive_rejects_zero_args(self):
        """Test that TAKE1 directive rejects zero arguments."""
        fname = '/path/to/nginx.conf'
        ctx = ('http', 'server')
        stmt = {'directive': 'server_name', 'args': [], 'line': 1}
        with pytest.raises(NgxParserDirectiveArgumentsError):
            analyze(fname, stmt, term=';', ctx=ctx)


class Test1MoreDirective:
    """Tests for NGX_CONF_1MORE directives."""

    def test_1more_directive_accepts_one_arg(self):
        """Test that 1MORE directive accepts one argument."""
        fname = '/path/to/nginx.conf'
        ctx = ('http',)
        stmt = {'directive': 'index', 'args': ['index.html'], 'line': 1}
        analyze(fname, stmt, term=';', ctx=ctx)

    def test_1more_directive_accepts_multiple_args(self):
        """Test that 1MORE directive accepts multiple arguments."""
        fname = '/path/to/nginx.conf'
        ctx = ('http',)
        stmt = {'directive': 'index', 'args': ['index.html', 'index.htm', 'default.html'], 'line': 1}
        analyze(fname, stmt, term=';', ctx=ctx)

    def test_1more_directive_rejects_zero_args(self):
        """Test that 1MORE directive rejects zero arguments."""
        fname = '/path/to/nginx.conf'
        ctx = ('http',)
        stmt = {'directive': 'index', 'args': [], 'line': 1}
        with pytest.raises(NgxParserDirectiveArgumentsError):
            analyze(fname, stmt, term=';', ctx=ctx)


class TestStrictMode:
    """Tests for strict mode behavior."""

    def test_unknown_directive_raises_in_strict_mode(self):
        """Test that unknown directive raises error in strict mode."""
        fname = '/path/to/nginx.conf'
        ctx = ('http',)
        stmt = {'directive': 'completely_unknown_directive', 'args': [], 'line': 1}
        with pytest.raises(NgxParserDirectiveUnknownError) as exc_info:
            analyze(fname, stmt, term=';', ctx=ctx, strict=True)
        assert 'unknown directive' in exc_info.value.strerror

    def test_unknown_directive_ignored_in_non_strict_mode(self):
        """Test that unknown directive is ignored in non-strict mode."""
        fname = '/path/to/nginx.conf'
        ctx = ('http',)
        stmt = {'directive': 'completely_unknown_directive', 'args': [], 'line': 1}
        # Should not raise in non-strict mode
        analyze(fname, stmt, term=';', ctx=ctx, strict=False)


class TestBlockDirectives:
    """Tests for block directive handling."""

    def test_block_directive_requires_brace(self):
        """Test that block directive requires opening brace."""
        fname = '/path/to/nginx.conf'
        ctx = ()
        stmt = {'directive': 'http', 'args': [], 'line': 1}
        with pytest.raises(NgxParserDirectiveArgumentsError) as exc_info:
            analyze(fname, stmt, term=';', ctx=ctx)
        assert 'has no opening "{"' in exc_info.value.strerror

    def test_block_directive_accepts_brace(self):
        """Test that block directive accepts opening brace."""
        fname = '/path/to/nginx.conf'
        ctx = ()
        stmt = {'directive': 'http', 'args': [], 'line': 1}
        # Should not raise
        analyze(fname, stmt, term='{', ctx=ctx)

    def test_non_block_directive_rejects_brace(self):
        """Test that non-block directive rejects opening brace."""
        fname = '/path/to/nginx.conf'
        ctx = ('http', 'server')
        stmt = {'directive': 'listen', 'args': ['80'], 'line': 1}
        with pytest.raises(NgxParserDirectiveArgumentsError) as exc_info:
            analyze(fname, stmt, term='{', ctx=ctx)
        assert 'is not terminated by ";"' in exc_info.value.strerror


class TestEnterBlockCtx:
    """Tests for enter_block_ctx function."""

    def test_http_location_nesting(self):
        """Test that location blocks in http context are flattened."""
        stmt = {'directive': 'location', 'args': ['/'], 'line': 1}
        ctx = ('http', 'server')
        result = enter_block_ctx(stmt, ctx)
        # Location blocks don't nest - they should just be ('http', 'location')
        assert result == ('http', 'location')

    def test_nested_location_in_location(self):
        """Test that nested location also returns ('http', 'location')."""
        stmt = {'directive': 'location', 'args': ['/api'], 'line': 1}
        ctx = ('http', 'location')
        result = enter_block_ctx(stmt, ctx)
        assert result == ('http', 'location')

    def test_non_location_block_appends(self):
        """Test that non-location blocks are appended to context."""
        stmt = {'directive': 'server', 'args': [], 'line': 1}
        ctx = ('http',)
        result = enter_block_ctx(stmt, ctx)
        assert result == ('http', 'server')

    def test_empty_context(self):
        """Test entering block from empty context."""
        stmt = {'directive': 'http', 'args': [], 'line': 1}
        ctx = ()
        result = enter_block_ctx(stmt, ctx)
        assert result == ('http',)


class TestDirectivesDatabase:
    """Tests for DIRECTIVES dictionary integrity."""

    def test_directives_contains_common_directives(self):
        """Spot-check that common directives exist in the database."""
        common_directives = [
            'http', 'server', 'location', 'listen', 'root',
            'index', 'return', 'if', 'proxy_pass', 'upstream',
            'events', 'worker_processes', 'error_log', 'access_log'
        ]
        for directive in common_directives:
            assert directive in DIRECTIVES, f"Missing directive: {directive}"

    def test_contexts_dictionary_keys(self):
        """Test that CONTEXTS has expected context tuples."""
        expected_contexts = [
            (),
            ('events',),
            ('http',),
            ('http', 'server'),
            ('http', 'location'),
            ('http', 'upstream'),
        ]
        for ctx in expected_contexts:
            assert ctx in CONTEXTS, f"Missing context: {ctx}"


class TestContextValidation:
    """Tests for directive context validation."""

    def test_directive_wrong_context(self):
        """Test that directive in wrong context raises error."""
        fname = '/path/to/nginx.conf'
        # 'listen' is valid in http>server but not in http directly
        stmt = {'directive': 'listen', 'args': ['80'], 'line': 1}
        ctx = ('http',)
        with pytest.raises(NgxParserDirectiveContextError) as exc_info:
            analyze(fname, stmt, term=';', ctx=ctx)
        assert 'is not allowed here' in exc_info.value.strerror

    def test_directive_correct_context(self):
        """Test that directive in correct context passes."""
        fname = '/path/to/nginx.conf'
        stmt = {'directive': 'listen', 'args': ['80'], 'line': 1}
        ctx = ('http', 'server')
        # Should not raise
        analyze(fname, stmt, term=';', ctx=ctx)

    def test_check_ctx_disabled(self):
        """Test that context checking can be disabled."""
        fname = '/path/to/nginx.conf'
        # 'listen' in wrong context, but check_ctx=False
        stmt = {'directive': 'listen', 'args': ['80'], 'line': 1}
        ctx = ('http',)
        # Should not raise when check_ctx=False
        analyze(fname, stmt, term=';', ctx=ctx, check_ctx=False)

    def test_check_args_disabled(self):
        """Test that argument checking can be disabled."""
        fname = '/path/to/nginx.conf'
        stmt = {'directive': 'listen', 'args': [], 'line': 1}  # Missing required arg
        ctx = ('http', 'server')
        # Should not raise when check_args=False
        analyze(fname, stmt, term=';', ctx=ctx, check_args=False)
