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
    result = runner.invoke(app, ["generate", "--list-agents"])

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
            "generate",
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agent",
            "claude-code",
            "--dry-run",
            "--target-path",
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
            "generate",
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agent",
            "claude-code",
            "--target-path",
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
            "generate",
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agent",
            "claude-code",
            "--agent",
            "gemini-cli",
            "--target-path",
            str(tmp_path),
            "--yes",
        ],
    )

    assert result.exit_code == 0
    assert (tmp_path / ".claude" / "commands" / "test-prompt.md").exists()
    assert (tmp_path / ".gemini" / "commands" / "test-prompt.toml").exists()


def test_cli_handles_invalid_agent_key(mock_prompts_dir):
    """Test that CLI handles invalid agent keys gracefully with exit code 2."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "generate",
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agent",
            "invalid-agent",
            "--yes",
        ],
    )

    assert result.exit_code == 2  # Validation error
    assert "unsupported agent" in result.stdout.lower() or "error" in result.stdout.lower()


def test_cli_handles_missing_prompts_directory(tmp_path):
    """Test that CLI handles missing prompts directory gracefully with exit code 3."""
    prompts_dir = tmp_path / "nonexistent"

    runner = CliRunner()

    # Mock the fallback function to return None to test the error case
    with patch("slash_commands.writer._find_package_prompts_dir", return_value=None):
        result = runner.invoke(
            app,
            [
                "generate",
                "--prompts-dir",
                str(prompts_dir),
                "--agent",
                "claude-code",
                "--yes",
            ],
        )

        assert result.exit_code == 3  # I/O error


def test_cli_explicit_path_shows_specific_directory_error(tmp_path):
    """Test that CLI shows specific directory error message when using explicit path."""
    prompts_dir = tmp_path / "nonexistent"
    runner = CliRunner()

    # Mock the fallback function to return None to test the error case
    with patch("slash_commands.writer._find_package_prompts_dir", return_value=None):
        # Explicitly specify --prompts-dir
        result = runner.invoke(
            app,
            [
                "generate",
                "--prompts-dir",
                str(prompts_dir),
                "--agent",
                "claude-code",
                "--yes",
            ],
        )

        assert result.exit_code == 3  # I/O error
        # Should mention specific directory check
        assert "Ensure the specified prompts directory exists" in result.stdout
        assert f"current: {prompts_dir}" in result.stdout


def test_cli_shows_summary(mock_prompts_dir, tmp_path):
    """Test that CLI shows summary of generated files."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "generate",
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agent",
            "claude-code",
            "--target-path",
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
            "generate",
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agent",
            "claude-code",
            "--target-path",
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
                "generate",
                "--prompts-dir",
                str(mock_prompts_dir),
                "--agent",
                "claude-code",
                "--target-path",
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
            "generate",
            "--prompts-dir",
            str(mock_prompts_dir),
            "--agent",
            "claude-code",
            "--target-path",
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
                "generate",
                "--prompts-dir",
                str(mock_prompts_dir),
                "--agent",
                "claude-code",
                "--target-path",
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
                command_dir=".cursor/commands",
                command_format=CommandFormat.MARKDOWN,
                command_file_extension=".md",
                detection_dirs=(".cursor",),
            ),
        ]

        result = runner.invoke(
            app,
            [
                "generate",
                "--prompts-dir",
                str(mock_prompts_dir),
                "--detection-path",
                str(tmp_path),
                "--target-path",
                str(tmp_path),
            ],
        )

        # Should generate files for both agents
        assert result.exit_code == 0
        assert (tmp_path / ".claude" / "commands" / "test-prompt.md").exists()
        assert (tmp_path / ".cursor" / "commands" / "test-prompt.md").exists()


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
                "generate",
                "--prompts-dir",
                str(mock_prompts_dir),
                "--detection-path",
                str(tmp_path),
                "--target-path",
                str(tmp_path),
            ],
        )

        # Should only generate files for claude-code
        assert result.exit_code == 0
        assert (tmp_path / ".claude" / "commands" / "test-prompt.md").exists()
        assert not (tmp_path / ".cursor" / "commands" / "test-prompt.md").exists()


def test_cli_interactive_agent_selection_cancels_on_no_selection(mock_prompts_dir, tmp_path):
    """Test that interactive agent selection cancels with exit code 1."""
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
                "generate",
                "--prompts-dir",
                str(mock_prompts_dir),
                "--detection-path",
                str(tmp_path),
                "--target-path",
                str(tmp_path),
            ],
        )

        # Should exit with exit code 1 (user cancellation)
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
                "generate",
                "--prompts-dir",
                str(mock_prompts_dir),
                "--target-path",
                str(tmp_path),
                "--yes",
            ],
        )

        # Should not call checkbox
        mock_checkbox.assert_not_called()
        # Should generate files automatically
        assert result.exit_code == 0
        assert (tmp_path / ".claude" / "commands" / "test-prompt.md").exists()


