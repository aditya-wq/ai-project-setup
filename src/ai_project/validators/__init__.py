"""Output validation module.

Validates compressed output to ensure structural elements are preserved:
headings, code blocks, URLs, file paths, and bullets.
"""

import re
from pathlib import Path
from typing import List, Set, Tuple

URL_REGEX = re.compile(r"https?://[^\s)]+")
FENCE_OPEN_REGEX = re.compile(r"^(\s{0,3})(`{3,}|~{3,})(.*)$")
HEADING_REGEX = re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE)
BULLET_REGEX = re.compile(r"^\s*[-*+]\s+", re.MULTILINE)
PATH_REGEX = re.compile(r"(?:\./|\.\./|/|[A-Za-z]:\\)[\w\-/\\\.]+|[\w\-\.]+[/\\][\w\-/\\\.]+")


class ValidationResult:
    """Container for validation results."""

    def __init__(self) -> None:
        self.is_valid: bool = True
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def add_error(self, msg: str) -> None:
        """Add an error and mark as invalid."""
        self.is_valid = False
        self.errors.append(msg)

    def add_warning(self, msg: str) -> None:
        """Add a warning without invalidating."""
        self.warnings.append(msg)


def read_file(path: Path) -> str:
    """Read file contents safely.

    Args:
        path: File path

    Returns:
        File contents as string
    """
    return path.read_text(errors="ignore")


def extract_headings(text: str) -> List[Tuple[str, str]]:
    """Extract all headings from markdown text.

    Args:
        text: Markdown text

    Returns:
        List of (level, title) tuples
    """
    return [(level, title.strip()) for level, title in HEADING_REGEX.findall(text)]


def extract_code_blocks(text: str) -> List[str]:
    """Extract fenced code blocks from text.

    Handles nested fences and variable fence lengths per CommonMark spec.

    Args:
        text: Markdown text

    Returns:
        List of code block strings including fences
    """
    blocks = []
    lines = text.split("\n")
    i = 0
    n = len(lines)

    while i < n:
        match = FENCE_OPEN_REGEX.match(lines[i])
        if not match:
            i += 1
            continue

        fence_char = match.group(2)[0]
        fence_len = len(match.group(2))
        block_lines = [lines[i]]
        i += 1
        closed = False

        while i < n:
            close_match = FENCE_OPEN_REGEX.match(lines[i])
            if (
                close_match
                and close_match.group(2)[0] == fence_char
                and len(close_match.group(2)) >= fence_len
                and close_match.group(3).strip() == ""
            ):
                block_lines.append(lines[i])
                closed = True
                i += 1
                break
            block_lines.append(lines[i])
            i += 1

        if closed:
            blocks.append("\n".join(block_lines))

    return blocks


def extract_urls(text: str) -> Set[str]:
    """Extract all URLs from text.

    Args:
        text: Text to search

    Returns:
        Set of URLs
    """
    return set(URL_REGEX.findall(text))


def extract_paths(text: str) -> Set[str]:
    """Extract file paths from text.

    Args:
        text: Text to search

    Returns:
        Set of file paths
    """
    return set(PATH_REGEX.findall(text))


def count_bullets(text: str) -> int:
    """Count bullet points in text.

    Args:
        text: Text to analyze

    Returns:
        Number of bullet points
    """
    return len(BULLET_REGEX.findall(text))


def validate_headings(original: str, compressed: str, result: ValidationResult) -> None:
    """Validate heading preservation.

    Args:
        original: Original text
        compressed: Compressed text
        result: ValidationResult to update
    """
    h1 = extract_headings(original)
    h2 = extract_headings(compressed)

    if len(h1) != len(h2):
        result.add_error(f"Heading count mismatch: {len(h1)} vs {len(h2)}")

    if h1 != h2:
        result.add_warning("Heading text/order changed")


def validate_code_blocks(original: str, compressed: str, result: ValidationResult) -> None:
    """Validate code block preservation.

    Args:
        original: Original text
        compressed: Compressed text
        result: ValidationResult to update
    """
    c1 = extract_code_blocks(original)
    c2 = extract_code_blocks(compressed)

    if c1 != c2:
        result.add_error("Code blocks not preserved exactly")


def validate_urls(original: str, compressed: str, result: ValidationResult) -> None:
    """Validate URL preservation.

    Args:
        original: Original text
        compressed: Compressed text
        result: ValidationResult to update
    """
    u1 = extract_urls(original)
    u2 = extract_urls(compressed)

    if u1 != u2:
        result.add_error(f"URL mismatch: lost={u1 - u2}, added={u2 - u1}")


def validate_paths(original: str, compressed: str, result: ValidationResult) -> None:
    """Validate file path preservation.

    Args:
        original: Original text
        compressed: Compressed text
        result: ValidationResult to update
    """
    p1 = extract_paths(original)
    p2 = extract_paths(compressed)

    if p1 != p2:
        result.add_warning(f"Path mismatch: lost={p1 - p2}, added={p2 - p1}")


def validate_bullets(original: str, compressed: str, result: ValidationResult) -> None:
    """Validate bullet point preservation.

    Args:
        original: Original text
        compressed: Compressed text
        result: ValidationResult to update
    """
    b1 = count_bullets(original)
    b2 = count_bullets(compressed)

    if b1 == 0:
        return

    diff = abs(b1 - b2) / b1

    if diff > 0.15:
        result.add_warning(f"Bullet count changed too much: {b1} -> {b2}")


def validate(original_path: Path, compressed_path: Path) -> ValidationResult:
    """Validate compressed output against original.

    Args:
        original_path: Path to original file
        compressed_path: Path to compressed file

    Returns:
        ValidationResult with any errors or warnings
    """
    result = ValidationResult()

    original = read_file(original_path)
    compressed = read_file(compressed_path)

    validate_headings(original, compressed, result)
    validate_code_blocks(original, compressed, result)
    validate_urls(original, compressed, result)
    validate_paths(original, compressed, result)
    validate_bullets(original, compressed, result)

    return result
