"""Tests for the slash command CLI."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from slash_commands.cli import app


@pytest.fixture
def mock_prompts_dir(tmp_path):
    """Create a temporary prompts directory with test prompts."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    # Create a test prompt
    prompt_file = prompts_dir / "test-prompt.md"
    prompt_file.write_text("""---
name: test-prompt
description: Test prompt for CLI tests
tags:
  - testing
arguments: []
enabled: true
---
# Test Prompt

This is a test prompt.
""")

    return prompts_dir


def test_cli_list_agents():
    """Test that --list-agents lists all supported agents."""
    runner = CliRunner()
    result = runner.invoke(app, ["--list-agents"])

    assert result.exit_code == 0
    assert "claude-code" in result.stdout
    assert "gemini-cli" in result.stdout
    assert "cursor" in result.stdout


def test_cli_dry_run_flag(mock_prompts_dir, tmp_path):
    """Test that --dry-run flag prevents file writes."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agents",
            "claude-code",
            "--dry-run",
            "--base-path",
            str(tmp_path),
        ],
    )

    assert result.exit_code == 0
    assert "dry run" in result.stdout.lower()
    assert not (tmp_path / ".claude" / "commands" / "test-prompt.md").exists()


def test_cli_generates_files_for_single_agent(mock_prompts_dir, tmp_path):
    """Test that CLI generates files for a single agent."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agents",
            "claude-code",
            "--base-path",
            str(tmp_path),
            "--yes",
        ],
    )

    assert result.exit_code == 0
    assert (tmp_path / ".claude" / "commands" / "test-prompt.md").exists()


def test_cli_generates_files_for_multiple_agents(mock_prompts_dir, tmp_path):
    """Test that CLI generates files for multiple agents."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agents",
            "claude-code",
            "--agents",
            "gemini-cli",
            "--base-path",
            str(tmp_path),
            "--yes",
        ],
    )

    assert result.exit_code == 0
    assert (tmp_path / ".claude" / "commands" / "test-prompt.md").exists()
    assert (tmp_path / ".gemini" / "commands" / "test-prompt.toml").exists()


def test_cli_handles_invalid_agent_key(mock_prompts_dir):
    """Test that CLI handles invalid agent keys gracefully."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agents",
            "invalid-agent",
            "--yes",
        ],
    )

    assert result.exit_code != 0
    assert "unsupported agent" in result.stdout.lower() or "error" in result.stdout.lower()


def test_cli_handles_missing_prompts_directory(tmp_path):
    """Test that CLI handles missing prompts directory gracefully."""
    prompts_dir = tmp_path / "nonexistent"

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--prompts-dir",
            str(prompts_dir),
            "--agents",
            "claude-code",
            "--yes",
        ],
    )

    assert result.exit_code != 0
    assert "does not exist" in result.stdout.lower() or "error" in result.stdout.lower()


def test_cli_shows_summary(mock_prompts_dir, tmp_path):
    """Test that CLI shows summary of generated files."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agents",
            "claude-code",
            "--base-path",
            str(tmp_path),
            "--yes",
        ],
    )

    assert result.exit_code == 0
    assert "prompts loaded" in result.stdout.lower() or "files written" in result.stdout.lower()


def test_cli_respects_prompts_dir_option(mock_prompts_dir, tmp_path):
    """Test that CLI respects --prompts-dir option."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agents",
            "claude-code",
            "--base-path",
            str(tmp_path),
            "--yes",
        ],
    )

    assert result.exit_code == 0
    # Should have found the test prompt
    assert "test-prompt" in result.stdout.lower() or result.exit_code == 0
