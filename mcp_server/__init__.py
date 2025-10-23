"""Spec-Driven Development MCP Server.

A FastMCP-based server providing prompts, resources, and tools for
spec-driven development workflows.
"""

import tomllib
from pathlib import Path

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from .config import config
from .prompts_loader import register_prompts


def _get_version() -> str:
    """Get the version from pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


__version__ = _get_version()


def create_app() -> FastMCP:
    """Create and configure the FastMCP application.

    Returns:
        Configured FastMCP server instance
    """
    # Initialize FastMCP server
    mcp = FastMCP(name="spec-driven-development-mcp")

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> PlainTextResponse:
        return PlainTextResponse("OK")

    # Load prompts from the prompts directory and register them
    register_prompts(mcp, config.prompts_dir)

    @mcp.tool(name="basic-example", description="Return a static message for testing.")
    def basic_example_tool() -> str:
        """Basic example tool used to verify MCP tool registration."""

        return "Basic example tool invoked successfully."

    # TODO: Register resources (Task 2.1)
    # TODO: Register tools (Task 5.1)
    # TODO: Setup notifications (Task 5.2)
    # TODO: Setup sampling (Task 5.3)
    # TODO: Setup logging (Task 5.4)

    return mcp
