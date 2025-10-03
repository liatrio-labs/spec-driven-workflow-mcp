# Spec: Spec-Driven Development MCP Proof of Concept

## Introduction/Overview

Deliver a FastMCP-based server that exposes the existing Spec Driven Development (`prompts/`) guidance as Model Context Protocol primitives so engineers and AI assistants can orchestrate the SDD workflow from any MCP-aware client. The proof of concept (POC) must demonstrate local (`uvx`) and Kubernetes-hosted operation, enabling users to generate specs, derive task lists, and manage implementation checkpoints end-to-end while showcasing the broader capabilities of MCP (Prompts, Resources, Tools, ResourceTemplates, Notifications, and Sampling). All generated artifacts stay on the user's filesystem in a user-defined workspace; the server only brokers access to those local files and provides no remote persistence layer. The repository `tasks/` directory remains development-only and must not be exposed by the server at runtime.

## Goals

- Provide a FastMCP server that runs via STDIO and HTTP transports, accessible locally and through Kubernetes deployment.
- Expose the `generate-spec`, `generate-task-list-from-spec`, and `manage-tasks` prompts as MCP prompts/resources without altering their Markdown content.
- Support a demonstrable round-trip workflow: create a spec, transform it into a task list, and manage progress using the provided prompts, resources, and helper tools, with all outputs remaining in the user-selected workspace (not the development-only `tasks/` directory).
- Package the server for containerized deployment (Docker + Kustomize) with clear operational documentation, including reference `fastmcp.json` definitions for dev/prod.
- Illuminate advanced MCP primitives (ResourceTemplates, Notifications, Sampling) so future iterations can extend automation and collaboration patterns.

## User Stories

- **Story 1 – Engineer discovery:** As a Liatrio engineer, I can connect the FastMCP Inspector to the server to browse available prompts and resources so I understand how to drive the SDD workflow.
- **Story 2 – AI-driven authoring:** As an AI assistant connected to the server, I can invoke the exposed prompts to generate a new specification and derivative task list stored in `/tasks/`, ensuring consistency across tooling.
- **Story 3 – Platform deployment:** As a platform engineer, I can deploy the packaged server to a Kubernetes cluster using the provided Kustomize manifest so teams can access the MCP endpoint internally.
- **Story 4 – Client integration:** As an engineer using another MCP-aware client, I can register the remote server URL and call prompts/resources over HTTP to execute the SDD workflow without local setup.

## Demoable Units of Work

### Slice 1 – FastMCP server foundation

- **Purpose & Users:** Establish a runnable FastMCP server for Liatrio engineers and AI assistants.
- **Demo Criteria:** Start the server via `uvx fastmcp run ...` (STDIO) and `fastmcp run ... --transport http --port 8000`; Inspector lists all prompts/resources.
- **Proof Artifact(s):** Terminal session transcript; screenshot of FastMCP Inspector showing prompt catalogue.

### Slice 2 – End-to-end SDD round trip

- **Purpose & Users:** Demonstrate spec generation, task list creation, and task management via MCP calls for engineers and assistants.
- **Demo Criteria:** Using the Inspector (or scripted client), trigger `generate-spec` to produce a spec in `/tasks/`, follow with `generate-task-list-from-spec`, and reference `manage-tasks` guidance during review.
- **Proof Artifact(s):** Sample generated spec and task list saved inside a demo workspace mount (e.g., `/workspace/sdd/0001-spec-sdd-mcp-poc.md`); recorded interaction log or Markdown transcript.

### Slice 3 – Client integration via HTTP transport

- **Purpose & Users:** Validate consumption from a secondary MCP-aware client.
- **Demo Criteria:** Configure an external MCP client (e.g., Claude Desktop, VS Code MCP plugin) to reach the server over HTTP and successfully invoke prompts.
- **Proof Artifact(s):** Connection configuration snippet; client-side screenshot/log showing prompt execution.

### Slice 4 – Deployable packaging

- **Purpose & Users:** Provide operational packaging for platform engineers.
- **Demo Criteria:** Build container image locally, apply Kustomize overlay to deploy in a test cluster, and confirm `/mcp` endpoint readiness probe succeeds.
- **Proof Artifact(s):** Docker build log, Kubernetes deployment manifest, `kubectl` output validating pod readiness.

### Slice 5 – Protocol extensions showcase

- **Purpose & Users:** Demonstrate FastMCP-specific protocol capabilities that enrich the SDD workflow for engineers and AI assistants.
- **Demo Criteria:** Trigger a sampling request from the server (e.g., prompt the client LLM to draft a spec summary) and emit a notification when new artifacts land in `/tasks/`; verify both in the Inspector or alternate client.
- **Proof Artifact(s):** Recorded interaction showing sampling exchange, notification payload captured via client logs.

## Functional Requirements

