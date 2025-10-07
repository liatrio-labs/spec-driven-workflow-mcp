"""Spec-Driven Development MCP Server entrypoint.

This is the main entrypoint for running the FastMCP server.
The 'mcp' instance is automatically discovered by the FastMCP CLI.
"""

from mcp_server import create_app

# Create the MCP server instance
# The CLI looks for 'mcp', 'server', or 'app' at module level
mcp = create_app()
