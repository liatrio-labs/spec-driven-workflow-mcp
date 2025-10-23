# Operations Guide

This guide covers deployment, configuration, and operation of the Spec-Driven Development MCP server.

## Local Development

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

1. Clone the repository and navigate to the project directory
2. Install dependencies:

   ```bash
   uv sync
   ```

3. Run tests to verify setup:

   ```bash
   uv run pytest
   ```

### Running the Server

#### STDIO Transport (Default)

The STDIO transport is ideal for local development and integration with MCP clients like Claude Desktop:

```bash
uvx fastmcp run server.py
```

Or using the development server with the MCP Inspector:

```bash
uvx fastmcp dev server.py
```

This will start the server and open the MCP Inspector in your browser, allowing you to:

- Browse available prompts, resources, and tools
- Test prompt invocations
- View server logs and metrics

#### HTTP Transport

For remote access or integration with web-based clients:

```bash
uvx fastmcp run server.py --transport http --port 8000
```

The server will be available at `http://localhost:8000`.

## Configuration

The server can be configured via environment variables:

### Workspace Configuration

- `SDD_WORKSPACE_ROOT`: Root directory for generated specs and tasks (default: `/workspace`)
- `SDD_PROMPTS_DIR`: Directory containing prompt templates (default: `./prompts`)

### Transport Configuration

- `SDD_TRANSPORT`: Transport type - `stdio` or `http` (default: `stdio`)
- `SDD_HTTP_HOST`: HTTP server host (default: `0.0.0.0`)
- `SDD_HTTP_PORT`: HTTP server port (default: `8000`)

### Logging Configuration

- `SDD_LOG_LEVEL`: Logging level - `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `INFO`)
- `SDD_LOG_FORMAT`: Log format - `json` or `text` (default: `json`)

### CORS Configuration (HTTP only)

- `SDD_CORS_ENABLED`: Enable CORS (default: `true`)
- `SDD_CORS_ORIGINS`: Comma-separated list of allowed origins (default: `*`)

### Example

```bash
export SDD_WORKSPACE_ROOT=/home/user/workspace
export SDD_LOG_LEVEL=DEBUG
uvx fastmcp run server.py
```

## MCP Client Integration

### Claude Desktop

Add the following to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "spec-driven-development": {
      "command": "uvx",
      "args": ["fastmcp", "run", "/path/to/spec-driven-development-mcp/server.py"]
    }
  }
}
```

### VS Code MCP Plugin

1. Install the MCP plugin for VS Code
2. Add the server configuration to your workspace settings:

   ```json
   {
     "mcp.servers": {
       "spec-driven-development": {
         "command": "uvx",
         "args": ["fastmcp", "run", "/path/to/spec-driven-development-mcp/server.py"]
       }
     }
   }
   ```

### FastMCP Inspector

The FastMCP Inspector provides a web-based interface for testing and debugging:

```bash
uvx fastmcp dev server.py
```

This will:

1. Start the MCP server
2. Start the Inspector proxy
3. Open the Inspector UI in your browser

## Testing

### Run All Tests

```bash
uv run pytest
```

### Run with Coverage

```bash
uv run pytest --cov=mcp_server --cov=slash_commands --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the detailed coverage report.

```bash
uv run pytest tests/test_prompts.py -v
```

## Troubleshooting

### Server Won't Start

1. Verify Python version: `python --version` (should be 3.12+)
2. Reinstall dependencies: `uv sync`
3. Check for port conflicts (if using HTTP transport)

### Prompts Not Loading

1. Verify prompts directory exists and contains `.md` files
2. Check that prompt files have valid YAML frontmatter
3. Review server logs for parsing errors

### Tests Failing

1. Ensure all dependencies are installed: `uv sync`
2. Run tests with verbose output: `uv run pytest -v`
3. Check for environment variable conflicts
