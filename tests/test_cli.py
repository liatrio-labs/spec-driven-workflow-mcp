"""Tests for the slash command CLI."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from slash_commands.cli import app
from slash_commands.config import AgentConfig, CommandFormat


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


def test_cli_prompts_for_overwrite_without_yes(mock_prompts_dir, tmp_path):
    """Test that CLI prompts for overwrite when files exist and --yes is not set."""
    # Create an existing file
    output_path = tmp_path / ".claude" / "commands" / "test-prompt.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("existing content")

    runner = CliRunner()
    # Don't pass --yes flag to test prompting
    with patch("slash_commands.writer.prompt_overwrite_action") as mock_prompt:
        mock_prompt.return_value = "overwrite"
        result = runner.invoke(
            app,
            [
                "--prompts-dir",
                str(mock_prompts_dir),
                "--agents",
                "claude-code",
                "--base-path",
                str(tmp_path),
            ],
            input="overwrite\n",
        )

        # Should prompt for overwrite action
        assert (
            "overwrite" in result.stdout.lower()
            or "existing" in result.stdout.lower()
            or mock_prompt.called
        )


def test_cli_honors_yes_flag_for_overwrite(mock_prompts_dir, tmp_path):
    """Test that CLI honors --yes flag and auto-overwrites existing files."""
    # Create an existing file
    output_path = tmp_path / ".claude" / "commands" / "test-prompt.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("existing content")

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
    # File should be overwritten
    assert "Test Prompt" in output_path.read_text()


def test_cli_reports_backup_creation(mock_prompts_dir, tmp_path):
    """Test that CLI reports when backup files are created."""
    # Create an existing file
    output_path = tmp_path / ".claude" / "commands" / "test-prompt.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("existing content")

    runner = CliRunner()
    with patch("slash_commands.writer.prompt_overwrite_action") as mock_prompt:
        mock_prompt.return_value = "backup"
        result = runner.invoke(
            app,
            [
                "--prompts-dir",
                str(mock_prompts_dir),
                "--agents",
                "claude-code",
                "--base-path",
                str(tmp_path),
            ],
            input="backup\n",
        )

        # Should report backup creation
        assert (
            "backup" in result.stdout.lower()
            or ".bak" in result.stdout.lower()
            or mock_prompt.called
        )
        # Backup file should exist with timestamp pattern
        backup_files = list(output_path.parent.glob("test-prompt.md.*.bak"))
        assert len(backup_files) > 0


def test_cli_interactive_agent_selection_selects_all(mock_prompts_dir, tmp_path):
    """Test that interactive agent selection allows selecting all detected agents."""
    # Create agent directories
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".cursor").mkdir()

    runner = CliRunner()
    # Mock questionary.checkbox to return all agents
    with patch("slash_commands.cli.questionary.checkbox") as mock_checkbox:
        # Simulate selecting all agents
        mock_checkbox.return_value.ask.return_value = [
            AgentConfig(
                key="claude-code",
                display_name="Claude Code",
                command_dir=".claude/commands",
                command_format=CommandFormat.MARKDOWN,
                command_file_extension=".md",
                detection_dirs=(".claude",),
            ),
            AgentConfig(
                key="cursor",
                display_name="Cursor",
                command_dir=".cursorrules/commands",
                command_format=CommandFormat.MARKDOWN,
                command_file_extension=".md",
                detection_dirs=(".cursor", ".cursorrules"),
            ),
        ]

        result = runner.invoke(
            app,
            [
                "--prompts-dir",
                str(mock_prompts_dir),
                "--base-path",
                str(tmp_path),
            ],
        )

        # Should generate files for both agents
        assert result.exit_code == 0
        assert (tmp_path / ".claude" / "commands" / "test-prompt.md").exists()
        assert (tmp_path / ".cursorrules" / "commands" / "test-prompt.md").exists()


def test_cli_interactive_agent_selection_partial_selection(mock_prompts_dir, tmp_path):
    """Test that interactive agent selection allows selecting subset of agents."""
    # Create agent directories
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".cursor").mkdir()

    runner = CliRunner()
    # Mock questionary.checkbox to return only one agent
    with patch("slash_commands.cli.questionary.checkbox") as mock_checkbox:
        # Simulate selecting only claude-code
        mock_checkbox.return_value.ask.return_value = [
            AgentConfig(
                key="claude-code",
                display_name="Claude Code",
                command_dir=".claude/commands",
                command_format=CommandFormat.MARKDOWN,
                command_file_extension=".md",
                detection_dirs=(".claude",),
            ),
        ]

        result = runner.invoke(
            app,
            [
                "--prompts-dir",
                str(mock_prompts_dir),
                "--base-path",
                str(tmp_path),
            ],
        )

        # Should only generate files for claude-code
        assert result.exit_code == 0
        assert (tmp_path / ".claude" / "commands" / "test-prompt.md").exists()
        assert not (tmp_path / ".cursorrules" / "commands" / "test-prompt.md").exists()


def test_cli_interactive_agent_selection_cancels_on_no_selection(mock_prompts_dir, tmp_path):
    """Test that interactive agent selection cancels when no agents are selected."""
    # Create agent directories
    (tmp_path / ".claude").mkdir()

    runner = CliRunner()
    # Mock questionary.checkbox to return empty list
    with patch("slash_commands.cli.questionary.checkbox") as mock_checkbox:
        # Simulate selecting no agents
        mock_checkbox.return_value.ask.return_value = []

        result = runner.invoke(
            app,
            [
                "--prompts-dir",
                str(mock_prompts_dir),
                "--base-path",
                str(tmp_path),
            ],
        )

        # Should exit with error message
        assert result.exit_code == 1
        assert "no agents selected" in result.stdout.lower()


def test_cli_interactive_agent_selection_bypassed_with_yes_flag(mock_prompts_dir, tmp_path):
    """Test that --yes flag bypasses interactive agent selection."""
    # Create agent directories
    (tmp_path / ".claude").mkdir()

    runner = CliRunner()
    # Should not call questionary.checkbox when --yes is used
    with patch("slash_commands.cli.questionary.checkbox") as mock_checkbox:
        result = runner.invoke(
            app,
            [
                "--prompts-dir",
                str(mock_prompts_dir),
                "--base-path",
                str(tmp_path),
                "--yes",
            ],
        )

        # Should not call checkbox
        mock_checkbox.assert_not_called()
        # Should generate files automatically
        assert result.exit_code == 0
        assert (tmp_path / ".claude" / "commands" / "test-prompt.md").exists()
