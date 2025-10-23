"""Pytest fixtures for MCP server tests."""

import tempfile
from pathlib import Path
from textwrap import dedent

import pytest
from fastmcp import FastMCP

from mcp_server.prompt_utils import MarkdownPrompt, load_markdown_prompt


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
description: Generate a Specification (Spec) for a feature
tags:
  - planning
  - specification
arguments: []
meta:
  category: spec-development
---

# Generate Specification
""",
            encoding="utf-8",
        )

        (prompts_dir / "generate-task-list-from-spec.md").write_text(
            """---
name: generate-task-list-from-spec
description: Generate a task list from a Spec
tags:
  - planning
  - tasks
arguments: []
meta:
  category: spec-development
---

# Generate Task List
""",
            encoding="utf-8",
        )

        (prompts_dir / "manage-tasks.md").write_text(
            """---
name: manage-tasks
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
""",
            encoding="utf-8",
        )

        yield prompts_dir


@pytest.fixture
def mcp_server():
    """Create a basic FastMCP server instance for testing.

    Returns:
        FastMCP server instance
    """
    return FastMCP(name="test-server")


@pytest.fixture
def sample_prompt(tmp_path) -> MarkdownPrompt:
    """Return a sample Markdown prompt with arguments and overrides."""

    prompt_path = tmp_path / "sample-prompt.md"
    prompt_path.write_text(
        dedent(
            """\
            ---
            name: sample-prompt
            description: Sample prompt showcasing arguments and overrides
            tags:
              - testing
              - generators
            arguments:
              - name: primary_input
                description: Main instruction for the command
                required: true
              - name: secondary_flag
                description: Toggle additional behaviour
                required: false
            meta:
              category: generator-tests
              command_prefix: sdd-
            agent_overrides:
              gemini-cli:
                description: Sample prompt tailored for Gemini CLI
                arguments:
                  - name: gemini_flag
                    description: Toggle for Gemini specific behaviour
                    required: false
              claude-code:
                description: Sample prompt tailored for Claude Code
            enabled: true
            ---

            # Sample Prompt

            Use the provided instructions to perform the desired action.
            """
        ),
        encoding="utf-8",
    )

    return load_markdown_prompt(prompt_path)


@pytest.fixture
def prompt_with_placeholder_body(tmp_path) -> MarkdownPrompt:
    """Return a prompt containing explicit argument placeholders in the body."""

    prompt_path = tmp_path / "prompt-with-placeholders.md"
    prompt_path.write_text(
        dedent(
            """\
            ---
            name: prompt-with-placeholders
            description: Prompt for validating placeholder substitution
            tags:
              - testing
            arguments:
              - name: query
                description: Search query to send to the agent
                required: true
              - name: format
                description: Preferred response format
                required: false
            meta:
              category: generator-tests
              command_prefix: sdd-
            agent_overrides:
              gemini-cli:
                description: Prompt with TOML specific placeholder
            ---

            # Prompt With Placeholders

            Provide guidance for

            $ARGUMENTS

            and ensure `{{args}}` are handled correctly.
            """
        ),
        encoding="utf-8",
    )

    return load_markdown_prompt(prompt_path)
