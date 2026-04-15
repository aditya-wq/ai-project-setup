"""AI Agent integration hooks.

Provides hooks for Claude Code, Codex, and other AI agent integrations.
"""

import os
import json
from pathlib import Path
from typing import Optional

DEFAULT_MODE = "full"
HOOK_FILE = ".aiproject-active"
CONFIG_FILE = "aiproject-config.json"


def get_default_mode() -> str:
    """Get the default compression/intensity mode.

    Returns:
        Mode string (lite, full, ultra, or off)
    """
    return os.environ.get("AIPROJECT_DEFAULT_MODE", DEFAULT_MODE)


def set_mode(mode: str) -> None:
    """Set the current mode in the flag file.

    Args:
        mode: Mode to set (lite, full, ultra, commit, review, compress, off)
    """
    home_dir = Path.home()
    flag_path = home_dir / ".aiproject" / HOOK_FILE

    flag_path.parent.mkdir(parents=True, exist_ok=True)
    flag_path.write_text(mode)


def get_mode() -> Optional[str]:
    """Get the current mode from flag file.

    Returns:
        Mode string or None if not set
    """
    home_dir = Path.home()
    flag_path = home_dir / ".aiproject" / HOOK_FILE

    if flag_path.exists():
        return flag_path.read_text().strip()
    return None


def clear_mode() -> None:
    """Clear the current mode flag."""
    home_dir = Path.home()
    flag_path = home_dir / ".aiproject" / HOOK_FILE
    flag_path.unlink(missing_ok=True)


def get_status_badge(mode: str) -> str:
    """Generate status badge for the given mode.

    Args:
        mode: Current mode

    Returns:
        Status badge string for display
    """
    if mode == "off" or not mode:
        return ""

    upper_mode = mode.upper()
    return f"[AIPROJECT:{upper_mode}]"
