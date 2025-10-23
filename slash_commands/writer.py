"""Writer for generating slash command files for multiple agents."""

from __future__ import annotations

import re
import shutil

# tomllib is part of the Python standard library since Python 3.11
# Project requires Python 3.12+ for compatibility with all dependencies
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

import questionary
import yaml

from mcp_server.prompt_utils import MarkdownPrompt, load_markdown_prompt
from slash_commands.config import AgentConfig, get_agent_config, list_agent_keys
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
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
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
        self.agents = agents if agents is not None else list_agent_keys()
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
        files_written = 0
        for prompt in prompts:
            for agent in agent_configs:
                file_info = self._generate_file(prompt, agent)
                if file_info:
                    files.append(file_info)
                    # Only count files that were actually written (not dry run)
                    if not self.dry_run:
                        files_written += 1

        return {
            "prompts_loaded": len(prompts),
            "files_written": files_written,
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
        # Sanitize file stem: drop any path components and restrict to safe chars
        safe_stem = Path(prompt.name).name  # remove any directories
        safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "-", safe_stem).strip("-_.") or "command"
        filename = f"{safe_stem}{agent.command_file_extension}"
        output_path = self.base_path / agent.command_dir / filename

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
            output_path.write_text(content, encoding="utf-8")

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

    def find_generated_files(
        self, agents: list[str] | None = None, include_backups: bool = True
    ) -> list[dict[str, Any]]:
        """Find all files generated by this tool.

        Args:
            agents: List of agent keys to search. If None, searches all supported agents.
            include_backups: If True, includes backup files in the results.

        Returns:
            List of dicts with keys: path, agent, agent_display_name, type, reason
        """
        found_files = []
        agent_keys = list_agent_keys() if agents is None else agents

        for agent_key in agent_keys:
            try:
                agent = get_agent_config(agent_key)
                command_dir = self.base_path / agent.command_dir

                if not command_dir.exists():
                    continue

                # Check for regular command files
                for file_path in command_dir.glob(f"*{agent.command_file_extension}"):
                    if self._is_generated_file(file_path, agent):
                        found_files.append({
                            "path": str(file_path),
                            "agent": agent.key,
                            "agent_display_name": agent.display_name,
                            "type": "command",
                            "reason": "Has generated metadata",
                        })

                # Check for backup files
                if include_backups:
                    # Look for files matching the backup pattern: *.extension.timestamp.bak
                    escaped_ext = re.escape(agent.command_file_extension)
                    pattern = re.compile(rf".*{escaped_ext}\.\d{{8}}-\d{{6}}\.bak$")
                    for file_path in command_dir.iterdir():
                        if file_path.is_file() and pattern.match(file_path.name):
                            found_files.append({
                                "path": str(file_path),
                                "agent": agent.key,
                                "agent_display_name": agent.display_name,
                                "type": "backup",
                                "reason": "Matches backup pattern",
                            })
            except KeyError:
                # Agent key not found, skip
                continue

        return found_files

    def _is_generated_file(self, file_path: Path, agent: AgentConfig) -> bool:
        """Check if a file was generated by this tool.

        Args:
            file_path: Path to the file to check
            agent: Agent configuration

        Returns:
            True if the file was generated by this tool
        """
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return False

        if agent.command_format.value == "markdown":
            return self._is_generated_markdown(content)
        elif agent.command_format.value == "toml":
            return self._is_generated_toml(content)
        return False

    def _is_generated_markdown(self, content: str) -> bool:
        """Check if markdown content was generated by this tool.

        Args:
            content: File content

        Returns:
            True if generated by this tool
        """
        # Check for YAML frontmatter with metadata
        if not content.startswith("---"):
            return False

        try:
            # Extract YAML frontmatter
            parts = content.split("---", 2)
            if len(parts) < 3:
                return False

            frontmatter = yaml.safe_load(parts[1])
            if not isinstance(frontmatter, dict):
                return False

            # Check for meta section with source_prompt or version
            meta = frontmatter.get("meta", {})
            return isinstance(meta, dict) and ("source_prompt" in meta or "version" in meta)
        except (yaml.YAMLError, AttributeError):
            return False

    def _is_generated_toml(self, content: str) -> bool:
        """Check if TOML content was generated by this tool.

        Args:
            content: File content

        Returns:
            True if generated by this tool
        """
        try:
            data = tomllib.loads(content)
            if not isinstance(data, dict):
                return False

            # Check for meta section with source_prompt or version
            meta = data.get("meta", {})
            return isinstance(meta, dict) and ("source_prompt" in meta or "version" in meta)
        except tomllib.TOMLDecodeError:
            return False

    def cleanup(
        self, agents: list[str] | None = None, include_backups: bool = True, dry_run: bool = False
    ) -> dict[str, Any]:
        """Clean up generated files.

        Args:
            agents: List of agent keys to clean. If None, cleans all agents.
            include_backups: If True, includes backup files in cleanup.
            dry_run: If True, don't delete files but report what would be deleted.

        Returns:
            Dict with keys: files_found, files_deleted, files
        """
        found_files = self.find_generated_files(agents=agents, include_backups=include_backups)

        deleted_files = []
        errors = []

        for file_info in found_files:
            file_path = Path(file_info["path"])
            if not dry_run:
                try:
                    file_path.unlink()
                    deleted_files.append(file_info)
                except OSError as e:
                    errors.append({"path": str(file_path), "error": str(e)})
            else:
                deleted_files.append(file_info)

        return {
            "files_found": len(found_files),
            "files_deleted": len(deleted_files),
            "files": deleted_files,
            "errors": errors,
        }
