"""Runtime configuration for the SDD MCP server.

Provides testable defaults with environment variable overrides for:
- Workspace paths
- Transport options (STDIO/HTTP)
- Logging configuration
"""

import os
from pathlib import Path
from typing import Literal

TransportType = Literal["stdio", "http"]


class Config:
    """Runtime configuration with environment overrides."""

    def __init__(self) -> None:
        """Initialize configuration with defaults and environment overrides."""
        # Workspace paths
        self.workspace_root = Path(
            os.getenv("SDD_WORKSPACE_ROOT", "/workspace")
        ).resolve()
        self.prompts_dir = Path(
            os.getenv("SDD_PROMPTS_DIR", str(Path(__file__).parent.parent / "prompts"))
        ).resolve()

        # Transport configuration
        self.transport: TransportType = os.getenv("SDD_TRANSPORT", "stdio")  # type: ignore
        self.http_host = os.getenv("SDD_HTTP_HOST", "0.0.0.0")
        self.http_port = int(os.getenv("SDD_HTTP_PORT", "8000"))

        # Logging configuration
        self.log_level = os.getenv("SDD_LOG_LEVEL", "INFO")
        self.log_format = os.getenv("SDD_LOG_FORMAT", "json")  # json or text

        # CORS configuration for HTTP transport
        self.cors_enabled = os.getenv("SDD_CORS_ENABLED", "true").lower() == "true"
        self.cors_origins = os.getenv("SDD_CORS_ORIGINS", "*").split(",")

    def ensure_workspace_dirs(self) -> None:
        """Create workspace directories if they don't exist."""
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "specs").mkdir(exist_ok=True)
        (self.workspace_root / "tasks").mkdir(exist_ok=True)

    def __repr__(self) -> str:
        """Return string representation of configuration."""
        return (
            f"Config(workspace_root={self.workspace_root}, "
            f"prompts_dir={self.prompts_dir}, "
            f"transport={self.transport}, "
            f"http_host={self.http_host}, "
            f"http_port={self.http_port}, "
            f"log_level={self.log_level})"
        )


# Global configuration instance
config = Config()
