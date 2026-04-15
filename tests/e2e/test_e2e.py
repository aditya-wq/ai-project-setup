"""End-to-end tests for complete workflows."""

import pytest
from pathlib import Path
from ai_project import compress_file
from ai_project.validators import validate
from ai_project.config import Settings


class TestEndToEndCompression:
    """End-to-end compression workflow tests."""

    @pytest.fixture
    def sample_markdown(self, tmp_path):
        """Create a sample markdown file."""
        file_path = tmp_path / "sample.md"
        content = """# Project Documentation

## Overview

This project provides text compression for AI agents.

## Features

- Fast compression
- High quality output
- Preserves structure

## Usage

```python
from ai_project import compress_file

compress_file("document.md")
```

## Links

- https://example.com/docs
- http://test.org/guide

## Configuration

Available settings:

- Model selection
- Retry limits
- Backup options

Check `/usr/local/config` for defaults.
"""
        file_path.write_text(content)
        return file_path

    def test_full_compression_workflow(self, sample_markdown):
        """Test complete compression workflow."""
        original_content = sample_markdown.read_text()

        result = compress_file(sample_markdown)

        compressed_content = sample_markdown.read_text()
        validation = validate(original_content, compressed_content)

        assert validation.is_valid() or len(validation.warnings) < 3

    def test_backup_created(self, sample_markdown):
        """Test backup file is created."""
        compress_file(sample_markdown)

        backup_path = sample_markdown.parent / "sample.original.md"
        assert backup_path.exists()
        assert backup_path.read_text().startswith("# Project Documentation")

    def test_validation_passes(self, sample_markdown):
        """Test that compressed content passes validation."""
        original = sample_markdown.read_text()
        compress_file(sample_markdown)
        compressed = sample_markdown.read_text()

        result = validate(original, compressed)

        assert len(result.errors) == 0


class TestConfigurationIntegration:
    """Test configuration integration."""

    def test_settings_load(self):
        """Test that settings load correctly."""
        settings = Settings()
        assert settings.model is not None
        assert settings.max_retries >= 0

    def test_environment_override(self):
        """Test environment variable override."""
        import os
        os.environ["AIPROJECT_MAX_RETRIES"] = "3"
        
        from ai_project.config import reload_settings
        settings = reload_settings()
        assert settings.max_retries == 3
        
        del os.environ["AIPROJECT_MAX_RETRIES"]
