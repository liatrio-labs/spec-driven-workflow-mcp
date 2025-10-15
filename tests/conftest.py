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

        (prompts_dir / "generate-spec.md").write_text(
            """---
name: generate-spec
title: Generate Specification
description: Generate a Specification (Spec) for a feature
tags:
  - planning
  - specification
arguments: []
meta:
  category: spec-development
---

# Generate Specification
"""
        )

        (prompts_dir / "generate-task-list-from-spec.md").write_text(
            """---
name: generate-task-list-from-spec
title: Generate Task List From Spec
description: Generate a task list from a Spec
tags:
  - planning
  - tasks
arguments: []
meta:
  category: spec-development
---

# Generate Task List
"""
        )

        (prompts_dir / "manage-tasks.md").write_text(
            """---
name: manage-tasks
title: Manage Tasks
description: Guidelines for managing task lists and working on tasks/subtasks
tags:
  - execution
  - tasks
arguments: []
meta:
  category: task-management
allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch
---

# Manage Tasks
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
