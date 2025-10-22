"""Tests for the slash command writer."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mcp_server.prompt_utils import MarkdownPrompt
from slash_commands.config import CommandFormat
from slash_commands.writer import SlashCommandWriter


@pytest.fixture
def mock_prompt_load(tmp_path):
    """Create a mock prompt loader that returns sample prompts."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    # Create a sample prompt file
    prompt_file = prompts_dir / "test-prompt.md"
    prompt_file.write_text(
        """---
name: test-prompt
description: Test prompt for writer tests
tags:
  - testing
arguments: []
enabled: true
---
# Test Prompt

This is a test prompt.
"""
    )

    def load_prompts(dir_path: Path):
        return [
            MarkdownPrompt(
                path=prompt_file,
                name="test-prompt",
                description="Test prompt for writer tests",
                tags={"testing"},
                meta=None,
                enabled=True,
                arguments=[],
                body="# Test Prompt\n\nThis is a test prompt.",
                agent_overrides=None,
            )
        ]

    return prompts_dir, load_prompts


def test_writer_generates_command_for_single_agent(mock_prompt_load, tmp_path):
    """Test that writer generates command file for a single agent."""
    prompts_dir, _load_prompts = mock_prompt_load

    writer = SlashCommandWriter(
        prompts_dir=prompts_dir,
        agents=["claude-code"],
        dry_run=False,
        base_path=tmp_path,
    )

    result = writer.generate()

    # Verify that a file was created
    expected_path = tmp_path / ".claude" / "commands" / "test-prompt.md"
    assert expected_path.exists()
    assert "Test Prompt" in expected_path.read_text()

    # Verify result structure
    assert result["files_written"] == 1
    assert len(result["files"]) == 1
    assert result["files"][0]["path"] == str(expected_path)
    assert result["files"][0]["agent"] == "claude-code"


def test_writer_generates_commands_for_multiple_agents(mock_prompt_load, tmp_path):
    """Test that writer generates command files for multiple agents."""
    prompts_dir, _load_prompts = mock_prompt_load

    writer = SlashCommandWriter(
        prompts_dir=prompts_dir,
        agents=["claude-code", "gemini-cli"],
        dry_run=False,
        base_path=tmp_path,
    )

    result = writer.generate()

    # Verify that files were created for both agents
    claude_path = tmp_path / ".claude" / "commands" / "test-prompt.md"
    gemini_path = tmp_path / ".gemini" / "commands" / "test-prompt.toml"

    assert claude_path.exists()
    assert gemini_path.exists()

    # Verify result structure
    assert result["files_written"] == 2
    assert len(result["files"]) == 2


def test_writer_respects_dry_run_flag(mock_prompt_load, tmp_path):
    """Test that writer doesn't create files when dry_run is True."""
    prompts_dir, _load_prompts = mock_prompt_load

    writer = SlashCommandWriter(
        prompts_dir=prompts_dir,
        agents=["claude-code"],
        dry_run=True,
        base_path=tmp_path,
    )

    result = writer.generate()

    # Verify that no files were created
    expected_path = tmp_path / ".claude" / "commands" / "test-prompt.md"
    assert not expected_path.exists()

    # Verify result structure still reports what would be written
    assert result["files_written"] == 0
    assert len(result["files"]) == 1
    assert result["files"][0]["path"] == str(expected_path)


def test_writer_creates_parent_directories(mock_prompt_load, tmp_path):
    """Test that writer creates parent directories if they don't exist."""
    prompts_dir, _load_prompts = mock_prompt_load

    writer = SlashCommandWriter(
        prompts_dir=prompts_dir,
        agents=["claude-code"],
        dry_run=False,
        base_path=tmp_path,
    )

    writer.generate()

    # Verify that parent directory was created
    expected_dir = tmp_path / ".claude" / "commands"
    assert expected_dir.exists()
    assert expected_dir.is_dir()


def test_writer_calls_generator_with_correct_agent(mock_prompt_load, tmp_path):
    """Test that writer calls generator with correct agent configuration."""
    prompts_dir, _load_prompts = mock_prompt_load

    with patch("slash_commands.writer.CommandGenerator") as mock_generator_class:
        mock_generator = MagicMock()
        mock_generator.generate.return_value = "---\nname: test-prompt\n---\n\n# Test Prompt"
        mock_generator_class.create.return_value = mock_generator

        writer = SlashCommandWriter(
            prompts_dir=prompts_dir,
            agents=["claude-code"],
            dry_run=False,
            base_path=tmp_path,
        )

        writer.generate()

        # Verify generator was called with correct agent
        mock_generator_class.create.assert_called_once_with(CommandFormat.MARKDOWN)
        assert mock_generator.generate.called


def test_writer_loads_prompts_from_directory(mock_prompt_load, tmp_path):
    """Test that writer loads prompts from the specified directory."""
    prompts_dir, _load_prompts = mock_prompt_load

    writer = SlashCommandWriter(
        prompts_dir=prompts_dir,
        agents=["claude-code"],
        dry_run=False,
        base_path=tmp_path,
    )

    result = writer.generate()

    # Verify that prompts were loaded
    assert result["prompts_loaded"] == 1
    assert len(result["prompts"]) == 1
    assert result["prompts"][0]["name"] == "test-prompt"


def test_writer_handles_missing_prompts_directory(tmp_path):
    """Test that writer handles missing prompts directory gracefully."""
    prompts_dir = tmp_path / "nonexistent"

    writer = SlashCommandWriter(
        prompts_dir=prompts_dir,
        agents=["claude-code"],
        dry_run=False,
        base_path=tmp_path,
    )

    with pytest.raises(ValueError, match="Prompts directory does not exist"):
        writer.generate()


def test_writer_handles_invalid_agent_key(mock_prompt_load, tmp_path):
    """Test that writer handles invalid agent keys gracefully."""
    prompts_dir, _load_prompts = mock_prompt_load

    writer = SlashCommandWriter(
        prompts_dir=prompts_dir,
        agents=["invalid-agent"],
        dry_run=False,
        base_path=tmp_path,
    )

    with pytest.raises(KeyError, match="Unsupported agent"):
        writer.generate()
