"""Spec-Driven Development MCP Server.

A FastMCP-based server providing prompts, resources, and tools for
spec-driven development workflows.
"""

from fastmcp import FastMCP

from .config import config
from .prompts_loader import load_prompts_from_directory

__version__ = "0.1.0"


def create_app() -> FastMCP:
    """Create and configure the FastMCP application.

    Returns:
        Configured FastMCP server instance
    """
    # Initialize FastMCP server
    mcp = FastMCP(name="spec-driven-development-mcp")

    # Load prompts from the prompts directory
    load_prompts_from_directory(mcp, config.prompts_dir)

    # TODO: Register resources (Task 2.1)
    # TODO: Register tools (Task 5.1)
    # TODO: Setup notifications (Task 5.2)
    # TODO: Setup sampling (Task 5.3)
    # TODO: Setup logging (Task 5.4)

    return mcp


# Create the global app instance
app = create_app()
