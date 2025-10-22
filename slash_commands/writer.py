"""Writer for generating slash command files for multiple agents."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import questionary

from mcp_server.prompt_utils import MarkdownPrompt, load_markdown_prompt
from slash_commands.config import AgentConfig, get_agent_config
from slash_commands.generators import CommandGenerator

OverwriteAction = Literal["cancel", "overwrite", "backup", "overwrite-all"]


def prompt_overwrite_action(file_path: Path) -> OverwriteAction:
    """Prompt user for what to do with an existing file.

    Args:
        file_path: Path to the existing file

    Returns:
        One of: "cancel", "overwrite", "backup", "overwrite-all"
    """
    response = questionary.select(
        f"File already exists: {file_path}\nWhat would you like to do?",
        choices=[
            questionary.Choice("Cancel", "cancel"),
            questionary.Choice("Overwrite this file", "overwrite"),
            questionary.Choice("Create backup and overwrite", "backup"),
            questionary.Choice("Overwrite all existing files", "overwrite-all"),
        ],
    ).ask()

    if response is None:
        # User pressed Ctrl+C or similar
        return "cancel"

    return response  # type: ignore[return-value]


def create_backup(file_path: Path) -> Path:
    """Create a timestamped backup of an existing file.

    Args:
        file_path: Path to the file to backup

    Returns:
        Path to the backup file
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = file_path.with_suffix(f"{file_path.suffix}.{timestamp}.bak")

    # Copy file with metadata preserved
    shutil.copy2(file_path, backup_path)

    return backup_path


class SlashCommandWriter:
    """Orchestrates prompt loading and generation of command files for multiple agents."""

    def __init__(
        self,
        prompts_dir: Path,
        agents: list[str] | None = None,
        dry_run: bool = False,
        base_path: Path | None = None,
        overwrite_action: OverwriteAction | None = None,
    ):
        """Initialize the writer.

        Args:
            prompts_dir: Directory containing prompt files
            agents: List of agent keys to generate commands for. If None, uses all supported agents.
            dry_run: If True, don't write files but report what would be written
            base_path: Base directory for output paths. If None, uses current directory.
            overwrite_action: Global overwrite action to apply. If None, will prompt per file.
        """
        self.prompts_dir = prompts_dir
        self.agents = agents or []
        self.dry_run = dry_run
        self.base_path = base_path or Path.cwd()
        self.overwrite_action = overwrite_action
        self._global_overwrite = False  # Track if user chose "overwrite-all"
        self._backups_created = []  # Track backup files created

    def generate(self) -> dict[str, Any]:
        """Generate command files for all configured agents.

        Returns:
            Dict with keys:
            - prompts_loaded: Number of prompts loaded
            - files_written: Number of files written
            - files: List of dicts with path and agent info
            - prompts: List of prompt metadata
        """
        # Load prompts
        prompts = self._load_prompts()

        # Get agent configs
        agent_configs = [get_agent_config(key) for key in self.agents]

        # Generate files
        files = []
        for prompt in prompts:
            for agent in agent_configs:
                file_info = self._generate_file(prompt, agent)
                if file_info:
                    files.append(file_info)

        return {
            "prompts_loaded": len(prompts),
            "files_written": sum(1 for f in files if not self.dry_run),
            "files": files,
            "prompts": [{"name": p.name, "path": str(p.path)} for p in prompts],
            "backups_created": self._backups_created,
        }

    def _load_prompts(self) -> list[MarkdownPrompt]:
        """Load all prompts from the prompts directory."""
        if not self.prompts_dir.exists():
            raise ValueError(f"Prompts directory does not exist: {self.prompts_dir}")

        prompts = []
        for prompt_file in sorted(self.prompts_dir.glob("*.md")):
            prompt = load_markdown_prompt(prompt_file)
            prompts.append(prompt)

        return prompts

    def _generate_file(self, prompt: MarkdownPrompt, agent: AgentConfig) -> dict[str, Any] | None:
        """Generate a command file for a single prompt and agent.

        Args:
            prompt: The prompt to generate from
            agent: The agent configuration

        Returns:
            Dict with path and agent info, or None if skipped
        """
        # Skip if prompt is disabled
        if not prompt.enabled:
            return None

        # Create generator for this agent's format
        generator = CommandGenerator.create(agent.command_format)

        # Generate command content
        content = generator.generate(prompt, agent)

        # Determine output path (resolve relative to base_path)
        output_path = (
            self.base_path / agent.command_dir / f"{prompt.name}{agent.command_file_extension}"
        )

        # Handle existing files
        if output_path.exists() and not self.dry_run:
            action = self._handle_existing_file(output_path)
            if action == "cancel":
                raise RuntimeError("Cancelled by user")
            elif action == "backup":
                backup_path = create_backup(output_path)
                self._backups_created.append(str(backup_path))

        # Create parent directories if needed
        if not self.dry_run:
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file if not dry run
        if not self.dry_run:
            output_path.write_text(content)

        return {
            "path": str(output_path),
            "agent": agent.key,
            "agent_display_name": agent.display_name,
            "format": agent.command_format.value,
        }

    def _handle_existing_file(self, file_path: Path) -> OverwriteAction:
        """Handle an existing file by determining what action to take.

        Args:
            file_path: Path to the existing file

        Returns:
            OverwriteAction to apply
        """
        # If global overwrite was already set, use it
        if self._global_overwrite:
            return "overwrite"

        # Use global action if set
        if self.overwrite_action == "overwrite-all":
            return "overwrite"
        elif self.overwrite_action:
            return self.overwrite_action

        # Otherwise prompt for action
        action = prompt_overwrite_action(file_path)

        # If user chose "overwrite-all", set the flag
        if action == "overwrite-all":
            self._global_overwrite = True
            return "overwrite"

        return action
