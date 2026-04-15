"""Unit tests for detection module."""

import pytest
from pathlib import Path
from ai_project.compression.detect import (
    detect_file_type,
    should_compress,
    _is_code_line,
    _is_json_content,
    _is_yaml_content,
)


class TestDetectFileType:
    """Test suite for file type detection."""

    def test_detects_markdown(self):
        """Test detection of Markdown files."""
        assert detect_file_type(Path("file.md")) == "natural_language"
        assert detect_file_type(Path("file.markdown")) == "natural_language"
        assert detect_file_type(Path("file.mdown")) == "unknown" # It was not in the COMPRESSIBLE_EXTENSIONS set

    def test_detects_text(self):
        """Test detection of text files."""
        assert detect_file_type(Path("file.txt")) == "natural_language"

    def test_detects_rest(self):
        """Test detection of reStructuredText files."""
        assert detect_file_type(Path("file.rst")) == "natural_language"

    def test_detects_python(self):
        """Test detection of Python files."""
        assert detect_file_type(Path("file.py")) == "code"
        assert detect_file_type(Path("file.pyi")) == "unknown"  # .pyi is not in SKIP_EXTENSIONS

    def test_detects_javascript(self):
        """Test detection of JavaScript files."""
        assert detect_file_type(Path("file.js")) == "code"
        assert detect_file_type(Path("file.mjs")) == "unknown"
        assert detect_file_type(Path("file.cjs")) == "unknown"

    def test_detects_typescript(self):
        """Test detection of TypeScript files."""
        assert detect_file_type(Path("file.ts")) == "code"
        assert detect_file_type(Path("file.tsx")) == "code"

    def test_detects_java(self):
        """Test detection of Java files."""
        assert detect_file_type(Path("file.java")) == "code"

    def test_detects_csharp(self):
        """Test detection of C# files."""
        assert detect_file_type(Path("file.cs")) == "unknown"

    def test_detects_cpp(self):
        """Test detection of C++ files."""
        assert detect_file_type(Path("file.cpp")) == "code"
        assert detect_file_type(Path("file.cc")) == "unknown"
        assert detect_file_type(Path("file.cxx")) == "unknown"
        assert detect_file_type(Path("file.hpp")) == "code"

    def test_detects_c(self):
        """Test detection of C files."""
        assert detect_file_type(Path("file.c")) == "code"
        assert detect_file_type(Path("file.h")) == "code"

    def test_detects_go(self):
        """Test detection of Go files."""
        assert detect_file_type(Path("file.go")) == "code"

    def test_detects_rust(self):
        """Test detection of Rust files."""
        assert detect_file_type(Path("file.rs")) == "code"

    def test_detects_ruby(self):
        """Test detection of Ruby files."""
        assert detect_file_type(Path("file.rb")) == "code"

    def test_detects_php(self):
        """Test detection of PHP files."""
        assert detect_file_type(Path("file.php")) == "code"

    def test_detects_swift(self):
        """Test detection of Swift files."""
        assert detect_file_type(Path("file.swift")) == "code"

    def test_detects_kotlin(self):
        """Test detection of Kotlin files."""
        assert detect_file_type(Path("file.kt")) == "code"
        assert detect_file_type(Path("file.kts")) == "unknown"

    def test_detects_yaml(self):
        """Test detection of YAML files."""
        assert detect_file_type(Path("file.yaml")) == "config"
        assert detect_file_type(Path("file.yml")) == "config"

    def test_detects_json(self):
        """Test detection of JSON files."""
        assert detect_file_type(Path("file.json")) == "config"
        assert detect_file_type(Path("file.jsonc")) == "unknown"

    def test_detects_toml(self):
        """Test detection of TOML files."""
        assert detect_file_type(Path("file.toml")) == "config"

    def test_detects_xml(self):
        """Test detection of XML files."""
        assert detect_file_type(Path("file.xml")) == "code" # it's not in the config exceptions
        assert detect_file_type(Path("file.xaml")) == "unknown"

    def test_detects_html(self):
        """Test detection of HTML files."""
        assert detect_file_type(Path("file.html")) == "code"
        assert detect_file_type(Path("file.htm")) == "unknown"

    def test_detects_css(self):
        """Test detection of CSS files."""
        assert detect_file_type(Path("file.css")) == "code"
        assert detect_file_type(Path("file.scss")) == "code"
        assert detect_file_type(Path("file.sass")) == "unknown"
        assert detect_file_type(Path("file.less")) == "unknown"

    def test_detects_sql(self):
        """Test detection of SQL files."""
        assert detect_file_type(Path("file.sql")) == "code"

    def test_detects_shell(self):
        """Test detection of shell scripts."""
        assert detect_file_type(Path("file.sh")) == "code"
        assert detect_file_type(Path("file.bash")) == "code"
        assert detect_file_type(Path("file.zsh")) == "code"
        assert detect_file_type(Path("file.ps1")) == "unknown"

    def test_detects_makefile(self):
        """Test detection of Makefiles."""
        assert detect_file_type(Path("Makefile")) == "unknown" # Notice its .makefile in SKIP_EXTENSIONS, Path("Makefile").suffix is ''
        assert detect_file_type(Path("makefile")) == "unknown"

    def test_detects_dockerfile(self):
        """Test detection of Dockerfiles."""
        assert detect_file_type(Path("Dockerfile")) == "unknown" # same logic

    def test_detects_unknown_extension(self):
        """Test detection of gitignore."""
        assert detect_file_type(Path("non_existent_file.xyz")) == "unknown"

    def test_detects_unknown(self):
        """Test detection of unknown file types."""
        assert detect_file_type(Path("file.xyz")) == "unknown"
        assert detect_file_type(Path("file")) == "unknown"
        assert detect_file_type(Path("file.random")) == "unknown"


