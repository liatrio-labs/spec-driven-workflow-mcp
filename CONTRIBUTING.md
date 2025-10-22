# Contributing to Spec Driven Development (SDD) MCP

Thanks for your interest in contributing! This guide explains how to set up your environment, follow our style and commit conventions, run tests and linters, and submit pull requests.

## Overview

This repository provides an MCP server and prompts that enable a spec‑driven development workflow. Contributions generally fall into one of these areas:

- Documentation and examples
- Prompt and workflow improvements
- Server code, tests, and tooling

Please open an issue first for significant changes to discuss the approach.

## Getting Started

1. Fork and clone the repository.
2. Ensure you have Python 3.12+ and [`uv`](https://docs.astral.sh/uv/) installed.
3. Set up the development environment:

```bash
uv sync
pre-commit install
```

## Development Setup

- Use `uv` for all Python dependency and execution tasks.
- Install pre-commit hooks once with `pre-commit install`.
- Keep changes small and focused; prefer incremental PRs.

### Common Commands

```bash
# Run tests with coverage
uv run pytest

# Run full pre-commit checks across the repo
uv run pre-commit run --all-files

# Run the server (STDIO)
uvx fastmcp run server.py

# Run the server (HTTP)
uvx fastmcp run server.py --transport http --port 8000
```

See `docs/operations.md` for more details on transports and configuration.

## Style and Quality

- Python style and formatting are enforced via `ruff`. The pre-commit hooks will run `ruff check` and `ruff format`.
- Markdown is linted using markdownlint (via pre-commit). Keep lines reasonably short and headings well structured.
- Keep documentation consistent with `docs/operations.md` and `README.md`.

## Testing

- Tests use `pytest` with coverage reporting via `pytest-cov`.
- Before submitting a PR, run:

```bash
# Run tests with coverage report
uv run pytest

# View HTML coverage report (opens in default browser)
uv run python -m webbrowser htmlcov/index.html
```

The test suite generates both terminal and HTML coverage reports showing which code paths are tested.

## Branching and Commit Conventions

### Branch Naming

Use short, descriptive branch names with a category prefix:

- `feat/<short-topic>`
- `fix/<short-topic>`
- `docs/<short-topic>`
- `chore/<short-topic>`
- `refactor/<short-topic>`

Examples:

- `feat/issue-templates`
- `docs/contributing-guide`

### Conventional Commits

We follow the Conventional Commits specification. Examples:

- `feat: add helper tool to list artifacts`
- `fix: handle missing prompt metadata in loader`
- `docs: clarify HTTP transport usage`
- `chore: bump dependencies and run pre-commit`

If a change is breaking, include `!` (e.g., `feat!: drop Python 3.10 support`).

Semantic versioning and releases are automated in CI (e.g., `python-semantic-release`). Contributors only need to follow Conventional Commits; no manual tagging is required.

## Pull Requests

- Keep PRs focused and well scoped.
- **PR titles must follow Conventional Commits format** (e.g., `feat: add new feature`). This is enforced by an automated check.
- PR description template:

```markdown
## Why?

## What Changed?

## Additional Notes
```

- Ensure all checks pass (tests and pre-commit) before requesting review.
- Reference related issues and task IDs where applicable.

### PR Title Format

PR titles are validated automatically and must follow this format:

```
<type>(<optional scope>): <description>
```

**Valid types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Examples:**
- `feat(auth): add login button to navigation`
- `fix: resolve race condition in async handler`
- `docs: update installation instructions`
- `chore: bump dependencies and run pre-commit`

The description should:
- Start with a lowercase letter
- Be concise and descriptive
- Use imperative mood (e.g., "add" not "added" or "adds")

**Breaking changes:** Add `!` after the type (e.g., `feat!: drop Python 3.10 support`)

If the automated check fails, update your PR title and it will re-run automatically.

## Issue Templates

Use the GitHub issue templates under `.github/ISSUE_TEMPLATE/` for bug reports, feature requests, and questions. These templates prompt for summary, context/repro, environment (Python/OS), and related prompt/task IDs.

## Code of Conduct (Placeholder)

We strive to maintain a welcoming and respectful community. A formal Code of Conduct will be added or linked here in a future update. In the meantime, please be considerate and professional in all interactions.

If you have any concerns, please open an issue or contact the maintainers.

## References

- `docs/operations.md` — operations, transports, and configuration
- `README.md` — overview and quick start
- `.pre-commit-config.yaml` — linting and formatting hooks
- `.github/ISSUE_TEMPLATE/` — issue forms
