"""Generators for producing agent-specific slash command files."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Protocol

import tomli_w
import yaml

try:
    from __version__ import __version__
except ImportError:
    # Fallback for when installed as a package
    from importlib.metadata import version

    __version__ = version("spec-driven-development-mcp")

from mcp_server.prompt_utils import MarkdownPrompt, PromptArgumentSpec
from slash_commands.config import AgentConfig, CommandFormat


class CommandGeneratorProtocol(Protocol):
    def generate(
        self, prompt: MarkdownPrompt, agent: AgentConfig
    ) -> str:  # pragma: no cover - stub
        ...


def _apply_agent_overrides(
    prompt: MarkdownPrompt, agent: AgentConfig
) -> tuple[str, list[PromptArgumentSpec], bool]:
    """Apply agent-specific overrides to a prompt.

    Returns:
        Tuple of (description, arguments, enabled)
    """
    description = prompt.description
    arguments = prompt.arguments
    enabled = prompt.enabled

    if prompt.agent_overrides and agent.key in prompt.agent_overrides:
        overrides = prompt.agent_overrides[agent.key]
        if isinstance(overrides, dict):
            if "description" in overrides:
                description = overrides["description"]
            if "arguments" in overrides:
                # Merge base arguments with override arguments
                override_args = _normalize_override_arguments(overrides["arguments"])
                # Deduplicate by name with override precedence
                existing_names = {arg.name for arg in arguments}
                # Only add override args that don't already exist
                arguments = list(arguments) + [
                    arg for arg in override_args if arg.name not in existing_names
                ]
            if "enabled" in overrides:
                enabled = overrides["enabled"]

    return description, arguments, enabled


def _normalize_override_arguments(raw: list[dict[str, Any]]) -> list[PromptArgumentSpec]:
    """Normalize argument overrides to PromptArgumentSpec objects."""
    normalized = []
    for entry in raw:
        if isinstance(entry, dict):
            name = entry.get("name")
            if name:
                normalized.append(
                    PromptArgumentSpec(
                        name=name,
                        description=entry.get("description"),
                        required=entry.get("required", True),
                    )
                )
    return normalized


def _normalize_output(content: str) -> str:
    """Normalize whitespace and encoding in generated output.

    - Ensures consistent line endings (LF)
    - Removes trailing whitespace from lines
    - Ensures UTF-8 encoding
    - Preserves intentional blank lines

    Args:
        content: The generated content to normalize

    Returns:
        Normalized content string
    """
    # Normalize line endings to LF
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    # Remove trailing whitespace from each line, preserve intentional blank lines
    result = "\n".join(line.rstrip() for line in content.splitlines())
    if result and not result.endswith("\n"):
        result += "\n"

    return result


def _build_arguments_section_markdown(arguments: list[PromptArgumentSpec]) -> str:
    """Build a markdown-formatted arguments section."""
    if not arguments:
        return ""

    lines = []
    for arg in arguments:
        if arg.required:
            lines.append(f"- `<{arg.name}>` (required): {arg.description or ''}")
        else:
            lines.append(f"- `[{arg.name}]` (optional): {arg.description or ''}")
    return "\n".join(lines)


def _build_arguments_section_toml(arguments: list[PromptArgumentSpec]) -> str:
    """Build a TOML-formatted arguments section."""
    if not arguments:
        return "{ required = {}, optional = {} }"

    required = {}
    optional = {}
    for arg in arguments:
        if arg.required:
            required[arg.name] = arg.description or ""
        else:
            optional[arg.name] = arg.description or ""

    return f"{{ required = {required}, optional = {optional} }}"


def _replace_placeholders(
    body: str, arguments: list[PromptArgumentSpec], replace_double_braces: bool = True
) -> str:
    """Replace argument placeholders in the body text.

    Args:
        body: The body text to process
        arguments: List of argument specs
        replace_double_braces: If True, replace {{args}} with comma-separated names
    """
    result = body

    # Replace $ARGUMENTS with markdown-formatted arguments
    if "$ARGUMENTS" in result:
        args_section = _build_arguments_section_markdown(arguments)
        # Replace `$ARGUMENTS` first (with backticks), then $ARGUMENTS (without backticks)
        result = result.replace("`$ARGUMENTS`", args_section)
        result = result.replace("$ARGUMENTS", args_section)

    # Replace {{args}} with argument names (only if flag is True)
    if replace_double_braces and "{{args}}" in result:
        arg_names = [arg.name for arg in arguments]
        result = result.replace("{{args}}", ", ".join(arg_names))

    return result


class MarkdownCommandGenerator:
    """Generator for Markdown-format slash command files."""

    def generate(self, prompt: MarkdownPrompt, agent: AgentConfig) -> str:
        """Generate a Markdown-formatted command file.

        Args:
            prompt: The source prompt to generate from
            agent: The agent configuration

        Returns:
            Complete markdown file content
        """
        description, arguments, enabled = _apply_agent_overrides(prompt, agent)

        # Build frontmatter
        frontmatter = {
            "name": self._get_command_name(prompt, agent),
            "description": description,
            "tags": sorted(prompt.tags) if prompt.tags else [],
            "enabled": enabled,
            "arguments": [
                {
                    "name": arg.name,
                    "description": arg.description,
                    "required": arg.required,
                }
                for arg in arguments
            ],
            "meta": self._build_meta(prompt, agent),
        }

        # Replace placeholders in body
        body = _replace_placeholders(prompt.body, arguments, replace_double_braces=False)

        # Format as YAML frontmatter + body
        yaml_content = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
        output = f"---\n{yaml_content}---\n\n{body}\n"
        return _normalize_output(output)

    def _get_command_name(self, prompt: MarkdownPrompt, agent: AgentConfig) -> str:
        """Get the command name with optional prefix."""
        prefix = prompt.meta.get("command_prefix", "") if prompt.meta else ""
        return f"{prefix}{prompt.name}"

    def _build_meta(self, prompt: MarkdownPrompt, agent: AgentConfig) -> dict:
        """Build metadata section for the command."""
        meta = prompt.meta.copy() if prompt.meta else {}
        meta.update({
            "agent": agent.key,
            "agent_display_name": agent.display_name,
            "command_dir": agent.command_dir,
            "command_format": agent.command_format.value,
            "command_file_extension": agent.command_file_extension,
            "source_prompt": prompt.name,
            "source_path": str(prompt.path),
            "version": __version__,
            "updated_at": datetime.now(UTC).isoformat(),
        })
        return meta


class TomlCommandGenerator:
    """Generator for TOML-format slash command files (Gemini CLI spec)."""

    def generate(self, prompt: MarkdownPrompt, agent: AgentConfig) -> str:
        """Generate a TOML-formatted command file following Gemini CLI spec.

        According to https://geminicli.com/docs/cli/custom-commands/:
        - Required field: `prompt` (String)
        - Optional field: `description` (String)
        - {{args}} placeholder is preserved (not replaced)

        Args:
            prompt: The source prompt to generate from
            agent: The agent configuration

        Returns:
            Complete TOML file content
        """
        description, arguments, _enabled = _apply_agent_overrides(prompt, agent)

        # Replace $ARGUMENTS with markdown-formatted arguments
        # But preserve {{args}} placeholder for Gemini CLI context-aware injection
        prompt_text = _replace_placeholders(prompt.body, arguments, replace_double_braces=False)

        # Build TOML structure following official Gemini CLI spec
        # Only include 'description' if it exists, 'prompt' is always required
        toml_data = {"prompt": prompt_text}
        if description:
            toml_data["description"] = description

        # Add metadata fields (version tracking for our tooling)
        # These are ignored by Gemini CLI but preserved for bookkeeping
        toml_data["meta"] = {
            "version": __version__,
            "updated_at": datetime.now(UTC).isoformat(),
            "source_prompt": prompt.name,
            "agent": agent.key,
        }

        # Convert to TOML format
        output = self._dict_to_toml(toml_data)
        return _normalize_output(output)

    def _dict_to_toml(self, data: dict) -> str:
        """Convert a dict to TOML format."""
        return tomli_w.dumps(data)


class CommandGenerator:
    """Base class for command generators."""

    @staticmethod
    def create(format: CommandFormat) -> CommandGeneratorProtocol:
        """Factory method to create a generator for the specified format."""
        if format == CommandFormat.MARKDOWN:
            return MarkdownCommandGenerator()
        elif format == CommandFormat.TOML:
            return TomlCommandGenerator()
        else:
            raise ValueError(f"Unsupported command format: {format}")
