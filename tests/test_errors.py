# -*- coding: utf-8 -*-
"""Tests for crossplane exception classes (errors.py)."""
import pytest

from crossplane.errors import (
    NgxParserBaseException,
    NgxParserSyntaxError,
    NgxParserDirectiveError,
    NgxParserDirectiveArgumentsError,
    NgxParserDirectiveContextError,
    NgxParserDirectiveUnknownError,
)


class TestNgxParserBaseException:
    """Tests for the base exception class."""

    def test_str_with_lineno(self):
        """Test string representation with line number."""
        exc = NgxParserBaseException(
            strerror='unexpected character',
            filename='/etc/nginx/nginx.conf',
            lineno=42
        )
        result = str(exc)
        assert result == 'unexpected character in /etc/nginx/nginx.conf:42'

    def test_str_without_lineno(self):
        """Test string representation without line number.

        Note: There is a known issue in the error class where lineno=None
        causes a TypeError due to format string mismatch. This test documents
        the current behavior.
        """
        exc = NgxParserBaseException(
            strerror='file not found',
            filename='/etc/nginx/nginx.conf',
            lineno=None
        )
        # The current implementation has a bug: args is a 3-tuple but
        # the format string for lineno=None only has 2 placeholders.
        # This test documents the bug rather than the intended behavior.
        with pytest.raises(TypeError):
            str(exc)

    def test_attributes(self):
        """Test that exception attributes are set correctly."""
        exc = NgxParserBaseException(
            strerror='test error',
            filename='/path/to/file.conf',
            lineno=10
        )
        assert exc.strerror == 'test error'
        assert exc.filename == '/path/to/file.conf'
        assert exc.lineno == 10
        assert exc.args == ('test error', '/path/to/file.conf', 10)

    def test_args_tuple(self):
        """Test that args tuple is properly set for exception chaining."""
        exc = NgxParserBaseException(
            strerror='error message',
            filename='config.conf',
            lineno=5
        )
        assert len(exc.args) == 3
        assert exc.args[0] == 'error message'
        assert exc.args[1] == 'config.conf'
        assert exc.args[2] == 5


class TestExceptionInheritance:
    """Tests for exception class hierarchy."""

    def test_syntax_error_inheritance(self):
        """Test NgxParserSyntaxError inherits from base."""
        exc = NgxParserSyntaxError('syntax error', 'file.conf', 1)
        assert isinstance(exc, NgxParserBaseException)
        assert isinstance(exc, Exception)

    def test_directive_error_inheritance(self):
        """Test NgxParserDirectiveError inherits from base."""
        exc = NgxParserDirectiveError('directive error', 'file.conf', 1)
        assert isinstance(exc, NgxParserBaseException)
        assert isinstance(exc, Exception)

    def test_arguments_error_inheritance(self):
        """Test NgxParserDirectiveArgumentsError inherits from DirectiveError."""
        exc = NgxParserDirectiveArgumentsError('args error', 'file.conf', 1)
        assert isinstance(exc, NgxParserDirectiveError)
        assert isinstance(exc, NgxParserBaseException)
        assert isinstance(exc, Exception)

    def test_context_error_inheritance(self):
        """Test NgxParserDirectiveContextError inherits from DirectiveError."""
        exc = NgxParserDirectiveContextError('context error', 'file.conf', 1)
        assert isinstance(exc, NgxParserDirectiveError)
        assert isinstance(exc, NgxParserBaseException)
        assert isinstance(exc, Exception)

    def test_unknown_error_inheritance(self):
        """Test NgxParserDirectiveUnknownError inherits from DirectiveError."""
        exc = NgxParserDirectiveUnknownError('unknown directive', 'file.conf', 1)
        assert isinstance(exc, NgxParserDirectiveError)
        assert isinstance(exc, NgxParserBaseException)
        assert isinstance(exc, Exception)


class TestExceptionCatching:
    """Tests for exception catching behavior."""

    def test_catching_base_catches_syntax_error(self):
        """Test that catching base exception catches syntax errors."""
        with pytest.raises(NgxParserBaseException):
            raise NgxParserSyntaxError('syntax error', 'file.conf', 1)

    def test_catching_base_catches_directive_error(self):
        """Test that catching base exception catches directive errors."""
        with pytest.raises(NgxParserBaseException):
            raise NgxParserDirectiveError('directive error', 'file.conf', 1)

    def test_catching_base_catches_arguments_error(self):
        """Test that catching base exception catches arguments errors."""
        with pytest.raises(NgxParserBaseException):
            raise NgxParserDirectiveArgumentsError('args error', 'file.conf', 1)

    def test_catching_base_catches_context_error(self):
        """Test that catching base exception catches context errors."""
        with pytest.raises(NgxParserBaseException):
            raise NgxParserDirectiveContextError('context error', 'file.conf', 1)

    def test_catching_base_catches_unknown_error(self):
        """Test that catching base exception catches unknown errors."""
        with pytest.raises(NgxParserBaseException):
            raise NgxParserDirectiveUnknownError('unknown error', 'file.conf', 1)

    def test_catching_directive_catches_subclasses(self):
        """Test that catching DirectiveError catches its subclasses."""
        with pytest.raises(NgxParserDirectiveError):
            raise NgxParserDirectiveArgumentsError('args error', 'file.conf', 1)

        with pytest.raises(NgxParserDirectiveError):
            raise NgxParserDirectiveContextError('context error', 'file.conf', 1)

        with pytest.raises(NgxParserDirectiveError):
            raise NgxParserDirectiveUnknownError('unknown error', 'file.conf', 1)

    def test_catching_syntax_does_not_catch_directive(self):
        """Test that SyntaxError and DirectiveError are distinct."""
        with pytest.raises(NgxParserDirectiveError):
            try:
                raise NgxParserDirectiveError('directive error', 'file.conf', 1)
            except NgxParserSyntaxError:
                pytest.fail('Should not catch DirectiveError as SyntaxError')


class TestExceptionUsage:
    """Tests for typical exception usage patterns."""

    def test_raise_and_access_attributes(self):
        """Test raising exception and accessing attributes in handler."""
        try:
            raise NgxParserSyntaxError(
                strerror='unexpected }',
                filename='/etc/nginx/nginx.conf',
                lineno=100
            )
        except NgxParserSyntaxError as e:
            assert e.strerror == 'unexpected }'
            assert e.filename == '/etc/nginx/nginx.conf'
            assert e.lineno == 100
            assert 'unexpected }' in str(e)
            assert '/etc/nginx/nginx.conf' in str(e)
            assert '100' in str(e)

    def test_exception_with_none_filename(self):
        """Test exception with None filename."""
        exc = NgxParserBaseException('error', None, 5)
        result = str(exc)
        assert result == 'error in None:5'

    def test_exception_with_unicode_message(self):
        """Test exception with unicode characters in message."""
        exc = NgxParserSyntaxError(
            strerror='invalid character: \u00e9',
            filename='/path/to/file.conf',
            lineno=1
        )
        result = str(exc)
        assert 'invalid character: \u00e9' in result
