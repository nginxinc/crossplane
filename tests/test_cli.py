# -*- coding: utf-8 -*-
"""Tests for crossplane CLI (__main__.py)."""
import io
import os
import sys

import pytest

from crossplane.__main__ import (
    parse_args,
    parse,
    build,
    lex,
    minify,
    format,
    _dump_payload,
    _prompt_yes,
)

here = os.path.dirname(__file__)


class TestParseArgs:
    """Tests for argument parsing."""

    def test_parse_command(self):
        """Test parse subcommand argument parsing."""
        args = parse_args(['parse', 'nginx.conf'])
        assert args._subcommand.__name__ == 'parse'
        assert args.filename == 'nginx.conf'
        assert args.out is None
        assert args.indent is None
        assert args.catch is True
        assert args.single is False
        assert args.comments is False
        assert args.strict is False
        assert args.combine is False

    def test_parse_command_with_options(self):
        """Test parse subcommand with various options."""
        args = parse_args([
            'parse', 'nginx.conf',
            '--out', 'output.json',
            '--indent', '2',
            '--no-catch',
            '--single-file',
            '--include-comments',
            '--strict',
            '--combine',
            '--ignore', 'ssl_certificate,ssl_key'
        ])
        assert args.out == 'output.json'
        assert args.indent == 2
        assert args.catch is False
        assert args.single is True
        assert args.comments is True
        assert args.strict is True
        assert args.combine is True
        assert args.ignore == 'ssl_certificate,ssl_key'

    def test_build_command(self):
        """Test build subcommand argument parsing."""
        args = parse_args(['build', 'payload.json'])
        assert args._subcommand.__name__ == 'build'
        assert args.filename == 'payload.json'
        assert args.dirname is None
        assert args.force is False
        assert args.indent == 4
        assert args.tabs is False
        assert args.header is True
        assert args.stdout is False
        assert args.verbose is False

    def test_build_command_with_options(self):
        """Test build subcommand with various options."""
        args = parse_args([
            'build', 'payload.json',
            '--dir', '/tmp/nginx',
            '--force',
            '--indent', '2',
            '--no-headers',
            '--stdout',
            '--verbose'
        ])
        assert args.dirname == '/tmp/nginx'
        assert args.force is True
        assert args.indent == 2
        assert args.header is False
        assert args.stdout is True
        assert args.verbose is True

    def test_build_command_tabs_option(self):
        """Test build subcommand with tabs option."""
        args = parse_args(['build', 'payload.json', '--tabs'])
        assert args.tabs is True

    def test_lex_command(self):
        """Test lex subcommand argument parsing."""
        args = parse_args(['lex', 'nginx.conf'])
        assert args._subcommand.__name__ == 'lex'
        assert args.filename == 'nginx.conf'
        assert args.out is None
        assert args.indent is None
        assert args.line_numbers is False

    def test_lex_command_with_options(self):
        """Test lex subcommand with various options."""
        args = parse_args([
            'lex', 'nginx.conf',
            '--out', 'tokens.json',
            '--indent', '4',
            '--line-numbers'
        ])
        assert args.out == 'tokens.json'
        assert args.indent == 4
        assert args.line_numbers is True

    def test_minify_command(self):
        """Test minify subcommand argument parsing."""
        args = parse_args(['minify', 'nginx.conf'])
        assert args._subcommand.__name__ == 'minify'
        assert args.filename == 'nginx.conf'
        assert args.out is None

    def test_minify_command_with_output(self):
        """Test minify subcommand with output option."""
        args = parse_args(['minify', 'nginx.conf', '--out', 'minified.conf'])
        assert args.out == 'minified.conf'

    def test_format_command(self):
        """Test format subcommand argument parsing."""
        args = parse_args(['format', 'nginx.conf'])
        assert args._subcommand.__name__ == 'format'
        assert args.filename == 'nginx.conf'
        assert args.out is None
        assert args.indent == 4
        assert args.tabs is False

    def test_format_command_with_options(self):
        """Test format subcommand with various options."""
        args = parse_args([
            'format', 'nginx.conf',
            '--out', 'formatted.conf',
            '--indent', '2'
        ])
        assert args.out == 'formatted.conf'
        assert args.indent == 2

    def test_format_command_with_tabs(self):
        """Test format subcommand with tabs option."""
        args = parse_args(['format', 'nginx.conf', '--tabs'])
        assert args.tabs is True

    def test_help_command(self):
        """Test help subcommand argument parsing."""
        args = parse_args(['help', 'parse'])
        assert args._subcommand.__name__ == 'help'
        assert args.command == 'parse'

    def test_version_flag(self):
        """Test --version flag."""
        with pytest.raises(SystemExit) as exc_info:
            parse_args(['--version'])
        assert exc_info.value.code == 0

    def test_no_subcommand_error(self):
        """Test error when no subcommand is provided."""
        with pytest.raises(SystemExit) as exc_info:
            parse_args([])
        assert exc_info.value.code != 0


