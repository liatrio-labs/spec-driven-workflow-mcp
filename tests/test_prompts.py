"""Tests for prompt loading and registration."""

import anyio
import pytest

from mcp_server.prompts_loader import _parse_frontmatter, load_prompts_from_directory


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
        frontmatter, body = _parse_frontmatter(content)

        assert frontmatter["description"] == "Test prompt"
        assert frontmatter["tags"] == ["test", "example"]
        assert body.startswith("# Prompt Body")

    def test_parse_frontmatter_without_frontmatter(self):
        """Test parsing content without frontmatter."""
        content = "# Just a heading\n\nSome content"
        frontmatter, body = _parse_frontmatter(content)

        assert frontmatter == {}
        assert body == content

    def test_parse_frontmatter_with_invalid_yaml(self):
        """Test parsing invalid YAML frontmatter."""
        content = """---
invalid: yaml: content:
---

Body"""
        frontmatter, body = _parse_frontmatter(content)

        assert frontmatter == {}
        assert "Body" in body


class TestPromptLoading:
    """Tests for loading prompts from directory."""

    def test_load_prompts_from_directory(self, mcp_server, temp_prompts_dir):
        """Test loading prompts from a directory."""
        load_prompts_from_directory(mcp_server, temp_prompts_dir)

        # Get the loaded prompts
        async def get_prompts():
            return await mcp_server.get_prompts()

        prompts = anyio.run(get_prompts)

        # Verify prompts were loaded
        assert len(prompts) == 2
        assert "test-prompt" in prompts
        assert "another-prompt" in prompts

    def test_loaded_prompt_has_description(self, mcp_server, temp_prompts_dir):
        """Test that loaded prompts have descriptions from frontmatter."""
        load_prompts_from_directory(mcp_server, temp_prompts_dir)

        async def get_prompts():
            return await mcp_server.get_prompts()

        prompts = anyio.run(get_prompts)
        test_prompt = prompts["test-prompt"]

        # Check that the prompt has the description
        assert test_prompt.fn.__doc__ == "A test prompt"

    def test_load_prompts_from_nonexistent_directory(self, mcp_server, tmp_path):
        """Test loading prompts from a directory that doesn't exist."""
        nonexistent_dir = tmp_path / "nonexistent"

        with pytest.raises(ValueError, match="does not exist"):
            load_prompts_from_directory(mcp_server, nonexistent_dir)

    def test_prompt_returns_message_list(self, mcp_server, temp_prompts_dir):
        """Test that prompts return a list of messages."""
        load_prompts_from_directory(mcp_server, temp_prompts_dir)

        async def get_prompts():
            return await mcp_server.get_prompts()

        prompts = anyio.run(get_prompts)
        test_prompt = prompts["test-prompt"]

        # Call the prompt function
        messages = test_prompt.fn()

        # Verify it returns a list of messages
        assert isinstance(messages, list)
        assert len(messages) == 1
        assert messages[0].role == "user"
        assert "Test Prompt" in messages[0].content.text