1. Build the server with FastMCP (`fastmcp.FastMCP`) and dynamically register Markdown prompts in `prompts/` as MCP Prompts, annotating each with `_meta` tags that distinguish spec authoring, task management, and documentation flows.
2. Expose complementary Resources for reference materials (e.g., `resource://docs/readme`, `resource://prompts/manage_tasks`) so clients can fetch guidance without direct filesystem access.
3. Provide ResourceTemplates that map generated artifacts within a user-configurable workspace root (e.g., `resource://workspace/specs/{spec_id}`), ensuring the server reads directly from user-mounted storage without replicating data elsewhere or exposing the repository `tasks/` directory.
4. Supply helper Tools (e.g., `list_task_files`, `create_spec_stub`, `summarize_spec_diff`) to demonstrate MCP tool usage while keeping the Markdown-driven workflow optional and intact.
5. Emit MCP Notifications when new artifacts are written and support a Sampling request path where the server can ask the client LLM to generate content snippets (e.g., spec overview paragraphs).
6. Enable STDIO and HTTP transports with configurable port/host (default `8000`), defined in a checked-in `fastmcp.json`; document `fastmcp run` usage for both dev and prod variants.
7. Pin FastMCP and related dependencies to exact versions in `pyproject.toml`, and document `uv sync`, `uvx fastmcp run`, and `fastmcp project prepare` flows for reproducible environments.
8. Provide Dockerfile, `uv`/`uvx` entrypoints, and a minimal Kustomize overlay to deploy the server in Kubernetes with configurable filesystem roots, readiness probes, and secrets for future auth, while keeping all generated artifacts on the mounted local volume owned by the user and excluding the repository `tasks/` directory from exposure.
9. Produce operator documentation covering transports, environment variables, filesystem mounts, and reference configurations for common MCP clients (FastMCP Inspector, Claude Desktop, VS Code MCP plugin), including CORS/header expectations.
10. Implement structured logging, `/mcp/health` (or equivalent) readiness endpoints, and basic metrics to aid observability in both local and cluster deployments.
11. Author atomic asyncio tests that verify prompt/resource/tool registration and exercise notification/sampling flows without cross-test coupling.
12. Persist generated artifacts to the user-defined workspace following naming conventions from `generate-spec.md` and `generate-task-list-from-spec.md`, ensuring ResourceTemplates surface them immediately while reaffirming that storage stays local and isolated from the repository `tasks/` directory.

## Non-Goals (Out of Scope)

- Implementing advanced authentication/authorization (OAuth, SSO) or multi-tenant isolation.
- Providing direct integrations with external work-tracking systems (Jira, GitHub Issues) beyond documentation references.
- Persisting conversational state or task progress beyond Markdown artifacts in the repository storage.
- Building a full web UI; the POC focuses on MCP clients (Inspector, CLI, AI tools).

## Design Considerations (Optional)

- Maintain prompt text in `prompts/` as the single source of truth; server code should load them dynamically so updates require no redeploy beyond file sync.
- Use `_meta` tagging conventions to group prompts/resources/tools (e.g., `mcp.liatrio/sdd/spec`, `mcp.liatrio/sdd/tasks`) to improve discovery in heterogeneous clients.
- Surface README excerpts or onboarding notes as Resource templates so clients can present curated onboarding content without bespoke tooling.

## Technical Considerations (Optional)

- Utilize FastMCP root mounting so repository prompts are exposed read-only and user workspaces can be mounted read-write when desired; never expose the repository `tasks/` directory to clients.
- Document how to switch between stdio and HTTP transports, including environment variables for base paths when running in containers (e.g., bind-mount prompts and user workspace directories) and how `fastmcp.json` options map to these environments, keeping generated files on user-controlled storage and excluding the development-only `tasks/` directory.
- Leverage FastMCP tooling decorators to implement optional helper tools (file list, template initialization) without altering the Markdown-driven workflow, demonstrating broader MCP capabilities requested by the user.
- Capture patterns for running `fastmcp project prepare` with pre-built environments to accelerate cold starts in Kubernetes or CI.
- Plan for future auth integration by abstracting transport configuration (placeholders for headers, API keys) though not implemented in the POC, and note potential use of FastMCP auth middlewares.

## Success Metrics

- Server starts locally via `uvx` and is reachable via HTTP with listed prompts/resources/tools.
- At least one documented round-trip demonstrates generating a spec and corresponding task list using only MCP interactions.
- Container image builds successfully in CI and deploys with provided Kustomize manifest, passing readiness checks in a test cluster.
- External MCP client successfully connects and executes prompts without manual content transfer, including successful sampling and notification handling in at least one client.
- Automated test suite validates prompt/resource/tool registration and notification/sampling flows with atomic coverage.

## Testing Setup

- **Tooling:** Add `pytest`, `pytest-asyncio`, and `anyio` as development dependencies in `pyproject.toml`; standardize on `uv run pytest`.
- **Fixtures:** Provide `tests/conftest.py` fixtures that spin up the FastMCP server with temporary workspace directories (using `tempfile.TemporaryDirectory()`) to ensure repo `tasks/` stays isolated.
- **Atomic async tests:**
  - Verify prompt registration and `_meta` tagging (`test_prompts.py`).
  - Validate resource/resource-template access against the temp workspace (`test_resources.py`).
  - Exercise helper tools, sampling mocks, and notification dispatch (`test_tools_protocol.py`).
- **HTTP client integration:** Use `fastmcp.Client` inside `pytest.mark.asyncio` tests to call prompts/tools over the HTTP transport and assert responses.
- **Pre-commit / CI:** Document optional `pre-commit` hook for `uv run pytest` and require the CI pipeline to execute the full test suite on every push.

## Open Questions

- What authentication (if any) will be required when exposing the server beyond internal networks, and how should that influence future iterations?
- Should generated artifacts be automatically committed/persisted outside the runtime filesystem (e.g., pushed to Git) or remain manual?
- Are additional prompts/tools needed to support implementation phases (beyond spec/task list) in future roadmap iterations?
- How should versioning of prompts and generated artifacts be tracked to support reproducibility across clients?
