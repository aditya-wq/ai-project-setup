"""Unit tests for validators module."""

import pytest
from pathlib import Path
from ai_project.validators import (
    ValidationResult,
    extract_code_blocks,
    extract_headings,
    extract_urls,
    extract_paths,
    count_bullets,
    validate,
    validate_headings,
    validate_code_blocks,
    validate_urls,
    validate_paths,
    validate_bullets,
)


class TestExtractHeadings:
    """Test suite for heading extraction."""

    def test_extracts_single_heading(self):
        """Test extraction of a single heading."""
        text = "# Hello World"
        result = extract_headings(text)
        assert len(result) == 1
        assert result[0] == ("#", "Hello World")

    def test_extracts_multiple_headings(self):
        """Test extraction of multiple headings."""
        text = "# Heading 1\n## Heading 2\n### Heading 3"
        result = extract_headings(text)
        assert len(result) == 3

    def test_extracts_atx_style(self):
        """Test ATX-style headings (# to ######)."""
        text = "# H1\n## H2\n### H3\n#### H4\n##### H5\n###### H6"
        result = extract_headings(text)
        assert len(result) == 6



    def test_handles_empty_text(self):
        """Test with empty text."""
        result = extract_headings("")
        assert result == []

    def test_handles_no_headings(self):
        """Test with no headings."""
        result = extract_headings("Just plain text")
        assert result == []


class TestExtractCodeBlocks:
    """Test suite for code block extraction."""

    def test_extracts_fenced_code_block(self):
        """Test extraction of fenced code block."""
        text = "```python\nprint('hello')\n```"
        result = extract_code_blocks(text)
        assert len(result) == 1
        assert "print('hello')" in result[0]

    def test_extracts_tilde_code_block(self):
        """Test extraction of tilde-fenced code block."""
        text = "~~~\ncode here\n~~~"
        result = extract_code_blocks(text)
        assert len(result) == 1

    def test_extracts_multiple_code_blocks(self):
        """Test extraction of multiple code blocks."""
        text = "```js\ncode1\n```\ntext\n```py\ncode2\n```"
        result = extract_code_blocks(text)
        assert len(result) == 2

    def test_handles_empty_text(self):
        """Test with empty text."""
        result = extract_code_blocks("")
        assert result == []

    def test_handles_no_code_blocks(self):
        """Test with no code blocks."""
        result = extract_code_blocks("Just plain text")
        assert result == []


class TestExtractUrls:
    """Test suite for URL extraction."""

    def test_extracts_https_url(self):
        """Test extraction of HTTPS URL."""
        text = "Check https://example.com for more info"
        result = extract_urls(text)
        assert "https://example.com" in result

    def test_extracts_http_url(self):
        """Test extraction of HTTP URL."""
        text = "Visit http://example.com"
        result = extract_urls(text)
        assert "http://example.com" in result

    def test_extracts_multiple_urls(self):
        """Test extraction of multiple URLs."""
        text = "Links: https://a.com and http://b.com"
        result = extract_urls(text)
        assert len(result) == 2

    def test_extracts_urls_with_paths(self):
        """Test extraction of URLs with paths."""
        text = "See https://example.com/path/to/resource"
        result = extract_urls(text)
        assert "https://example.com/path/to/resource" in result

    def test_handles_empty_text(self):
        """Test with empty text."""
        result = extract_urls("")
        assert result == set()

    def test_handles_no_urls(self):
        """Test with no URLs."""
        result = extract_urls("Just plain text")
        assert result == set()


class TestExtractPaths:
    """Test suite for file path extraction."""

    def test_extracts_unix_paths(self):
        """Test extraction of Unix-style paths."""
        text = "See /usr/local/bin/file"
        result = extract_paths(text)
        assert "/usr/local/bin/file" in result

    def test_extracts_windows_paths(self):
        """Test extraction of Windows paths."""
        text = "C:\\Users\\name\\file.txt"
        result = extract_paths(text)
        assert len(result) >= 1

    def test_extracts_relative_paths(self):
        """Test extraction of relative paths."""
        text = "Check ./src/module"
        result = extract_paths(text)
        assert "./src/module" in result

    def test_handles_empty_text(self):
        """Test with empty text."""
        result = extract_paths("")
        assert result == set()

    def test_handles_no_paths(self):
        """Test with no paths."""
        result = extract_paths("Just plain text")
        assert result == set()


class TestCountBullets:
    """Test suite for bullet point extraction."""

    def test_extracts_dash_bullets(self):
        """Test extraction of dash bullets."""
        text = "- item 1\n- item 2"
        result = count_bullets(text)
        assert result == 2

    def test_extracts_asterisk_bullets(self):
        """Test extraction of asterisk bullets."""
        text = "* item 1\n* item 2"
        result = count_bullets(text)
        assert result == 2

    def test_extracts_plus_bullets(self):
        """Test extraction of plus bullets."""
        text = "+ item 1\n+ item 2"
        result = count_bullets(text)
        assert result == 2

    def test_handles_empty_text(self):
        """Test with empty text."""
        result = count_bullets("")
        assert result == 0

    def test_handles_no_bullets(self):
        """Test with no bullets."""
        result = count_bullets("Just plain text")
        assert result == 0


