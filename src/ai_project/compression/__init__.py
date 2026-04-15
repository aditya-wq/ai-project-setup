"""Text compression orchestration module.

This module provides the core functionality for compressing text files while
preserving structural elements like code blocks, URLs, and headings.
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Optional

OUTER_FENCE_REGEX = re.compile(
    r"\A\s*(`{3,}|~{3,})[^\n]*\n(.*)\n\1\s*\Z", re.DOTALL
)

from ..validators import validate, ValidationResult
from ..config import settings

MAX_RETRIES = 2


def strip_llm_wrapper(text: str) -> str:
    """Remove outer markdown code fence if present.

    Args:
        text: The raw output from an LLM

    Returns:
        Text with outer fence removed if present
    """
    match = OUTER_FENCE_REGEX.match(text)
    if match:
        return match.group(2)
    return text


def call_llm(prompt: str, model: Optional[str] = None) -> str:
    """Call the LLM API or CLI to process text.

    Args:
        prompt: The prompt to send to the LLM
        model: Optional model override

    Returns:
        The LLM response text

    Raises:
        RuntimeError: If LLM call fails
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            msg = client.messages.create(
                model=model or os.environ.get("AIPROJECT_MODEL", "claude-sonnet-4-5"),
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}],
            )
            return strip_llm_wrapper(msg.content[0].text.strip())
        except ImportError:
            pass

    try:
        result = subprocess.run(
            ["claude", "--print"],
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
        )
        return strip_llm_wrapper(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"LLM call failed:\n{e.stderr}")


def build_compress_prompt(original: str) -> str:
    """Build the compression prompt for the LLM.

    Args:
        original: The original text to compress

    Returns:
        Formatted prompt for compression
    """
    return f"""Compress this markdown into terse format while preserving technical accuracy.

STRICT RULES:
- Do NOT modify anything inside ``` code blocks
- Do NOT modify anything inside inline backticks
- Preserve ALL URLs exactly
- Preserve ALL headings exactly
- Preserve file paths and commands
- Return ONLY the compressed markdown body — do NOT wrap the entire output in a ```markdown fence or any other fence
- Only compress natural language prose

TEXT:
{original}
"""


def build_fix_prompt(original: str, compressed: str, errors: List[str]) -> str:
    """Build a fix prompt for validation errors.

    Args:
        original: Reference original text
        compressed: The compressed text with errors
        errors: List of validation errors

    Returns:
        Formatted fix prompt
    """
    errors_str = "\n".join(f"- {e}" for e in errors)
    return f"""Fix the following issues in the compressed markdown file. ONLY fix the listed errors — leave everything else exactly as-is.

CRITICAL RULES:
- DO NOT recompress or rephrase the file
- ONLY fix the listed errors
- Preserve terse style in all untouched sections

ERRORS TO FIX:
{errors_str}

ORIGINAL (reference only):
{original}

COMPRESSED (fix this):
{compressed}

Return ONLY the fixed compressed file. No explanation.
"""


def compress_file(filepath: Path, model: Optional[str] = None) -> bool:
    """Compress a text file using LLM-based compression.

    Args:
        filepath: Path to the file to compress
        model: Optional LLM model override

    Returns:
        True if compression succeeded, False otherwise

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file is too large
    """
    filepath = filepath.resolve()
    max_file_size = 500_000

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if filepath.stat().st_size > max_file_size:
        raise ValueError(f"File too large to compress safely (max 500KB): {filepath}")

    from .detect import should_compress
    print(f"Processing: {filepath}")

    if not should_compress(filepath):
        print("Skipping (not natural language)")
        return False

    original_text = filepath.read_text(errors="ignore")
    backup_path = filepath.with_name(filepath.stem + ".original.md")

    if backup_path.exists():
        print(f"Warning: Backup file already exists: {backup_path}")
        print("Aborting to prevent data loss. Please remove or rename the backup file.")
        return False

    print("Compressing with LLM...")
    compressed = call_llm(build_compress_prompt(original_text), model)

    backup_path.write_text(original_text)
    filepath.write_text(compressed)

    for attempt in range(MAX_RETRIES):
        print(f"Validation attempt {attempt + 1}")

        result = validate(backup_path, filepath)

        if result.is_valid:
            print("Validation passed")
            break

        print("Validation failed:")
        for err in result.errors:
            print(f"   - {err}")

        if attempt == MAX_RETRIES - 1:
            filepath.write_text(original_text)
            backup_path.unlink(missing_ok=True)
            print("Failed after retries — original restored")
            return False

        print("Fixing with LLM...")
        compressed = call_llm(
            build_fix_prompt(original_text, compressed, result.errors),
            model
        )
        filepath.write_text(compressed)

    return True