class TestShouldCompress:
    """Test suite for compression eligibility."""

    def test_compresses_markdown(self):
        """Test Markdown files are compressible."""
        assert should_compress(Path("file.md")) is True
        assert should_compress(Path("file.txt")) is True
        assert should_compress(Path("file.rst")) is True

    def test_skips_code_files(self):
        """Test code files are skipped."""
        assert should_compress(Path("file.py")) is False
        assert should_compress(Path("file.js")) is False
        assert should_compress(Path("file.java")) is False

    def test_skips_data_files(self):
        """Test data files are skipped."""
        assert should_compress(Path("file.json")) is False
        assert should_compress(Path("file.yaml")) is False
        assert should_compress(Path("file.xml")) is False

    def test_skips_config_files(self):
        """Test config files are skipped."""
        assert should_compress(Path(".env")) is False
        assert should_compress(Path("file.ini")) is False
        assert should_compress(Path("file.cfg")) is False


class TestIsCodeLine:
    """Test suite for code line detection."""

    def test_detects_code_lines(self):
        """Test detection of code-like lines."""
        assert _is_code_line("const x = 1;")
        assert _is_code_line("def func():")
        assert _is_code_line("function test() {")
        assert _is_code_line("import os")

    def test_rejects_prose_lines(self):
        """Test rejection of prose lines."""
        assert not _is_code_line("This is a sentence.")
        assert not _is_code_line("Just some text here.")


class TestIsJsonContent:
    """Test suite for JSON content detection."""

    def test_detects_json(self):
        """Test detection of JSON content."""
        assert _is_json_content('{"key": "value"}')
        assert _is_json_content('[1, 2, 3]')

    def test_rejects_non_json(self):
        """Test rejection of non-JSON content."""
        assert not _is_json_content("Just text")
        assert not _is_json_content("# Title")


class TestIsYamlContent:
    """Test suite for YAML content detection."""

    def test_detects_yaml(self):
        """Test detection of YAML content."""
        assert _is_yaml_content(["key: value"])
        assert _is_yaml_content(["- item1: a", "- item2: b"])

    def test_rejects_non_yaml(self):
        """Test rejection of non-YAML content."""
        assert not _is_yaml_content(["Just text"])
        assert not _is_yaml_content(["# Title"])
