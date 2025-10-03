"""Pytest fixtures for MCP server tests."""

import tempfile
from pathlib import Path

import pytest
from fastmcp import FastMCP


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace directory for testing.

    Yields:
        Path to temporary workspace directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        (workspace / "specs").mkdir()
        (workspace / "tasks").mkdir()
        yield workspace


@pytest.fixture
def temp_prompts_dir():
    """Create a temporary prompts directory with test prompts.

    Yields:
        Path to temporary prompts directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        prompts_dir = Path(tmpdir)

        # Create test prompt files
        (prompts_dir / "test-prompt.md").write_text(
            """---
description: A test prompt
---

# Test Prompt

This is a test prompt for testing purposes.
"""
        )

        (prompts_dir / "another-prompt.md").write_text(
            """---
description: Another test prompt
---

# Another Prompt

This is another test prompt.
"""
        )

        yield prompts_dir


@pytest.fixture
def mcp_server():
    """Create a basic FastMCP server instance for testing.

    Returns:
        FastMCP server instance
    """
    return FastMCP(name="test-server")
