"""Spec-Driven Development MCP Server.

A FastMCP-based server providing prompts, resources, and tools for
spec-driven development workflows.
"""

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

try:
    from __version__ import __version__
except ImportError:
    # Fallback for when installed as a package
    from importlib.metadata import version

    __version__ = version("spec-driven-workflow")

from .config import config
from .prompts_loader import register_prompts


def create_app() -> FastMCP:
    """Create and configure the FastMCP application.

    Returns:
        Configured FastMCP server instance
    """
    # Initialize FastMCP server
    mcp = FastMCP(name="spec-driven-workflow-mcp")

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
