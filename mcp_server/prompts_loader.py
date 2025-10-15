from __future__ import annotations

from pathlib import Path

from fastmcp import FastMCP

from .prompt_utils import MarkdownPrompt, load_markdown_prompt


def _load_prompt(prompts_dir: Path, filename: str) -> MarkdownPrompt:
    return load_markdown_prompt(prompts_dir / filename)


def _register_prompt(mcp: FastMCP, prompt: MarkdownPrompt) -> None:
    # See https://gofastmcp.com/servers/prompts#the-%40prompt-decorator
    @mcp.prompt(**prompt.decorator_kwargs())
    def prompt_handler() -> str:
        return prompt.body

    prompt_handler.__name__ = f"{prompt.name}_prompt"


def register_prompts(mcp: FastMCP, prompts_dir: Path) -> None:
    if not prompts_dir.exists():
        raise ValueError(f"Prompts directory does not exist: {prompts_dir}")

    # Get all of the prompt files
    prompt_files = sorted(
        (f for f in prompts_dir.iterdir() if f.is_file() and f.suffix == ".md"),
        key=lambda file_path: file_path.name,
    )

    # Load and register each prompt
    for prompt_file in prompt_files:
        prompt_info = _load_prompt(prompts_dir, prompt_file.name)
        _register_prompt(mcp, prompt_info)
