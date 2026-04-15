"""Configuration management module.

Provides centralized configuration with environment variable support,
defaults, and validation for all AI Project components.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class Settings:
    """Main settings container for AI Project configuration."""

    model: str = "claude-sonnet-4-5"
    max_file_size: int = 500_000
    max_retries: int = 2
    backup_suffix: str = ".original.md"
    compress_enabled: bool = True
    hook_auto_activate: bool = True
    default_intensity: str = "full"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        """Create Settings from environment variables."""
        return cls(
            model=os.environ.get("AIPROJECT_MODEL", "claude-sonnet-4-5"),
            max_file_size=int(os.environ.get("AIPROJECT_MAX_FILE_SIZE", "500000")),
            max_retries=int(os.environ.get("AIPROJECT_MAX_RETRIES", "2")),
            backup_suffix=os.environ.get("AIPROJECT_BACKUP_SUFFIX", ".original.md"),
            compress_enabled=os.environ.get("AIPROJECT_ENABLED", "true").lower() == "true",
            hook_auto_activate=os.environ.get("AIPROJECT_HOOK_AUTO", "true").lower() == "true",
            default_intensity=os.environ.get("AIPROJECT_INTENSITY", "full"),
            log_level=os.environ.get("AIPROJECT_LOG_LEVEL", "INFO"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return {
            "model": self.model,
            "max_file_size": self.max_file_size,
            "max_retries": self.max_retries,
            "backup_suffix": self.backup_suffix,
            "compress_enabled": self.compress_enabled,
            "hook_auto_activate": self.hook_auto_activate,
            "default_intensity": self.default_intensity,
            "log_level": self.log_level,
        }


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance.

    Returns:
        Settings instance (singleton)
    """
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def reload_settings() -> Settings:
    """Reload settings from environment.

    Returns:
        New Settings instance
    """
    global _settings
    _settings = Settings.from_env()
    return _settings


settings = get_settings()
