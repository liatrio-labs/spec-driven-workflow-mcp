"""Dynamic loader for Markdown prompts with _meta tagging.

Loads prompts from the prompts/ directory and registers them with FastMCP,
preserving YAML frontmatter as _meta tags for discovery and organization.
"""

from pathlib import Path
from typing import Any

import yaml
from fastmcp import FastMCP
from mcp.types import PromptMessage


def load_prompts_from_directory(mcp: FastMCP, prompts_dir: Path) -> None:
    """Load all Markdown prompts from a directory and register them with FastMCP.

    Args:
        mcp: FastMCP server instance to register prompts with
        prompts_dir: Directory containing .md prompt files

    Each prompt file should have YAML frontmatter with at least a 'description' field.
    The filename (without extension) becomes the prompt name.
    """
    if not prompts_dir.exists():
        raise ValueError(f"Prompts directory does not exist: {prompts_dir}")

    for prompt_file in prompts_dir.glob("*.md"):
        _load_prompt_file(mcp, prompt_file)


def _load_prompt_file(mcp: FastMCP, prompt_file: Path) -> None:
    """Load a single prompt file and register it with FastMCP.

    Args:
        mcp: FastMCP server instance
        prompt_file: Path to the .md prompt file
    """
    content = prompt_file.read_text()

    # Parse YAML frontmatter
    frontmatter, body = _parse_frontmatter(content)

    # Extract metadata
    prompt_name = prompt_file.stem  # filename without extension
    description = frontmatter.get("description", "")

    # Create a prompt function that returns the prompt body
    def create_prompt_fn(prompt_body: str) -> Any:
        """Factory to create a prompt function with the correct body."""

        def prompt_fn() -> list[PromptMessage]:
            """Return the prompt as a user message."""
            return [
                PromptMessage(
                    role="user",
                    content={
                        "type": "text",
                        "text": prompt_body,
                    },
                )
            ]

        return prompt_fn

    # Create and register the prompt
    prompt_fn = create_prompt_fn(body)
    prompt_fn.__name__ = prompt_name
    prompt_fn.__doc__ = description

    # Register with FastMCP using the decorator pattern
    mcp.prompt(name=prompt_name)(prompt_fn)


def _parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from Markdown content.

    Args:
        content: Markdown content with optional YAML frontmatter

    Returns:
        Tuple of (frontmatter_dict, body_content)
    """
    if not content.startswith("---"):
        return {}, content

    # Find the closing ---
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        frontmatter = {}

    # Return frontmatter and body
    body = parts[2].strip()
    return frontmatter, body
