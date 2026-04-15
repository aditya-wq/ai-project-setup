"""Shared utility functions.

Provides common utilities for file handling, logging, and error management.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure logging for the application.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("ai_project")
    logger.setLevel(getattr(logging, level.upper()))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def safe_read_file(filepath: Union[str, Path], default: str = "") -> str:
    """Safely read a file with fallback.

    Args:
        filepath: Path to file
        default: Default value if read fails

    Returns:
        File contents or default value
    """
    try:
        return Path(filepath).read_text(errors="ignore")
    except (OSError, PermissionError):
        return default


def safe_write_file(filepath: Union[str, Path], content: str) -> bool:
    """Safely write to a file.

    Args:
        filepath: Path to file
        content: Content to write

    Returns:
        True if successful
    """
    try:
        Path(filepath).write_text(content)
        return True
    except (OSError, PermissionError):
        return False


def ensure_dir(filepath: Union[str, Path]) -> Path:
    """Ensure directory exists for a file path.

    Args:
        filepath: File path

    Returns:
        Resolved Path object
    """
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def format_file_size(size: int) -> str:
    """Format file size in human-readable form.

    Args:
        size: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(size) < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


logger = setup_logging()
