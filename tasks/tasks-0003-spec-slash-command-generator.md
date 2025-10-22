## Relevant Files

- `slash_commands/__init__.py` - Exposes slash command generator package for imports and CLI wiring.
- `slash_commands/config.py` - Defines `AgentConfig`, supported agent registry, and related enums.
- `slash_commands/detection.py` - Implements auto-detection logic for configured agent directories.
- `slash_commands/generators.py` - Houses `CommandGenerator` base class plus Markdown/TOML subclasses.
- `slash_commands/writer.py` - Coordinates prompt loading and file generation for selected agents.
- `slash_commands/cli.py` - Typer CLI entry point handling argument parsing and interactive flows.
- `tests/test_config.py` - Unit tests validating agent configuration data models.
- `tests/test_detection.py` - Unit tests covering auto-detection behaviour.
- `tests/conftest.py` - Shared pytest fixtures for prompt samples and overrides.
- `tests/test_generators.py` - Unit tests for Markdown and TOML command generators.
- `tests/test_writer.py` - Unit tests ensuring writer orchestrates generation and dry-runs correctly.
- `tests/test_cli.py` - Unit tests covering CLI option parsing and exit codes.
- `docs/slash-command-generator.md` - Detailed usage documentation for the new feature.
- `README.md` - Surface-level overview linking to detailed documentation.
- `pyproject.toml` - Adds Typer dependency and CLI script entry point.

### Notes

- Unit tests should live alongside other `tests/` modules and leverage shared fixtures in `tests/conftest.py`.
- Use `pytest tests/<module>::<testcase>` for focused test runs during TDD cycles.
- Prefer `pathlib.Path` APIs for filesystem interactions to maintain cross-platform compatibility.

## Tasks

- [x] 1.0 Establish slash command configuration and agent detection foundations
  - Demo Criteria: "Config data models enumerate all 14 agents with accurate directories/formats and detection flags configured tools under pytest validation."
  - Proof Artifact(s): "CLI: `pytest tests/test_config.py tests/test_detection.py -v`; Log: detection fixture output listing detected agents."
  - [x] 1.1 Author failing tests in `tests/test_config.py` that assert required fields and format values for every agent entry.
  - [x] 1.2 Implement `CommandFormat` enum, `AgentConfig` dataclass, and helper accessors in `slash_commands/config.py` to satisfy the tests.
  - [x] 1.3 Populate `SUPPORTED_AGENTS` with all 14 tools, including directory paths, file extensions, and format metadata.
  - [x] 1.4 Draft failing detection tests in `tests/test_detection.py` covering positive, negative, and mixed directory scenarios using `tmp_path` fixtures.
  - [x] 1.5 Implement `detect_agents` (and supporting utilities) in `slash_commands/detection.py` so detection tests pass with deterministic ordering.

- [x] 2.0 Implement Markdown and TOML command generators with override support
  - Demo Criteria: "Generators transform `MarkdownPrompt` objects into .md/.toml command files that honor placeholders and agent-specific metadata overrides."
  - Proof Artifact(s): "CLI: `pytest tests/test_generators.py -v`; Snapshot diff: expected vs actual generated command files."
  - [x] 2.1 Add fixtures in `tests/conftest.py` for sample prompts, including agent override metadata and argument definitions.
  - [x] 2.2 Write failing tests in `tests/test_generators.py` that assert Markdown output includes frontmatter, body, and `$ARGUMENTS` placeholder handling.
  - [x] 2.3 Extend generator tests to cover TOML formatting, `{{args}}` substitution, and override application across multiple agents.
  - [x] 2.4 Implement `CommandGenerator` base class plus Markdown and TOML subclasses in `slash_commands/generators.py`, including helper factory selection logic.
  - [x] 2.5 Refine generators to normalize whitespace and encoding, updating tests to use snapshot-style comparisons for regression safety.

- [ ] 3.0 Build slash command writer orchestrating multi-agent generation and dry runs
  - Demo Criteria: "Writer loads prompts, generates commands for single and multi-agent selections, ensures directories exist, and reports dry-run results without writes."
  - Proof Artifact(s): "CLI: `pytest tests/test_writer.py -v`; Log: dry-run test output showing file paths and counts."
  - [ ] 3.1 Introduce failing writer tests that mock prompt loading and assert correct call sequences for single and multi-agent runs.
  - [ ] 3.2 Add dry-run focused tests ensuring no files are created while summaries report planned outputs.
  - [ ] 3.3 Implement `SlashCommandWriter` in `slash_commands/writer.py`, wiring config, generators, and prompt utilities with dependency injection-friendly design.
  - [ ] 3.4 Ensure writer creates parent directories, respects dry-run flag, and returns structured results; update tests to validate filesystem effects with `tmp_path`.
  - [ ] 3.5 Export writer interfaces from `slash_commands/__init__.py` for reuse by CLI and future modules.

- [ ] 4.0 Deliver Typer CLI with auto-detection and selection flows
  - Demo Criteria: "Running `sdd-generate-commands` auto-detects configured agents, supports interactive confirmation and `--agents`, `--list-agents`, `--dry-run`, `--yes` flags, and exits with correct status codes."
  - Proof Artifact(s): "CLI: `pytest tests/test_cli.py -v`; CLI: `sdd-generate-commands --list-agents`; Recording: interactive agent selection session."
  - [ ] 4.1 Define CLI tests using Typer's `CliRunner` to cover happy paths, invalid agent input, and exit codes.
  - [ ] 4.2 Implement Typer app in `slash_commands/cli.py`, wiring options via `Annotated` syntax and delegating to writer/detection modules.
  - [ ] 4.3 Add interactive selection logic leveraging detection results, opt-out confirmations, and `--yes` short-circuit coverage.
  - [ ] 4.4 Support `--agents`, `--list-agents`, `--dry-run`, and `--prompts-dir` options with clear messaging; extend tests accordingly.
  - [ ] 4.5 Register entry point in `pyproject.toml` and expose CLI in `slash_commands/__init__.py`; update CLI tests to assert console summary formatting.

- [ ] 5.0 Implement safe overwrite handling and finalize packaging & docs
  - Demo Criteria: "CLI prompts on existing files with cancel/overwrite/backup choices, creates timestamped `.bak` copies when selected, and project docs/scripts describe the workflow."
  - Proof Artifact(s): "CLI: fixture run showing overwrite prompt and `.bak` files; CLI: `ls -la .claude/commands/*.bak`; Diff: updates to `README.md` and `docs/slash-command-generator.md`."
  - [ ] 5.1 Craft failing writer/CLI tests that simulate existing command files and assert prompt branches for cancel, overwrite, and backup choices.
  - [ ] 5.2 Implement overwrite handling utilities that create timestamped backups via `shutil.copy2`, configurable for per-file vs global decisions.
  - [ ] 5.3 Extend CLI to surface overwrite prompts, honor `--yes`, and emit summary of backups created.
  - [ ] 5.4 Document new workflow in `docs/slash-command-generator.md` and add concise overview/link in `README.md`.
  - [ ] 5.5 Update `pyproject.toml` dependencies (Typer, Questionary if used) and regenerate `uv.lock`; note release considerations in `CHANGELOG.md` if required.
