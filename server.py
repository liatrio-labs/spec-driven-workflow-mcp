"""Spec-Driven Development MCP Server entrypoint.

This is the main entrypoint for running the FastMCP server.
The 'mcp' instance is automatically discovered by the FastMCP CLI.
"""

import sys

from mcp_server import create_app

# Create the MCP server instance
# The CLI looks for 'mcp', 'server', or 'app' at module level
mcp = create_app()


def main() -> None:
    """Entry point for console script.

    This function is called when the package is installed and run via:
        uvx spec-driven-development-mcp

    It runs the MCP server using stdio transport by default, or http transport
    if --transport http is passed as an argument.
    """
    # Parse command line arguments
    transport = "stdio"
    port = 8000
    args = sys.argv[1:]

    # Simple argument parsing for transport and port
    if "--transport" in args:
        idx = args.index("--transport")
        if idx + 1 < len(args):
            transport = args[idx + 1]

    if "--port" in args:
        idx = args.index("--port")
        if idx + 1 < len(args):
            port = int(args[idx + 1])

    # Run the server with the specified transport
    if transport == "http":
        mcp.run(transport="http", port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