class TestDumpPayload:
    """Tests for _dump_payload function."""

    def test_dump_payload_with_indent(self):
        """Test JSON output with indentation."""
        fp = io.StringIO()
        obj = {'key': 'value', 'list': [1, 2, 3]}
        _dump_payload(obj, fp, indent=2)
        output = fp.getvalue()
        assert '  "key"' in output
        assert output.endswith('\n')

    def test_dump_payload_without_indent(self):
        """Test JSON output without indentation (minified)."""
        fp = io.StringIO()
        obj = {'key': 'value', 'list': [1, 2, 3]}
        _dump_payload(obj, fp, indent=None)
        output = fp.getvalue()
        # Should be compact (no spaces after separators)
        assert '{"key":"value"' in output
        assert output.endswith('\n')


class TestCliParse:
    """Tests for CLI parse command."""

    def test_parse_to_file(self, tmp_path):
        """Test parse writes to file when --out specified."""
        config = os.path.join(here, 'configs', 'cli-test', 'nginx.conf')
        output_file = str(tmp_path / 'output.json')
        parse(config, out=output_file, catch=True)
        assert os.path.exists(output_file)
        with open(output_file) as f:
            content = f.read()
        assert 'status' in content

    def test_parse_with_indent(self, tmp_path):
        """Test parse with indentation."""
        config = os.path.join(here, 'configs', 'cli-test', 'nginx.conf')
        output_file = str(tmp_path / 'output.json')
        parse(config, out=output_file, indent=2, catch=True)
        with open(output_file) as f:
            content = f.read()
        # Indented output should have newlines and spaces
        assert '\n' in content
        assert '  ' in content

    def test_parse_with_comments(self, tmp_path):
        """Test parse with comments included."""
        config = os.path.join(here, 'configs', 'with-comments', 'nginx.conf')
        output_file = str(tmp_path / 'output.json')
        parse(config, out=output_file, catch=True, comments=True)
        with open(output_file) as f:
            content = f.read()
        assert 'comment' in content


class TestCliLex:
    """Tests for CLI lex command."""

    def test_lex_to_file(self, tmp_path):
        """Test lex writes to file."""
        config = os.path.join(here, 'configs', 'cli-test', 'nginx.conf')
        output_file = str(tmp_path / 'tokens.json')
        lex(config, out=output_file, indent=None, line_numbers=False)
        assert os.path.exists(output_file)
        with open(output_file) as f:
            content = f.read()
        assert 'events' in content
        assert 'http' in content

    def test_lex_with_line_numbers(self, tmp_path):
        """Test lex command with line numbers."""
        config = os.path.join(here, 'configs', 'cli-test', 'nginx.conf')
        output_file = str(tmp_path / 'tokens.json')
        lex(config, out=output_file, indent=None, line_numbers=True)
        with open(output_file) as f:
            content = f.read()
        # With line numbers, output should be tuples like ["events", 1]
        assert '[' in content


