# utils.py
"""
DIRAI Utility Functions
"""

import re
import sys
from pathlib import Path
from typing import Union
import pathspec

def is_binary(file_path: Union[str, Path]) -> bool:
    """Check if a file is binary"""
    try:
        with open(file_path, 'rb') as f:
            return b'\x00' in f.read(1024)
    except Exception:
        return True

def redact_sensitive_data(line: str, ignore_variables: list, redaction_patterns: list) -> str:
    """
    Redact sensitive information from text lines
    Args:
        line: Input text line
        ignore_variables: List of variable names to ignore
        redaction_patterns: List of patterns to redact
    Returns:
        Redacted text line
    """
    # Redact variables from ignore list
    for var in ignore_variables:
        line = re.sub(
            fr'(\b{re.escape(var)}\b\s*[:=]\s*)(["\']?)([^"\'\n]+)(["\']?)',
            r'\1\2\4',  # Preserve quotes but empty the value
            line,
            flags=re.IGNORECASE
        )

    # Redact common patterns
    for pattern in redaction_patterns:
        line = re.sub(
            fr'(\b{pattern}\b\s*[:=]\s*)(["\']?)([^"\'\n]+)(["\']?)',
            r'\1\2\4',
            line,
            flags=re.IGNORECASE
        )

    return line

def validate_config(config: dict) -> None:
    """Validate configuration parameters"""
    required_keys = ['exclude', 'output']
    for key in required_keys:
        if key not in config.get('default', {}): # fix: check in default profile
            raise ValueError(f"Missing required config key: {key}")

    if config.get('max_depth', 0) < 0:
        raise ValueError("max_depth cannot be negative")

def display_error(message: str, exit_code: int = 1) -> None:
    """Display error message and exit"""
    sys.stderr.write(f"\nERROR: {message}\n")
    sys.exit(exit_code)

def normalize_path(path: Union[str, Path]) -> Path:
    """Convert to absolute path and resolve symlinks"""
    path = Path(path).expanduser()
    return path.resolve()

def should_ignore_path(path: Path, ignore_patterns: list) -> bool:
    """Check if path matches any ignore patterns"""
    spec = pathspec.PathSpec.from_lines('gitwildmatch', ignore_patterns)
    return spec.match_file(str(path))