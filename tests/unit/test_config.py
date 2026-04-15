"""Unit tests for config module."""

import os
import pytest
from ai_project.config import Settings, get_settings, reload_settings


class TestSettings:
    """Test suite for Settings class."""

    def test_default_values(self):
        """Test default configuration values."""
        settings = Settings()
        assert settings.model == "claude-sonnet-4-5"
        assert settings.max_file_size == 500000
        assert settings.max_retries == 2
        assert settings.backup_suffix == ".original"
        assert settings.compress_enabled is True
        assert settings.hook_auto_activate is True
        assert settings.default_intensity == "full"
        assert settings.log_level == "INFO"

    def test_from_env_vars(self):
        """Test loading settings from environment variables."""
        os.environ["AIPROJECT_MODEL"] = "claude-opus-4"
        os.environ["AIPROJECT_MAX_FILE_SIZE"] = "1000000"
        os.environ["AIPROJECT_ENABLED"] = "false"

        settings = Settings()
        assert settings.model == "claude-opus-4"
        assert settings.max_file_size == 1000000
        assert settings.compress_enabled is False

        del os.environ["AIPROJECT_MODEL"]
        del os.environ["AIPROJECT_MAX_FILE_SIZE"]
        del os.environ["AIPROJECT_ENABLED"]

    def test_validate_model(self):
        """Test model validation."""
        os.environ["AIPROJECT_MODEL"] = "invalid-model"
        settings = Settings()
        assert settings.model == "invalid-model"
        del os.environ["AIPROJECT_MODEL"]

    def test_validate_max_retries(self):
        """Test max_retries validation."""
        os.environ["AIPROJECT_MAX_RETRIES"] = "5"
        settings = Settings()
        assert settings.max_retries == 5
        del os.environ["AIPROJECT_MAX_RETRIES"]


class TestGetSettings:
    """Test suite for get_settings singleton."""

    def test_returns_singleton(self):
        """Test that get_settings returns the same instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2

    def test_reload_returns_new_instance(self):
        """Test that reload_settings returns a new instance."""
        settings1 = get_settings()
        settings2 = reload_settings()
        assert settings1 is settings2