class TestCliMinify:
    """Tests for CLI minify command."""

    def test_minify_to_file(self, tmp_path):
        """Test minify writes to file."""
        config = os.path.join(here, 'configs', 'cli-test', 'nginx.conf')
        output_file = str(tmp_path / 'minified.conf')
        minify(config, out=output_file)
        assert os.path.exists(output_file)
        with open(output_file) as f:
            content = f.read()
        # Minified output should contain the directives
        assert 'events' in content


class TestCliFormat:
    """Tests for CLI format command."""

    def test_format_to_file(self, tmp_path):
        """Test format writes to file."""
        config = os.path.join(here, 'configs', 'cli-test', 'nginx.conf')
        output_file = str(tmp_path / 'formatted.conf')
        format(config, out=output_file, indent=4, tabs=False)
        assert os.path.exists(output_file)
        with open(output_file) as f:
            content = f.read()
        assert 'events' in content
        assert 'http' in content

    def test_format_with_tabs(self, tmp_path):
        """Test format with tabs."""
        config = os.path.join(here, 'configs', 'cli-test', 'nginx.conf')
        output_file = str(tmp_path / 'formatted.conf')
        format(config, out=output_file, indent=4, tabs=True)
        with open(output_file) as f:
            content = f.read()
        assert '\t' in content


class TestCliBuild:
    """Tests for CLI build command."""

    def test_build_creates_files(self, tmp_path):
        """Test build creates nginx config files."""
        payload_file = os.path.join(here, 'configs', 'cli-test', 'payload.json')
        build(payload_file, dirname=str(tmp_path), force=True, stdout=False)
        assert os.path.exists(tmp_path / 'nginx.conf')

    def test_build_verbose(self, capsys, tmp_path):
        """Test build verbose output."""
        payload_file = os.path.join(here, 'configs', 'cli-test', 'payload.json')
        build(payload_file, dirname=str(tmp_path), force=True, verbose=True)
        captured = capsys.readouterr()
        assert 'wrote to' in captured.out


class TestPromptYes:
    """Tests for _prompt_yes function."""

    def test_prompt_yes_keyboard_interrupt(self, monkeypatch):
        """Test that KeyboardInterrupt causes sys.exit(1)."""
        def mock_input(prompt):
            raise KeyboardInterrupt()

        monkeypatch.setattr('crossplane.__main__.input', mock_input)
        with pytest.raises(SystemExit) as exc_info:
            _prompt_yes()
        assert exc_info.value.code == 1

    def test_prompt_yes_eof_error(self, monkeypatch):
        """Test that EOFError causes sys.exit(1)."""
        def mock_input(prompt):
            raise EOFError()

        monkeypatch.setattr('crossplane.__main__.input', mock_input)
        with pytest.raises(SystemExit) as exc_info:
            _prompt_yes()
        assert exc_info.value.code == 1

    def test_prompt_yes_returns_true(self, monkeypatch):
        """Test that 'y' input returns True."""
        monkeypatch.setattr('crossplane.__main__.input', lambda prompt: 'y')
        assert _prompt_yes() is True

    def test_prompt_yes_returns_true_uppercase(self, monkeypatch):
        """Test that 'Y' input returns True."""
        monkeypatch.setattr('crossplane.__main__.input', lambda prompt: 'Y')
        assert _prompt_yes() is True

    def test_prompt_yes_returns_true_with_extra(self, monkeypatch):
        """Test that 'yes' input returns True."""
        monkeypatch.setattr('crossplane.__main__.input', lambda prompt: 'yes')
        assert _prompt_yes() is True

    def test_prompt_no_returns_false(self, monkeypatch):
        """Test that 'n' input returns False."""
        monkeypatch.setattr('crossplane.__main__.input', lambda prompt: 'n')
        assert _prompt_yes() is False

    def test_prompt_empty_returns_false(self, monkeypatch):
        """Test that empty input returns False."""
        monkeypatch.setattr('crossplane.__main__.input', lambda prompt: '')
        assert _prompt_yes() is False
