"""Centralized version management for the project.

This module reads the version from pyproject.toml to ensure a single source of truth.
"""

from __future__ import annotations

import tomllib
from importlib.metadata import version as get_package_version
from pathlib import Path


def _get_version() -> str:
    """Get the version from pyproject.toml."""
    pyproject_path = Path(__file__).parent / "pyproject.toml"
    if pyproject_path.exists():
        # Local development mode
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]
    else:
        # Installed package mode
        return get_package_version("spec-driven-development-mcp")


__version__ = _get_version()
