"""Spec-Driven Development MCP Server entrypoint.

This is the main entrypoint for running the FastMCP server.
The 'mcp' instance is automatically discovered by the FastMCP CLI.
"""

from mcp_server import create_app

# Create the MCP server instance
# The CLI looks for 'mcp', 'server', or 'app' at module level
mcp = create_app()


def main() -> None:
    """Entry point for console script.

    This function is called when the package is installed and run via:
        uvx spec-driven-development-mcp

    It runs the MCP server using stdio transport.
    """
    mcp.run()
