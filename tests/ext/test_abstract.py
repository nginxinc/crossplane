# -*- coding: utf-8 -*-
"""Tests for crossplane extension base class (ext/abstract.py)."""
import pytest

from crossplane.ext.abstract import CrossplaneExtension


class TestCrossplaneExtension:
    """Tests for the CrossplaneExtension base class."""

    def test_directives_default_empty(self):
        """Test that default directives dictionary is empty."""
        ext = CrossplaneExtension()
        assert ext.directives == {}

    def test_lex_raises_not_implemented(self):
        """Test that lex raises NotImplementedError."""
        ext = CrossplaneExtension()
        with pytest.raises(NotImplementedError):
            ext.lex(iter([]), 'some_directive')

    def test_parse_raises_not_implemented(self):
        """Test that parse raises NotImplementedError."""
        ext = CrossplaneExtension()
        stmt = {'directive': 'test', 'args': [], 'line': 1}
        parsing = {'file': 'test.conf', 'status': 'ok', 'errors': [], 'parsed': []}
        with pytest.raises(NotImplementedError):
            ext.parse(stmt, parsing, iter([]), ctx=(), consume=False)

    def test_build_raises_not_implemented(self):
        """Test that build raises NotImplementedError."""
        ext = CrossplaneExtension()
        stmt = {'directive': 'test', 'args': [], 'line': 1}
        with pytest.raises(NotImplementedError):
            ext.build(stmt, padding='    ', state={}, indent=4, tabs=False)


class TestCustomExtension:
    """Tests for custom extension subclassing."""

    def test_custom_extension_can_subclass(self):
        """Test that CrossplaneExtension can be properly subclassed."""
        class CustomExtension(CrossplaneExtension):
            directives = {
                'custom_directive': [],
            }

            def lex(self, token_iterator, directive):
                return iter([('token', 1, False)])

            def parse(self, stmt, parsing, tokens, ctx=(), consume=False):
                return stmt

            def build(self, stmt, padding, state=None, indent=4, tabs=False):
                return 'custom_directive;'

        ext = CustomExtension()
        assert 'custom_directive' in ext.directives
        assert list(ext.lex(iter([]), 'custom_directive')) == [('token', 1, False)]
        assert ext.parse({}, {}, iter([])) == {}
        assert ext.build({}, '', {}) == 'custom_directive;'

    def test_custom_extension_with_multiple_directives(self):
        """Test custom extension with multiple directives."""
        class MultiDirectiveExtension(CrossplaneExtension):
            directives = {
                'directive_a': ['context1'],
                'directive_b': ['context2'],
                'directive_c': [],
            }

            def lex(self, token_iterator, directive):
                raise NotImplementedError

            def parse(self, stmt, parsing, tokens, ctx=(), consume=False):
                raise NotImplementedError

            def build(self, stmt, padding, state, indent=4, tabs=False):
                raise NotImplementedError

        ext = MultiDirectiveExtension()
        assert len(ext.directives) == 3
        assert 'directive_a' in ext.directives
        assert 'directive_b' in ext.directives
        assert 'directive_c' in ext.directives

    def test_extension_directives_isolation(self):
        """Test that different extension instances don't share directives."""
        class ExtA(CrossplaneExtension):
            directives = {'ext_a_dir': []}

            def lex(self, token_iterator, directive):
                raise NotImplementedError

            def parse(self, stmt, parsing, tokens, ctx=(), consume=False):
                raise NotImplementedError

            def build(self, stmt, padding, state, indent=4, tabs=False):
                raise NotImplementedError

        class ExtB(CrossplaneExtension):
            directives = {'ext_b_dir': []}

            def lex(self, token_iterator, directive):
                raise NotImplementedError

            def parse(self, stmt, parsing, tokens, ctx=(), consume=False):
                raise NotImplementedError

            def build(self, stmt, padding, state, indent=4, tabs=False):
                raise NotImplementedError

        ext_a = ExtA()
        ext_b = ExtB()

        assert 'ext_a_dir' in ext_a.directives
        assert 'ext_b_dir' not in ext_a.directives
        assert 'ext_b_dir' in ext_b.directives
        assert 'ext_a_dir' not in ext_b.directives
