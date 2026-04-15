"""Environment configuration loader.

Loads settings from .env files and environment variables.
"""

import os
from pathlib import Path
from typing import Optional


class EnvConfig:
    """Environment configuration handler."""

    def __init__(self, env_file: Optional[Path] = None):
        """Initialize with optional .env file path.

        Args:
            env_file: Path to .env file (defaults to .env in project root)
        """
        self.env_file = env_file or self._find_env_file()
        if self.env_file and self.env_file.exists():
            self._load_env_file()

    def _find_env_file(self) -> Optional[Path]:
        """Find .env file in project directory."""
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            env_path = parent / ".env"
            if env_path.exists():
                return env_path
        return None

    def _load_env_file(self) -> None:
        """Load environment variables from .env file."""
        with open(self.env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    if key not in os.environ:
                        os.environ[key] = value

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable value.

        Args:
            key: Variable name
            default: Default value if not found

        Returns:
            Value or default
        """
        return os.environ.get(key, default)


config = EnvConfig()