class TestValidationResult:
    """Test suite for ValidationResult class."""

    def test_valid_result(self):
        """Test valid result with no issues."""
        result = ValidationResult()
        assert result.is_valid
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_result_with_errors(self):
        """Test result with errors."""
        result = ValidationResult()
        result.add_error("Missing code block")
        assert not result.is_valid
        assert len(result.errors) == 1

    def test_result_with_warnings(self):
        """Test result with warnings."""
        result = ValidationResult()
        result.add_warning("Bullet count changed")
        assert result.is_valid
        assert len(result.warnings) == 1


class TestValidateHeadings:
    """Test suite for heading validation."""

    def test_validates_matching_headings(self):
        """Test validation passes with matching headings."""
        original = "# Title\n## Section\n### Subsection"
        compressed = "# Title\n## Section\n### Subsection"
        result = ValidationResult()
        validate_headings(original, compressed, result)
        assert result.is_valid

    def test_validates_order_preserved(self):
        """Test validation warns if heading order changes."""
        original = "# A\n## B"
        compressed = "## B\n# A"
        result = ValidationResult()
        validate_headings(original, compressed, result)
        assert result.is_valid
        assert len(result.warnings) > 0

    def test_handles_empty_original(self):
        """Test handling of empty original."""
        result = ValidationResult()
        validate_headings("", "# Title", result)
        # It fails because length mismatch!
        assert not result.is_valid


class TestValidateCodeBlocks:
    """Test suite for code block validation."""

    def test_validates_preserved_blocks(self):
        """Test validation passes when blocks preserved."""
        text = "```python\nprint('hello')\n```"
        result = ValidationResult()
        validate_code_blocks(text, text, result)
        assert result.is_valid

    def test_handles_empty_original(self):
        """Test handling of empty original."""
        result = ValidationResult()
        validate_code_blocks("", "```code\nhello\n```", result)
        # Length changed, c1=[], c2=1 -> adds error
        assert not result.is_valid


class TestValidateUrls:
    """Test suite for URL validation."""

    def test_validates_preserved_urls(self):
        """Test validation passes when URLs preserved."""
        text = "Visit https://example.com"
        result = ValidationResult()
        validate_urls(text, text, result)
        assert result.is_valid

    def test_handles_empty_original(self):
        """Test handling of empty original."""
        result = ValidationResult()
        validate_urls("", "https://example.com", result)
        assert not result.is_valid


class TestValidatePaths:
    """Test suite for path validation."""

    def test_validates_preserved_paths(self):
        """Test validation passes when paths preserved."""
        text = "Check /usr/local/bin"
        result = ValidationResult()
        validate_paths(text, text, result)
        assert result.is_valid

    def test_handles_empty_original(self):
        """Test handling of empty original."""
        result = ValidationResult()
        validate_paths("", "/path/to/file", result)
        # Paths only adds warnings, so it is still valid
        assert result.is_valid


class TestValidateBullets:
    """Test suite for bullet validation."""

    def test_validates_preserved_bullets(self):
        """Test validation passes when bullets preserved."""
        text = "- item 1\n- item 2"
        result = ValidationResult()
        validate_bullets(text, text, result)
        assert result.is_valid

    def test_allows_small_difference(self):
        """Test allows small difference (<15%)."""
        original = "\\n".join([f"- item {i}" for i in range(20)])
        compressed = "\\n".join([f"- item {i}" for i in range(18)])
        result = ValidationResult()
        validate_bullets(original, compressed, result)
        assert result.is_valid

    def test_handles_empty_original(self):
        """Test handling of empty original."""
        result = ValidationResult()
        validate_bullets("", "- item 1", result)
        assert result.is_valid


class TestValidate:
    """Test suite for main validate function."""

    def test_validates_complete_content(self, tmp_path):
        """Test full validation of content."""
        original = "# Title\\n\\nCheck https://example.com\\n\\n```python\\nprint('hello')\\n```\\n\\n- item 1\\n- item 2\\n"
        compressed = original
        
        orig_file = tmp_path / "orig.md"
        comp_file = tmp_path / "comp.md"
        orig_file.write_text(original)
        comp_file.write_text(compressed)

        result = validate(orig_file, comp_file)
        assert result.is_valid

    def test_returns_combined_result(self, tmp_path):
        """Test returns combined validation result."""
        original = "# Title\\n\\n```code```\\n\\n- item"
        compressed = "# Title\\n\\n```code```\\n\\n- item"
        
        orig_file = tmp_path / "orig.md"
        comp_file = tmp_path / "comp.md"
        orig_file.write_text(original)
        comp_file.write_text(compressed)
        
        result = validate(orig_file, comp_file)
        assert isinstance(result, ValidationResult)
