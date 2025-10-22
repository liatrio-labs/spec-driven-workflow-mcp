from __future__ import annotations

import tomllib

import pytest

from mcp_server.prompt_utils import parse_frontmatter
from slash_commands.config import get_agent_config
from slash_commands.generators import (
    MarkdownCommandGenerator,
    TomlCommandGenerator,
)


def _extract_frontmatter_and_body(content: str) -> tuple[dict, str]:
    frontmatter, body = parse_frontmatter(content)
    if not frontmatter:
        pytest.fail("Generated markdown is missing YAML frontmatter")
    return frontmatter, body


def _parse_toml(content: str) -> dict:
    try:
        return tomllib.loads(content)
    except tomllib.TOMLDecodeError as exc:  # pragma: no cover - defensive
        pytest.fail(f"Generated TOML is invalid: {exc}")


def _normalize_for_comparison(text: str) -> str:
    """Normalize text for comparison (remove extra whitespace, normalize line endings)."""
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines) + "\n"


def test_markdown_generator_applies_agent_overrides(sample_prompt):
    agent = get_agent_config("claude-code")
    generator = MarkdownCommandGenerator()

    generated = generator.generate(sample_prompt, agent)
    frontmatter, body = _extract_frontmatter_and_body(generated)

    assert frontmatter["name"] == "sdd-sample-prompt"
    assert frontmatter["description"] == "Sample prompt tailored for Claude Code"
    assert sorted(frontmatter["tags"]) == ["generators", "testing"]
    assert frontmatter["enabled"] is True

    assert frontmatter["arguments"] == [
        {
            "name": "primary_input",
            "description": "Main instruction for the command",
            "required": True,
        },
        {
            "name": "secondary_flag",
            "description": "Toggle additional behaviour",
            "required": False,
        },
    ]

    meta = frontmatter["meta"]
    assert meta["category"] == "generator-tests"
    assert meta["agent"] == "claude-code"
    assert meta["agent_display_name"] == agent.display_name
    assert meta["command_dir"] == agent.command_dir
    assert meta["command_format"] == agent.command_format.value
    assert meta["command_file_extension"] == agent.command_file_extension
    assert meta["source_prompt"] == "sample-prompt"
    assert meta["source_path"].endswith("sample-prompt.md")

    assert "Use the provided instructions" in body
    assert "$ARGUMENTS" not in body


def test_markdown_generator_replaces_arguments_placeholder(prompt_with_placeholder_body):
    agent = get_agent_config("claude-code")
    generator = MarkdownCommandGenerator()

    generated = generator.generate(prompt_with_placeholder_body, agent)
    frontmatter, body = _extract_frontmatter_and_body(generated)

    assert frontmatter["name"] == "sdd-prompt-with-placeholders"
    assert frontmatter["description"] == "Prompt for validating placeholder substitution"

    assert "$ARGUMENTS" not in body
    assert "{{args}}" in body

    lines = [line.strip() for line in body.splitlines() if line.strip()]
    argument_lines = [line for line in lines if line.startswith("-")]

    assert "- `<query>` (required): Search query to send to the agent" in argument_lines
    assert "- `[format]` (optional): Preferred response format" in argument_lines, argument_lines


def test_toml_generator_applies_agent_overrides(sample_prompt):
    agent = get_agent_config("gemini-cli")
    generator = TomlCommandGenerator()

    generated = generator.generate(sample_prompt, agent)
    data = _parse_toml(generated)

    command = data["command"]
    assert command["name"] == "sdd-sample-prompt"
    assert command["description"] == "Sample prompt tailored for Gemini CLI"
    assert command["enabled"] is True
    assert command["tags"] == ["generators", "testing"]

    meta = command["meta"]
    assert meta["category"] == "generator-tests"
    assert meta["agent"] == "gemini-cli"
    assert meta["agent_display_name"] == agent.display_name
    assert meta["command_dir"] == agent.command_dir
    assert meta["command_format"] == agent.command_format.value
    assert meta["command_file_extension"] == agent.command_file_extension
    assert meta["source_prompt"] == "sample-prompt"
    assert meta["source_path"].endswith("sample-prompt.md")

    arguments = command["arguments"]
    assert arguments["required"] == {
        "primary_input": "Main instruction for the command",
    }
    assert arguments["optional"] == {
        "secondary_flag": "Toggle additional behaviour",
        "gemini_flag": "Toggle for Gemini specific behaviour",
    }

    body_text = command["body"]["text"]
    assert body_text.startswith("# Sample Prompt")
    assert "Use the provided instructions" in body_text
    assert "{{args}}" not in body_text
    assert "$ARGUMENTS" not in body_text


def test_toml_generator_substitutes_argument_placeholders(prompt_with_placeholder_body):
    agent = get_agent_config("qwen-code")
    generator = TomlCommandGenerator()

    generated = generator.generate(prompt_with_placeholder_body, agent)
    data = _parse_toml(generated)

    command = data["command"]
    assert command["name"] == "sdd-prompt-with-placeholders"
    assert command["description"] == "Prompt with TOML specific placeholder"
    assert command["tags"] == ["testing"]

    arguments = command["arguments"]
    assert arguments["required"] == {
        "query": "Search query to send to the agent",
    }
    assert arguments["optional"] == {
        "format": "Preferred response format",
    }

    body_text = command["body"]["text"]
    assert "{{args}}" not in body_text
    assert "$ARGUMENTS" not in body_text
    assert "primary_input" not in body_text
    assert "query" in body_text
    assert "[format]" in body_text

    meta = command["meta"]
    assert meta["agent"] == "qwen-code"
    assert meta["agent_display_name"] == agent.display_name
    assert meta["command_dir"] == agent.command_dir
    assert meta["command_format"] == agent.command_format.value
    assert meta["command_file_extension"] == agent.command_file_extension


def test_markdown_generator_snapshot_regression(sample_prompt):
    """Snapshot-style test to catch unintended changes in Markdown output format."""
    agent = get_agent_config("claude-code")
    generator = MarkdownCommandGenerator()

    generated = generator.generate(sample_prompt, agent)

    # Verify the output structure is consistent
    assert generated.startswith("---\n")
    assert "\n---\n" in generated
    assert generated.endswith("\n")

    # Verify no trailing whitespace in lines
    lines = generated.splitlines()
    for line in lines:
        assert line == line.rstrip(), "Line contains trailing whitespace"

    # Verify consistent line endings (LF only)
    assert "\r" not in generated


def test_toml_generator_snapshot_regression(sample_prompt):
    """Snapshot-style test to catch unintended changes in TOML output format."""
    agent = get_agent_config("gemini-cli")
    generator = TomlCommandGenerator()

    generated = generator.generate(sample_prompt, agent)

    # Verify the output structure is consistent
    assert generated.startswith("[command]")
    assert generated.endswith("\n")

    # Verify no trailing whitespace in lines
    lines = generated.splitlines()
    for line in lines:
        assert line == line.rstrip(), "Line contains trailing whitespace"

    # Verify consistent line endings (LF only)
    assert "\r" not in generated

    # Verify valid TOML structure
    data = _parse_toml(generated)
    assert "command" in data
    assert isinstance(data["command"], dict)
