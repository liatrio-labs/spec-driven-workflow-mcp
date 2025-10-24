"""Agent auto-detection utilities."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path

from .config import SUPPORTED_AGENTS, AgentConfig


def detect_agents(target_dir: Path | str) -> list[AgentConfig]:
    """Return agents whose detection directories exist under ``target_dir``.

    The result preserves the ordering defined in :data:`SUPPORTED_AGENTS` to
    ensure deterministic CLI output regardless of filesystem discovery order.
    """

    base_path = Path(target_dir)
    detected: list[AgentConfig] = []

    for agent in SUPPORTED_AGENTS:
        if _agent_configured(agent, base_path):
            detected.append(agent)

    return detected


def _agent_configured(agent: AgentConfig, base_path: Path) -> bool:
    """Return ``True`` if any of the agent's detection directories exist."""

    return any((base_path / Path(directory)).exists() for directory in agent.iter_detection_dirs())


def iter_detection_directories(agent: AgentConfig, base_path: Path | str) -> Iterable[Path]:
    """Yield absolute paths for the agent's detection directories."""

    base = Path(base_path)
    for directory in agent.iter_detection_dirs():
        yield base / Path(directory)


def supported_agents() -> Sequence[AgentConfig]:
    """Expose supported agents for callers that only import detection module."""

    return SUPPORTED_AGENTS


__all__ = ["detect_agents", "iter_detection_directories", "supported_agents"]
