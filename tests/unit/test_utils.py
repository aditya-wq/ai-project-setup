"""Unit tests for utils module."""

import pytest
from pathlib import Path
from ai_project.utils import (
    setup_logging,
    safe_read_file,
    safe_write_file,
    ensure_dir,
    format_file_size,
)


class TestSetupLogging:
    """Test suite for logging setup."""

    def test_returns_logger(self):
        """Test that setup_logging returns a logger."""
        logger = setup_logging()
        assert logger is not None

    def test_sets_level(self):
        """Test that log level is set correctly."""
        logger = setup_logging("DEBUG")
        assert logger.level == 10


class TestSafeReadFile:
    """Test suite for safe file reading."""

    def test_reads_existing_file(self, tmp_path):
        """Test reading an existing file."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("Hello, World!")

        content = safe_read_file(file_path)
        assert content == "Hello, World!"

    def test_returns_default_for_missing_file(self, tmp_path):
        """Test default value for missing file."""
        file_path = tmp_path / "missing.txt"
        content = safe_read_file(file_path, default="default")
        assert content == "default"

    def test_reads_string_path(self, tmp_path):
        """Test reading with string path."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("Hello!")

        content = safe_read_file(str(file_path))
        assert content == "Hello!"


class TestSafeWriteFile:
    """Test suite for safe file writing."""

    def test_writes_file(self, tmp_path):
        """Test writing a file."""
        file_path = tmp_path / "output.txt"
        result = safe_write_file(file_path, "Hello, World!")

        assert result is True
        assert file_path.read_text() == "Hello, World!"

    def test_returns_false_on_error(self):
        """Test returns False on write error."""
        result = safe_write_file("/invalid/path/file.txt", "content")
        assert result is False


class TestEnsureDir:
    """Test suite for directory creation."""

    def test_creates_parent_directory(self, tmp_path):
        """Test that parent directory is created."""
        file_path = tmp_path / "subdir" / "file.txt"
        result = ensure_dir(file_path)

        assert result == file_path
        assert file_path.parent.exists()


class TestFormatFileSize:
    """Test suite for file size formatting."""

    def test_formats_bytes(self):
        """Test formatting bytes."""
        assert format_file_size(500) == "500.0 B"

    def test_formats_kilobytes(self):
        """Test formatting kilobytes."""
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1500) == "1.5 KB"

    def test_formats_megabytes(self):
        """Test formatting megabytes."""
        assert format_file_size(1024 * 1024) == "1.0 MB"
        assert format_file_size(1024 * 1024 * 5) == "5.0 MB"

    def test_formats_gigabytes(self):
        """Test formatting gigabytes."""
        assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"

    def test_handles_zero(self):
        """Test formatting zero."""
        assert format_file_size(0) == "0.0 B"
