"""Tests for prompt loading and registration."""

import anyio
import pytest

from mcp_server.prompt_utils import load_markdown_prompt, parse_frontmatter
from mcp_server.prompts_loader import register_prompts


class TestFrontmatterParsing:
    """Tests for YAML frontmatter parsing."""

    def test_parse_frontmatter_with_valid_yaml(self):
        """Test parsing valid YAML frontmatter."""
        content = """---
description: Test prompt
tags:
  - test
  - example
---

# Prompt Body

This is the body."""
        frontmatter, body = parse_frontmatter(content)

        assert frontmatter["description"] == "Test prompt"
        assert frontmatter["tags"] == ["test", "example"]
        assert body.startswith("# Prompt Body")

    def test_parse_frontmatter_without_frontmatter(self):
        """Test parsing content without frontmatter."""
        content = "# Just a heading\n\nSome content"
        frontmatter, body = parse_frontmatter(content)

        assert frontmatter == {}
        assert body == content

    def test_parse_frontmatter_with_invalid_yaml(self):
        """Test parsing invalid YAML frontmatter."""
        content = """---
invalid: yaml: content:
---

Body"""
        frontmatter, body = parse_frontmatter(content)

        assert frontmatter == {}
        assert "Body" in body


class TestPromptLoading:
    """Tests for loading prompts from directory."""

    def test_register_prompts(self, mcp_server, temp_prompts_dir):
        """Test loading prompts from a directory."""
        register_prompts(mcp_server, temp_prompts_dir)

        async def get_prompts():
            return await mcp_server.get_prompts()

        prompts = anyio.run(get_prompts)

        assert set(prompts) == {
            "generate-spec",
            "generate-task-list-from-spec",
            "manage-tasks",
        }

    def test_prompt_metadata_preserved(self, mcp_server, temp_prompts_dir):
        """Test that prompt metadata from frontmatter is preserved."""
        register_prompts(mcp_server, temp_prompts_dir)

        async def get_prompts():
            return await mcp_server.get_prompts()

        prompts = anyio.run(get_prompts)
        prompt = prompts["manage-tasks"]

        assert (
            prompt.description == "Guidelines for managing task lists and working on tasks/subtasks"
        )
        assert prompt.meta == {
            "category": "task-management",
            "allowed-tools": "Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch",
        }

    def test_register_prompts_from_nonexistent_directory(self, mcp_server, tmp_path):
        """Test loading prompts from a directory that doesn't exist."""
        nonexistent_dir = tmp_path / "nonexistent"

        with pytest.raises(ValueError, match="does not exist"):
            register_prompts(mcp_server, nonexistent_dir)

    def test_prompt_returns_string_body(self, mcp_server, temp_prompts_dir):
        """Test that prompts return the Markdown body as a string."""
        register_prompts(mcp_server, temp_prompts_dir)

        async def get_prompts():
            return await mcp_server.get_prompts()

        prompts = anyio.run(get_prompts)
        prompt = prompts["generate-spec"]

        body = prompt.fn()

        assert isinstance(body, str)
        assert "Generate Specification" in body

    def test_prompt_decorator_kwargs_use_serializable_tags(self, temp_prompts_dir):
        prompt = load_markdown_prompt(temp_prompts_dir / "manage-tasks.md")

        decorator_kwargs = prompt.decorator_kwargs()

        assert decorator_kwargs["tags"] == ["execution", "tasks"]
