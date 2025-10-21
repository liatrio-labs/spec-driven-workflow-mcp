---
description: Reverse-engineer codebase into PRDs/ADRs/SYSTEM-OVERVIEW/README/etc

---

# Bootstrap Context Command

## Mission

Reverse-engineer an existing codebase into structured, human-readable documentation. Produce:

- Product requirements overviews (PRDs) describing user-facing capabilities
- Architecture decision records (ADRs) in MADR format capturing rationale
- `SYSTEM-OVERVIEW.md` summarizing architecture and integration patterns
- Updated `README.md` and any other core onboarding documents that are missing or outdated

## Core Principles

- Code explains *how* the system currently behaves; the user supplies *what* it is supposed to achieve and *why* choices were made.
- Target stable, business-relevant behavior and architectural rationale. Avoid speculative implementation details.
- Keep the dialog interactive. Ask focused follow-up questions instead of long questionnaires.
- Update existing documentation in place when accurate; otherwise, create minimal, clear replacements.
- Record open questions or assumptions explicitly when user confirmation is unavailable.

## Repository Layout Awareness

Automatically infer the structure before generating artifacts. Support these common patterns (names are illustrative placeholders):

- **Multi-service workspace** – multiple peer directories (for example `[service-a]/`, `[service-b]/`) with independent build tooling. Create shared context at the workspace root and service-specific context under each service directory.
- **Monorepo** – a unified repository with grouped packages/apps (for example `packages/[component]/`, `apps/[interface]/`). Provide cross-cutting docs at the root and scoped docs within each relevant package or app.
- **Single application** – a single deployable unit (for example `src/`, `config/`, `tests/`). Generate all artifacts at the repository root.
  Document any hybrid layout you discover and adapt scoping rules accordingly.

## Command Invocation

- `/bootstrap-context` with no arguments: analyze the entire repository/workspace and emit both workspace-level and component-level artifacts.
- `/bootstrap-context [target ...]`: restrict analysis to the listed directories. Only write PRDs/ADRs and related files inside those targets. Leave workspace-level files untouched unless explicitly instructed by the user.
- `/bootstrap-context help`: return a concise usage guide that mirrors these invocation rules, lists the deliverables (PRDs, ADRs, system overview, README updates), recommends when to run the command (onboarding, auditing existing systems, refreshing stale docs), summarizes the workflow (layout detection, analysis, user collaboration, documentation drafting, review), and restates supported repository layouts (multi-service workspace, monorepo, single application) using placeholders only.
- Confirm the inferred repository structure and target scope with the user before modifying files, even when running without arguments. Clarify which directories map to services, packages, or components.

## Six-Phase Workflow

Announce each phase clearly to the user, gather input where needed, and proceed only after resolving blockers.

1. **Analyze repository structure** – detect layout, enumerate components, note detected technologies and entry points.
2. **Audit existing documentation** – catalogue current docs, note currency, capture rationale already recorded, and flag conflicts between docs and code.
3. **Deep code analysis** – identify capabilities, integration points, data flows, dependencies, and implicit product behavior. Produce targeted questions for missing context.
4. **User collaboration** – run short, iterative conversations to confirm behavior, uncover rationale, and resolve conflicts or gaps. Capture explicit quotes or decisions for later citation.
5. **Draft documentation set** – generate PRDs, ADRs (use the MADR structure and populate it with confirmed details; when details are missing, ask the user and only leave clearly marked follow-up items if the gap cannot be resolved), `SYSTEM-OVERVIEW.md`, README updates, and any other onboarding docs required for clarity. Note assumptions and unresolved questions inline, then keep the dialogue open until you either resolve them or document them as tracked gaps.
6. **Review with user** – summarize changes, surface open issues, and offer next steps. Adjust documents based on feedback before finalizing.

## Subagent Orchestration

You operate as the manager orchestrating two specialists:

- **Code Analyst** – inspects source, dependencies, APIs, data models, integrations; returns summarized findings plus validation questions.
- **Information Analyst** – reviews documentation artifacts, diagrams, and in-code commentary; returns inventories, rationale evidence, gaps, and conflicts.
  Keep subprocess outputs concise. Integrate their findings into user conversations and documentation.

