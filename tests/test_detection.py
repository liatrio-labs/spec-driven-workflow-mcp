"""Tests for agent auto-detection helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from slash_commands.config import SUPPORTED_AGENTS, AgentConfig
from slash_commands.detection import detect_agents


@pytest.fixture(scope="module")
def supported_agents_by_key() -> dict[str, AgentConfig]:
    return {agent.key: agent for agent in SUPPORTED_AGENTS}


def test_detect_agents_returns_empty_when_no_matching_directories(tmp_path: Path):
    (tmp_path / "unrelated").mkdir()
    detected = detect_agents(tmp_path)
    assert detected == []


def test_detect_agents_identifies_configured_directories(
    tmp_path: Path, supported_agents_by_key: dict[str, AgentConfig]
):
    agent_keys = {"claude-code", "gemini-cli", "cursor"}
    for key in agent_keys:
        agent = supported_agents_by_key[key]
        for directory in agent.detection_dirs:
            full_dir = tmp_path / directory
            full_dir.mkdir(parents=True, exist_ok=True)

    detected = detect_agents(tmp_path)
    detected_keys = [agent.key for agent in detected]

    expected_order = [a.key for a in SUPPORTED_AGENTS if a.key in agent_keys]
    assert detected_keys == expected_order
    for key in detected_keys:
        directories = {tmp_path / path for path in supported_agents_by_key[key].detection_dirs}
        assert all(directory.exists() for directory in directories)


def test_detect_agents_deduplicates_and_orders_results(tmp_path: Path):
    claude_agent = next(agent for agent in SUPPORTED_AGENTS if agent.key == "claude-code")
    cursor_agent = next(agent for agent in SUPPORTED_AGENTS if agent.key == "cursor")

    for directory in claude_agent.detection_dirs + cursor_agent.detection_dirs:
        (tmp_path / directory).mkdir(parents=True, exist_ok=True)

    # create unrelated directories that should be ignored
    (tmp_path / ".unknown").mkdir()
    (tmp_path / "not-a-config").mkdir()

    detected = detect_agents(tmp_path)
    detected_keys = [agent.key for agent in detected]

    assert detected_keys == ["claude-code", "cursor"]
    assert all(detected_keys.count(key) == 1 for key in detected_keys)
