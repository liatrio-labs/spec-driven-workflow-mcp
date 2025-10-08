# Open-Source Readiness (Apache 2.0)

## Introduction/Overview

Open-source the `spec-driven-development-mcp` repository under the Apache 2.0 License. Deliver a public-ready experience with licensing, documentation, contribution guidelines, and issue templates that make it easy for new collaborators to adopt, use, and extend the MCP server.

## Goals

- Publish the project under Apache 2.0 with all required notices.
- Present an engaging `README.md` featuring a visual asset and newcomer-friendly overview.
- Document contribution and issue-reporting processes tailored to this codebase.
- Provide ready-to-use GitHub issue templates aligned with MCP workflow needs.
- Confirm semantic versioning strategy is documented for CI/CD managed releases.

## User Stories

- As a **potential adopter**, I want to understand the project’s purpose, licensing, and quick-start steps from the README so I can evaluate use.
- As a **first-time contributor**, I want clear contribution and issue guidelines so I can confidently propose changes or report bugs.
- As a **maintainer**, I want consistent issue reports and contributions so triage and reviews stay efficient.

## Demoable Units of Work

- **1. LICENSE + Notice**
  Demo Criteria: Repository root includes `LICENSE` and (if needed) `NOTICE` files with Apache 2.0 text referenced by `pyproject.toml` and README.
  Proof Artifact(s): `LICENSE`, optional `NOTICE`, `git diff`.
- **2. README Refresh**
  Demo Criteria: `README.md` showcases a new visual asset, highlights Apache 2.0 licensing, and links to contributions/docs.
  Proof Artifact(s): Screenshot/image asset, `README.md`, `git diff`.
- **3. Contribution Guide**
  Demo Criteria: `CONTRIBUTING.md` introduces workflows, coding standards, test commands, and PR expectations referencing existing tooling (`uv`, `pre-commit`, conventional commits).
  Proof Artifact(s): `CONTRIBUTING.md`, `git diff`.
- **4. Issue Templates & Policies**
  Demo Criteria: `.github/ISSUE_TEMPLATE/` includes bug, feature, and question forms; repository metadata enforces template usage with helpful default labels.
  Proof Artifact(s): YAML form files, `config.yml`, `git diff`.
- **5. Release & Maintenance Notes**
  Demo Criteria: Documented semver expectations in `README.md` or `CONTRIBUTING.md`, noting automation via CI/CD.
  Proof Artifact(s): Updated doc section, CI reference, `git diff`.

## Functional Requirements

1. The repository MUST include an Apache 2.0 `LICENSE` file and add a `NOTICE` file if required by dependencies or branding.
2. `README.md` MUST:
   - Emphasize Apache 2.0 licensing.
   - Include a new visual asset (diagram, screenshot, or banner).
   - Highlight installation, usage, and support resources.
3. A `CONTRIBUTING.md` MUST explain contribution workflow, development environment setup (`uv sync`, `uv run pytest`, `pre-commit run`), branch/commit conventions, and review process.
4. Contribution guidelines MUST include a “Code of Conduct” placeholder or link (create if absent).
5. `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml`, and `question.yml` MUST gather: summary, reproduction/context, environment details (Python version, OS), associated prompt/task IDs, and expected outcomes.
6. `.github/ISSUE_TEMPLATE/config.yml` MUST require template usage and apply sensible default labels.
7. Documentation MUST mention that semantic versioning is enforced via CI/CD (e.g., `python-semantic-release`), with contributor expectations limited to following commit conventions.
8. README MUST link to docs like `docs/operations.md`, `CONTRIBUTING.md`, and issue templates.
9. All markdown updates MUST pass existing markdownlint/pre-commit checks.

## Non-Goals (Out of Scope)

- Changes to MCP prompt logic or server behavior beyond documentation metadata.
- Introducing new automation pipelines beyond documenting existing CI/CD semver tooling.
- Creating full brand identity assets beyond the single README visual.

## Design Considerations

- README image should align with current project aesthetic: lightweight diagram or banner illustrating spec-driven workflow.
- Use consistent typography and color palette; prefer vector or high-resolution PNG.

## Technical Considerations

- Ensure new files respect repository structure (`.github/ISSUE_TEMPLATE/` directory).
- Reference existing tooling (`uv`, `pre-commit`, `python-semantic-release`) to keep instructions accurate.
- Confirm Apache 2.0 notice propagation if bundled binaries are ever distributed.

## Success Metrics

- README image renders correctly on GitHub and passes markdown linting.
- Contribution and issue docs reduce initial triage time (trackable qualitatively via future feedback).
- License compliance verified by maintainer review.

## Open Questions

- Should we add a Code of Conduct (e.g., Contributor Covenant) or link to Liatrio’s existing policy?
  - no, don't worry about this for now
- Preferred style for README visual asset (diagram vs banner) and who will produce it?
  - i'll handle the image, just insert a placeholder line for it in the README