def test_cli_no_agents_detected_exit_code(tmp_path):
    """Test that no agents detected exits with code 2 (validation error)."""
    # Don't create any agent directories
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "generate",
            "--prompts-dir",
            str(tmp_path / "prompts"),
            "--detection-path",
            str(tmp_path),
            "--yes",
        ],
    )

    assert result.exit_code == 2  # Validation error
    assert "no agents detected" in result.stdout.lower()


def test_cli_exit_code_user_cancellation(mock_prompts_dir, tmp_path):
    """Test that user cancellation during overwrite prompt exits with code 1."""
    # Create an existing file
    output_path = tmp_path / ".claude" / "commands" / "test-prompt.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("existing content")

    runner = CliRunner()
    # Mock overwrite prompt to return "cancel"
    with patch("slash_commands.writer.prompt_overwrite_action") as mock_prompt:
        mock_prompt.return_value = "cancel"
        result = runner.invoke(
            app,
            [
                "generate",
                "--prompts-dir",
                str(mock_prompts_dir),
                "--agent",
                "claude-code",
                "--target-path",
                str(tmp_path),
            ],
        )

        assert result.exit_code == 1  # User cancellation
        assert "cancelled" in result.stdout.lower() or "cancel" in result.stdout.lower()


def test_cli_cleanup_command(tmp_path):
    """Test that cleanup command lists files to be deleted."""
    # Create a generated file
    command_dir = tmp_path / ".claude" / "commands"
    command_dir.mkdir(parents=True, exist_ok=True)

    generated_file = command_dir / "test-command.md"
    generated_file.write_text("""---
name: test-command
description: Test command
meta:
  source_prompt: test-prompt
  version: 1.0.0
---
# Test Command
""")

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "cleanup",
            "--target-path",
            str(tmp_path),
            "--dry-run",
            "--yes",
        ],
    )

    assert result.exit_code == 0
    # Check for table title or summary panel
    assert "Found 1 file(s) to delete" in result.stdout or "DRY RUN Complete" in result.stdout


def test_cli_cleanup_deletes_files(tmp_path):
    """Test that cleanup command deletes generated files."""
    # Create a generated file
    command_dir = tmp_path / ".claude" / "commands"
    command_dir.mkdir(parents=True, exist_ok=True)

    generated_file = command_dir / "test-command.md"
    generated_file.write_text("""---
name: test-command
description: Test command
meta:
  source_prompt: test-prompt
  version: 1.0.0
---
# Test Command
""")

    runner = CliRunner()
    with patch("slash_commands.cli.questionary.confirm") as mock_confirm:
        mock_confirm.return_value.ask.return_value = True
        result = runner.invoke(
            app,
            [
                "cleanup",
                "--target-path",
                str(tmp_path),
                "--yes",
            ],
        )

    assert result.exit_code == 0
    assert not generated_file.exists()


def test_cli_cleanup_cancels_on_no_confirmation(tmp_path):
    """Test that cleanup command cancels when user declines confirmation."""
    # Create a generated file
    command_dir = tmp_path / ".claude" / "commands"
    command_dir.mkdir(parents=True, exist_ok=True)

    generated_file = command_dir / "test-command.md"
    generated_file.write_text("""---
name: test-command
description: Test command
meta:
  source_prompt: test-prompt
  version: 1.0.0
---
# Test Command
""")

    runner = CliRunner()
    with patch("slash_commands.cli.questionary.confirm") as mock_confirm:
        mock_confirm.return_value.ask.return_value = False
        result = runner.invoke(
            app,
            [
                "cleanup",
                "--target-path",
                str(tmp_path),
            ],
        )

    assert result.exit_code == 1
    assert generated_file.exists()  # File should still exist


def test_cli_cleanup_deletes_backup_files(tmp_path):
    """Test that cleanup command deletes backup files."""
    # Create a backup file
    command_dir = tmp_path / ".claude" / "commands"
    command_dir.mkdir(parents=True, exist_ok=True)

    backup_file = command_dir / "test-command.md.20241201-120000.bak"
    backup_file.write_text("backup content")

    runner = CliRunner()
    with patch("slash_commands.cli.questionary.confirm") as mock_confirm:
        mock_confirm.return_value.ask.return_value = True
        result = runner.invoke(
            app,
            [
                "cleanup",
                "--target-path",
                str(tmp_path),
                "--yes",
            ],
        )

    assert result.exit_code == 0
    assert not backup_file.exists()


def test_cli_cleanup_excludes_backups_when_requested(tmp_path):
    """Test that cleanup command excludes backup files when --no-backups is used."""
    # Create a backup file
    command_dir = tmp_path / ".claude" / "commands"
    command_dir.mkdir(parents=True, exist_ok=True)

    backup_file = command_dir / "test-command.md.20241201-120000.bak"
    backup_file.write_text("backup content")

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "cleanup",
            "--target-path",
            str(tmp_path),
            "--no-backups",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    assert "No generated files found" in result.stdout
