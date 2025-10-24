"""Tests for slash command configuration data models."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable
from typing import get_type_hints

import pytest

from slash_commands.config import SUPPORTED_AGENTS, AgentConfig, CommandFormat

EXPECTED_AGENTS: dict[str, dict[str, object]] = {
    "claude-code": {
        "display_name": "Claude Code",
        "command_dir": ".claude/commands",
        "command_format": CommandFormat.MARKDOWN,
        "command_file_extension": ".md",
        "detection_dirs": (".claude",),
    },
    "codex-cli": {
        "display_name": "Codex CLI",
        "command_dir": ".codex/prompts",
        "command_format": CommandFormat.MARKDOWN,
        "command_file_extension": ".md",
        "detection_dirs": (".codex",),
    },
    "cursor": {
        "display_name": "Cursor",
        "command_dir": ".cursor/commands",
        "command_format": CommandFormat.MARKDOWN,
        "command_file_extension": ".md",
        "detection_dirs": (".cursor",),
    },
    "gemini-cli": {
        "display_name": "Gemini CLI",
        "command_dir": ".gemini/commands",
        "command_format": CommandFormat.TOML,
        "command_file_extension": ".toml",
        "detection_dirs": (".gemini",),
    },
    "opencode": {
        "display_name": "OpenCode CLI",
        "command_dir": ".config/opencode/command",
        "command_format": CommandFormat.MARKDOWN,
        "command_file_extension": ".md",
        "detection_dirs": (".opencode",),
    },
    "vs-code": {
        "display_name": "VS Code",
        "command_dir": ".config/Code/User/prompts",
        "command_format": CommandFormat.MARKDOWN,
        "command_file_extension": ".prompt.md",
        "detection_dirs": (".config/Code",),
    },
    "windsurf": {
        "display_name": "Windsurf",
        "command_dir": ".codeium/windsurf/global_workflows",
        "command_format": CommandFormat.MARKDOWN,
        "command_file_extension": ".md",
        "detection_dirs": (".codeium", ".codeium/windsurf"),
    },
}


@pytest.fixture(scope="module")
def supported_agents_by_key() -> dict[str, AgentConfig]:
    return {agent.key: agent for agent in SUPPORTED_AGENTS}


def test_command_format_defines_markdown_and_toml():
    assert CommandFormat.MARKDOWN.value == "markdown"
    assert CommandFormat.TOML.value == "toml"
    assert {member.value for member in CommandFormat} == {"markdown", "toml"}


def test_agent_config_is_frozen_dataclass():
    assert dataclasses.is_dataclass(AgentConfig)
    params = getattr(AgentConfig, "__dataclass_params__", None)
    assert params is not None and params.frozen is True


@pytest.mark.parametrize(
    "field_name, field_type",
    [
        ("key", str),
        ("display_name", str),
        ("command_dir", str),
        ("command_format", CommandFormat),
        ("command_file_extension", str),
        ("detection_dirs", tuple[str, ...]),
    ],
)
def test_agent_config_has_expected_field_types(field_name: str, field_type: object):
    field_types = get_type_hints(AgentConfig)
    assert field_name in field_types
    assert field_types[field_name] == field_type


def test_supported_agents_is_tuple_sorted_by_key():
    assert isinstance(SUPPORTED_AGENTS, tuple)
    keys = tuple(agent.key for agent in SUPPORTED_AGENTS)
    assert keys == tuple(sorted(keys))


def test_supported_agents_match_expected_configuration(
    supported_agents_by_key: dict[str, AgentConfig],
):
    assert set(supported_agents_by_key) == set(EXPECTED_AGENTS)
    for key, expected in EXPECTED_AGENTS.items():
        agent = supported_agents_by_key[key]
        for attribute, value in expected.items():
            assert getattr(agent, attribute) == value, f"Unexpected {attribute} for {key}"
        assert (
            agent.command_dir.endswith("/commands")
            or agent.command_dir.endswith("/prompts")
            or agent.command_dir.endswith("/global_workflows")
            or agent.command_dir.endswith("/command")
        )
        assert agent.command_file_extension.startswith(".")
        assert isinstance(agent.detection_dirs, tuple)
        assert all(dir_.startswith(".") for dir_ in agent.detection_dirs)


def test_supported_agents_include_all_markdown_and_toml_formats(
    supported_agents_by_key: dict[str, AgentConfig],
):
    markdown_agents = [
        agent
        for agent in supported_agents_by_key.values()
        if agent.command_format is CommandFormat.MARKDOWN
    ]
    toml_agents = [
        agent
        for agent in supported_agents_by_key.values()
        if agent.command_format is CommandFormat.TOML
    ]
    assert len(markdown_agents) == 6
    assert len(toml_agents) == 1


def test_detection_dirs_cover_command_directory_roots(
    supported_agents_by_key: dict[str, AgentConfig],
):
    for agent in supported_agents_by_key.values():
        # For nested paths like .config/opencode/commands, check parent directories
        if "/" in agent.command_dir:
            path_parts = agent.command_dir.split("/")
            # Check first directory component
            command_root = path_parts[0]
            # For vs-code, check if .config exists in detection_dirs
            if agent.key == "vs-code":
                assert ".config" in agent.detection_dirs or ".config/Code" in agent.detection_dirs
            elif agent.key == "windsurf":
                assert (
                    ".codeium" in agent.detection_dirs
                    or ".codeium/windsurf" in agent.detection_dirs
                )
            elif agent.key == "opencode":
                assert ".opencode" in agent.detection_dirs
            else:
                assert command_root in agent.detection_dirs
        else:
            command_root = agent.command_dir.split("/", 1)[0]
            assert command_root in agent.detection_dirs
        assert isinstance(agent.detection_dirs, Iterable)
