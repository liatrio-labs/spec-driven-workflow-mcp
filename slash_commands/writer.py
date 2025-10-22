"""Writer for generating slash command files for multiple agents."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp_server.prompt_utils import MarkdownPrompt, load_markdown_prompt
from slash_commands.config import AgentConfig, get_agent_config
from slash_commands.generators import CommandGenerator


class SlashCommandWriter:
    """Orchestrates prompt loading and generation of command files for multiple agents."""

    def __init__(
        self,
        prompts_dir: Path,
        agents: list[str] | None = None,
        dry_run: bool = False,
        base_path: Path | None = None,
    ):
        """Initialize the writer.

        Args:
            prompts_dir: Directory containing prompt files
            agents: List of agent keys to generate commands for. If None, uses all supported agents.
            dry_run: If True, don't write files but report what would be written
            base_path: Base directory for output paths. If None, uses current directory.
        """
        self.prompts_dir = prompts_dir
        self.agents = agents or []
        self.dry_run = dry_run
        self.base_path = base_path or Path.cwd()

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
