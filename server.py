"""Spec-Driven Development MCP Server entrypoint.

This is the main entrypoint for running the FastMCP server.
The 'mcp' instance is automatically discovered by the FastMCP CLI.
"""

import argparse

from mcp_server import create_app

# Create the MCP server instance
# The CLI looks for 'mcp', 'server', or 'app' at module level
mcp = create_app()


def main() -> None:
    """Entry point for console script.

    This function is called when the package is installed and run via:
        uvx spec-driven-workflow

    It runs the MCP server using stdio transport by default, or http transport
    if --transport http is passed as an argument.
    """
    parser = argparse.ArgumentParser(description="Run the MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport type (default: stdio)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP server port (default: 8000)",
    )
    args = parser.parse_args()

    # Run the server with the specified transport
    if args.transport == "http":
        mcp.run(transport="http", port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
