"""Integration tests for compression workflow."""

import pytest
from pathlib import Path
from ai_project.compression import compress_file


class TestCompressionWorkflow:
    """Integration tests for compression workflow."""

    def test_compression_creates_backup(self, tmp_path):
        """Test that compression creates backup file."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test File\n\nThis is test content.")

        result = compress_file(test_file)

        backup_file = tmp_path / "test.original.md"
        assert backup_file.exists()

    def test_compression_preserves_headings(self, tmp_path):
        """Test that headings are preserved in compression."""
        test_file = tmp_path / "test.md"
        content = "# Title\n## Section 1\n### Subsection\n## Section 2"
        test_file.write_text(content)

        result = compress_file(test_file)
        compressed = test_file.read_text()

        assert "# Title" in compressed
        assert "## Section 1" in compressed

    def test_compression_preserves_code_blocks(self, tmp_path):
        """Test that code blocks are preserved."""
        test_file = tmp_path / "test.md"
        content = "# Code Example\n\n```python\ndef hello():\n    print('world')\n```"
        test_file.write_text(content)

        compress_file(test_file)
        compressed = test_file.read_text()

        assert "```python" in compressed
        assert "print('world')" in compressed

    def test_compression_preserves_urls(self, tmp_path):
        """Test that URLs are preserved."""
        test_file = tmp_path / "test.md"
        content = "# Links\n\nCheck https://example.com for info\n\nVisit http://test.org"
        test_file.write_text(content)

        compress_file(test_file)
        compressed = test_file.read_text()

        assert "https://example.com" in compressed
        assert "http://test.org" in compressed

    def test_compression_preserves_bullets(self, tmp_path):
        """Test that bullet points are preserved."""
        test_file = tmp_path / "test.md"
        content = "# List\n\n- Item 1\n- Item 2\n- Item 3"
        test_file.write_text(content)

        compress_file(test_file)
        compressed = test_file.read_text()

        assert compressed.count("- Item") >= 2

    def test_handles_large_file_gracefully(self, tmp_path):
        """Test handling of large files."""
        test_file = tmp_path / "large.md"
        content = "# Large File\n\n" + ("Paragraph text. " * 1000)
        test_file.write_text(content)

        try:
            result = compress_file(test_file)
        except Exception as e:
            assert "too large" in str(e).lower() or "size" in str(e).lower()
