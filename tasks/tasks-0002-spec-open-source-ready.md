## Relevant Files

- `LICENSE` - Apache 2.0 license text at repo root.
- `README.md` - Project overview, quick start, links, and license badge/section.
- `CONTRIBUTING.md` - Contribution workflow, setup, style, testing, PR guidance.
- `.github/ISSUE_TEMPLATE/bug_report.yml` - Structured bug report issue form.
- `.github/ISSUE_TEMPLATE/feature_request.yml` - Structured feature request form.
- `.github/ISSUE_TEMPLATE/question.yml` - Support/question form.
- `.github/ISSUE_TEMPLATE/config.yml` - Enforce templates and defaults.

### Notes

- Respect existing tooling: `uv`, `pytest`, `pre-commit`, `ruff`, markdownlint (see `.pre-commit-config.yaml`).
- Keep docs consistent with `docs/operations.md` and `pyproject.toml`.
- SemVer is automated via CI/CD (e.g., `python-semantic-release`); contributors just follow conventional commits.

## Tasks

- [x] 1.0 Add Apache 2.0 licensing artifacts
  - Demo Criteria: `LICENSE` present at repo root and referenced in README.
  - Proof Artifact(s): Files `LICENSE` and (optional) `NOTICE`; `git diff`.
  - [x] 1.1 Add official Apache 2.0 text to `LICENSE` at repo root
  - [x] 1.2 Add a license badge and License section reference in `README.md`
  - [x] 1.3 Cross-check `pyproject.toml` and `README.md` for correct license naming
  - [x] 1.4 Run linters: `pre-commit run --all-files` (markdownlint/ruff fixups)
  - [x] 1.5 Verify links render on GitHub (badge and License section)

- [x] 2.0 Refresh README with visual asset and links
  - Demo Criteria: `README.md` includes an image (diagram/screenshot/banner), Apache 2.0 license mention, and links to `docs/operations.md` and `CONTRIBUTING.md`.
  - Proof Artifact(s): Updated `README.md`; image asset committed; `git diff`.
  - [x] 2.1 Create a mermaid diagram of the spec-driven development workflow and embed it near the top of `README.md` (will convert to svg later)
  - [x] 2.2 Add links to `docs/operations.md` and `CONTRIBUTING.md`
  - [x] 2.3 Ensure Quick Start matches `docs/operations.md` commands (`uv sync`, `uv run pytest`, `uvx fastmcp ...`)
  - [x] 2.4 Add a brief License section pointing to `LICENSE`
  - [x] 2.5 Run `pre-commit run --all-files` to satisfy markdownlint

- [ ] 3.0 Add CONTRIBUTING.md
  - Demo Criteria: Contribution workflow documented (setup via `uv sync`, tests via `uv run pytest`, `pre-commit run`, branch/commit conventions, PR review process; Code of Conduct link/placeholder).
  - Proof Artifact(s): `CONTRIBUTING.md`; `git diff`.
  - [ ] 3.1 Draft structure: Overview, Getting Started, Dev Setup, Style, Testing, Commits, PRs, Code of Conduct
  - [ ] 3.2 Document environment setup: `uv sync`, `pre-commit install`, running hooks, `uv run pytest`
  - [ ] 3.3 Define branch naming and Conventional Commits format with examples
  - [ ] 3.4 Reference issue templates and `docs/operations.md`
  - [ ] 3.5 Run `pre-commit run --all-files`

- [ ] 4.0 Add GitHub Issue Templates
  - Demo Criteria: Issue forms for bug, feature, and question collect summary, repro/context, environment (Python, OS), logs/output, and related prompt/task IDs; `config.yml` enforces usage and default labels.
  - Proof Artifact(s): `.github/ISSUE_TEMPLATE/{bug_report.yml,feature_request.yml,question.yml,config.yml}`; `git diff`.
  - [ ] 4.1 Create `.github/ISSUE_TEMPLATE/bug_report.yml` with fields: Summary, Repro Steps, Expected, Actual, Logs/Output, Environment (OS, Python), Related Prompt/Task IDs
  - [ ] 4.2 Create `.github/ISSUE_TEMPLATE/feature_request.yml` with fields: Problem, Desired Outcome, Acceptance Criteria, Affected Prompts/Workflows, Additional Context
  - [ ] 4.3 Create `.github/ISSUE_TEMPLATE/question.yml` with fields: Context, Commands Run, Referenced Spec/Task IDs, What’s been tried
  - [ ] 4.4 Add `.github/ISSUE_TEMPLATE/config.yml` with `blank_issues_disabled: true`, default labels, and optional contact links
  - [ ] 4.5 Validate YAML (passes `check-yaml`), then run `pre-commit run --all-files`

- [ ] 5.0 Document SemVer expectations
  - Demo Criteria: README/CONTRIBUTING note clarifies semver is CI/CD-managed (no manual tagging), with conventional commits required.
  - Proof Artifact(s): Updated section in `README.md` or `CONTRIBUTING.md`; `git diff`.
  - [ ] 5.1 Add a section documenting CI-managed releases (semantic-release) and tag policy
  - [ ] 5.2 Link to `python-semantic-release` and note CHANGELOG generation
  - [ ] 5.3 Emphasize Conventional Commits as the contributor requirement
  - [ ] 5.4 Run `pre-commit run --all-files`
