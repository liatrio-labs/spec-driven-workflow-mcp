"""Centralized version management for the project.

This module reads the version from pyproject.toml to ensure a single source of truth.
"""

from __future__ import annotations

import tomllib
from pathlib import Path


def _get_version() -> str:
    """Get the version from pyproject.toml."""
    pyproject_path = Path(__file__).parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


__version__ = _get_version()
