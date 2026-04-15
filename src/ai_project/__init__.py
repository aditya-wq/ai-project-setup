"""AI Project - Text Compression and Optimization Toolkit.

A production-ready toolkit for compressing AI agent output and context files,
reducing token usage while preserving technical accuracy.

Architecture Overview:
    - compression: Core text compression modules
    - validators: Output validation and preservation checks
    - hooks: Agent integration hooks for Claude Code, Codex, etc.
    - config: Configuration management and environment settings
    - utils: Shared utilities and helpers
"""

__version__ = "1.0.0"
__author__ = "AI Project Team"
__license__ = "MIT"

from .compression import compress_file
from .validators import validate, ValidationResult

__all__ = [
    "compress_file",
    "validate",
    "ValidationResult",
    "__version__",
]
