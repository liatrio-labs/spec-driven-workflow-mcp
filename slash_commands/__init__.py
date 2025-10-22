"""Slash command generator package."""

from .config import SUPPORTED_AGENTS, AgentConfig, CommandFormat, get_agent_config, list_agent_keys
from .writer import SlashCommandWriter

__all__ = [
    "SUPPORTED_AGENTS",
    "AgentConfig",
    "CommandFormat",
    "SlashCommandWriter",
    "get_agent_config",
    "list_agent_keys",
]
