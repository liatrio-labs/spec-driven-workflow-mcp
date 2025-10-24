"""Configuration models for slash command generation."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import Enum


class CommandFormat(str, Enum):
    """Supported slash command file formats."""

    MARKDOWN = "markdown"
    TOML = "toml"


@dataclass(frozen=True)
class AgentConfig:
    """Metadata describing how to generate commands for a specific agent."""

    key: str
    display_name: str
    command_dir: str
    command_format: CommandFormat
    command_file_extension: str
    detection_dirs: tuple[str, ...]

    def iter_detection_dirs(self) -> Iterable[str]:
        """Return an iterator over configured detection directories."""

        return iter(self.detection_dirs)


_SUPPORTED_AGENT_DATA: tuple[tuple[str, str, str, CommandFormat, str, tuple[str, ...]], ...] = (
    ("claude-code", "Claude Code", ".claude/commands", CommandFormat.MARKDOWN, ".md", (".claude",)),
    (
        "vs-code",
        "VS Code",
        ".config/Code/User/prompts",
        CommandFormat.MARKDOWN,
        ".prompt.md",
        (".config/Code",),
    ),
    ("codex-cli", "Codex CLI", ".codex/prompts", CommandFormat.MARKDOWN, ".md", (".codex",)),
    (
        "cursor",
        "Cursor",
        ".cursor/commands",
        CommandFormat.MARKDOWN,
        ".md",
        (".cursor",),
    ),
    ("gemini-cli", "Gemini CLI", ".gemini/commands", CommandFormat.TOML, ".toml", (".gemini",)),
    (
        "windsurf",
        "Windsurf",
        ".codeium/windsurf/global_workflows",
        CommandFormat.MARKDOWN,
        ".md",
        (".codeium", ".codeium/windsurf"),
    ),
    (
        "opencode",
        "OpenCode CLI",
        ".config/opencode/command",
        CommandFormat.MARKDOWN,
        ".md",
        (".opencode",),
    ),
)

_SORTED_AGENT_DATA = tuple(sorted(_SUPPORTED_AGENT_DATA, key=lambda item: item[0]))

SUPPORTED_AGENTS: tuple[AgentConfig, ...] = tuple(
    AgentConfig(
        key=key,
        display_name=display_name,
        command_dir=command_dir,
        command_format=command_format,
        command_file_extension=command_file_extension,
        detection_dirs=detection_dirs,
    )
    for (
        key,
        display_name,
        command_dir,
        command_format,
        command_file_extension,
        detection_dirs,
    ) in _SORTED_AGENT_DATA
)

_AGENT_LOOKUP: Mapping[str, AgentConfig] = {agent.key: agent for agent in SUPPORTED_AGENTS}


def list_agent_keys() -> tuple[str, ...]:
    """Return the keys for all supported agents in order."""

    return tuple(agent.key for agent in SUPPORTED_AGENTS)


def get_agent_config(key: str) -> AgentConfig:
    """Return configuration for the requested agent key."""

    try:
        return _AGENT_LOOKUP[key]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise KeyError(f"Unsupported agent: {key}") from exc
