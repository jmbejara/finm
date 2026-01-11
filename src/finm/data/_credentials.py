"""Credential handling utilities for data module.

Provides credential resolution with the following precedence:
1. CLI argument (highest priority)
2. Environment variable
3. .env file
4. Interactive prompt (if terminal available)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def get_credentials(
    wrds_username: Optional[str] = None,
    env_file: Optional[Path] = None,
    interactive: bool = True,
) -> dict[str, Optional[str]]:
    """Get credentials with precedence: CLI arg > env var > .env file > interactive.

    Parameters
    ----------
    wrds_username : str, optional
        WRDS username from CLI argument (highest priority).
    env_file : Path, optional
        Path to .env file. Defaults to .env in current directory.
    interactive : bool, default True
        If True and credential not found, prompt user interactively.

    Returns
    -------
    dict
        Dictionary with credential keys and values.
    """
    # Load .env file (lowest precedence, loaded into os.environ)
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()

    # Resolve WRDS username with precedence
    resolved_wrds_username = (
        wrds_username  # CLI arg (highest)
        or os.environ.get("WRDS_USERNAME")  # Env var or .env (middle)
    )

    # Interactive prompt if still not found
    if not resolved_wrds_username and interactive and _is_interactive():
        resolved_wrds_username = _prompt_for_credential("WRDS username")

    credentials = {
        "wrds_username": resolved_wrds_username,
        "data_dir": os.environ.get("DATA_DIR"),
    }

    return credentials


def get_data_dir(
    data_dir: Optional[str | Path] = None,
    env_file: Optional[Path] = None,
) -> Path:
    """Get data directory with precedence: argument > env var > .env > default.

    Parameters
    ----------
    data_dir : str or Path, optional
        Data directory from argument (highest priority).
    env_file : Path, optional
        Path to .env file.

    Returns
    -------
    Path
        Resolved data directory path.
    """
    if data_dir:
        return Path(data_dir)

    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()

    env_data_dir = os.environ.get("DATA_DIR")
    if env_data_dir:
        return Path(env_data_dir)

    # Default to ./data_cache in current directory
    return Path("./data_cache")


def validate_credentials(
    required: list[str],
    credentials: dict[str, Optional[str]],
) -> None:
    """Validate that required credentials are present.

    Parameters
    ----------
    required : list[str]
        List of required credential keys.
    credentials : dict
        Dictionary of credential key-value pairs.

    Raises
    ------
    ValueError
        If any required credential is missing.
    """
    missing = [k for k in required if not credentials.get(k)]
    if missing:
        raise ValueError(
            f"Missing required credentials: {', '.join(missing)}. "
            f"Provide via CLI argument, environment variable, or .env file."
        )


def _is_interactive() -> bool:
    """Check if we're running in an interactive terminal."""
    return sys.stdin.isatty() and sys.stdout.isatty()


def _prompt_for_credential(name: str) -> Optional[str]:
    """Prompt user for a credential value.

    Parameters
    ----------
    name : str
        Name of the credential to prompt for.

    Returns
    -------
    str or None
        User-provided value, or None if empty.
    """
    try:
        value = input(f"{name}: ").strip()
        return value if value else None
    except (EOFError, KeyboardInterrupt):
        return None
