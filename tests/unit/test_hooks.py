"""Unit tests for hooks module."""

import os
import pytest
from pathlib import Path
from ai_project.hooks import (
    get_default_mode,
    set_mode,
    get_mode,
    clear_mode,
    get_status_badge,
)


class TestGetDefaultMode:
    """Test suite for default mode retrieval."""

    def test_returns_full_by_default(self):
        """Test returns 'full' when no env var set."""
        result = get_default_mode()
        assert result == "full"

    def test_respects_env_var(self):
        """Test respects AIPROJECT_DEFAULT_MODE."""
        os.environ["AIPROJECT_DEFAULT_MODE"] = "lite"
        result = get_default_mode()
        assert result == "lite"
        del os.environ["AIPROJECT_DEFAULT_MODE"]


class TestSetMode:
    """Test suite for mode setting."""

    def test_sets_mode(self):
        """Test setting mode creates flag file."""
        set_mode("lite")
        flag_file = Path.home() / ".aiproject" / ".aiproject-mode"
        assert flag_file.exists()


class TestGetMode:
    """Test suite for mode retrieval."""

    def test_returns_none_when_not_set(self):
        """Test returns None when no mode is set."""
        clear_mode()
        result = get_mode()
        assert result is None

    def test_returns_set_mode(self):
        """Test returns set mode value."""
        set_mode("ultra")
        result = get_mode()
        assert result == "ultra"
        clear_mode()


class TestClearMode:
    """Test suite for mode clearing."""

    def test_clears_mode(self):
        """Test clearing mode removes flag file."""
        set_mode("full")
        clear_mode()
        result = get_mode()
        assert result is None


class TestGetStatusBadge:
    """Test suite for status badge generation."""

    def test_returns_badge_for_mode(self):
        """Test returns badge text for active mode."""
        set_mode("lite")
        badge = get_status_badge()
        assert "lite" in badge.lower()
        clear_mode()

    def test_returns_empty_when_inactive(self):
        """Test returns empty when not active."""
        clear_mode()
        badge = get_status_badge()
        assert badge == ""
