# Task List: Spec-Driven Development MCP POC

## Relevant Files

- `mcp_server/__init__.py` - FastMCP application factory and transport wiring.
- `mcp_server/config.py` - Runtime configuration (workspace root, transport options, logging).
- `mcp_server/prompts_loader.py` - Dynamic loader for Markdown prompts in `prompts/`.
- `mcp_server/resources.py` - Resource and ResourceTemplate definitions surfacing docs and workspace artifacts.
- `mcp_server/tools.py` - Helper tools (listing artifacts, creating stubs, summarizing diffs).
- `mcp_server/notifications.py` - Notification dispatch helpers for artifact events.
- `mcp_server/sampling.py` - Sampling orchestration utilities for delegated LLM content.
- `mcp_server/logging.py` - Structured logging setup and metrics hooks.
- `fastmcp.json` - Transport presets for STDIO and HTTP operation.
- `Dockerfile` - Container image definition with `uv`/`uvx` entrypoints.
- `kustomize/overlays/dev/kustomization.yaml` - Dev overlay for Kubernetes deployment.
- `kustomize/overlays/dev/deployment.yaml` - Deployment manifest with readiness probe and volume mounts.
- `tests/conftest.py` - Pytest fixtures spinning up temporary workspace directories.
- `tests/test_prompts.py` - Tests covering prompt registration and `_meta` tagging.
- `tests/test_resources.py` - Tests exercising resources and resource templates.
- `tests/test_tools_protocol.py` - Tests covering helper tools, notifications, and sampling flows.
- `docs/operations.md` - Operator documentation for transports, configs, and MCP clients.
- `docs/workspace-examples/` - Sample generated specs/task lists demonstrating round-trip workflow.

### Notes

- Keep repository `tasks/` directory internal; mount user-defined workspaces for generated artifacts at runtime.
- Use `uv sync` for environment setup and `uv run pytest` for automated tests.
- Follow `_meta` tagging conventions to group MCP prompts/resources/tools for discovery.
- Document FastMCP Inspector, Claude Desktop, and VS Code MCP plugin integration paths.
- Use the Tavily, FastMCP, and Context7 MCPs to reference documentation and best practices for all relevant tools as implementation proceeds.
- Stand up testing scaffolding at project start so every slice can follow a TDD loop (write failing test, implement, refactor) before expanding features.
- Leverage `uv` and `fastmcp` project scaffolding (e.g., `fastmcp project init`, `uv init`) during setup to enforce consistent structure, lock dependencies, and accelerate first runnable server builds.

## Tasks

- [~] 1.0 Establish FastMCP server foundation
  - Demo Criteria: Run `uvx fastmcp run mcp_server:app` for STDIO and `fastmcp run --transport http --port 8000` so Inspector lists prompts/resources/tools.
  - Proof Artifact(s): Terminal recording of both transports; Inspector screenshot capturing catalog entries with `_meta` tags.
  - [x] 1.1 Define package layout (`mcp_server/`, `tests/`, `docs/`) and configure `pyproject.toml` pinning FastMCP plus dev dependencies.
  - [x] 1.2 Implement `mcp_server/config.py` for workspace paths, transports, logging, and environment overrides with testable defaults.
  - [x] 1.3 Build `mcp_server/prompts_loader.py` to ingest Markdown prompts with `_meta` tagging and expose them via FastMCP prompts API.
  - [x] 1.4 Scaffold `mcp_server/__init__.py` application factory registering prompts, resources, tools, notifications, and sampling stubs.
  - [x] 1.5 Create initial pytest fixtures and failing tests (`tests/test_prompts.py`) exercising prompt registration to drive TDD cycle.
  - [ ] 1.6 Document local execution workflow in `README.md` and `docs/operations.md`, including STDIO vs HTTP invocation examples.

- [ ] 2.0 Deliver end-to-end SDD round trip via MCP
  - Demo Criteria: Invoke `generate-spec`, `generate-task-list-from-spec`, and `manage-tasks` prompts through MCP to create artifacts inside a mounted workspace.
  - Proof Artifact(s): Sample spec and task list files under `/workspace/sdd/`; execution transcript or Markdown log of the workflow.
  - [ ] 2.1 Implement workspace ResourceTemplates mapping spec/task artifacts under configurable root while excluding repo `tasks/`.
  - [ ] 2.2 Add helper tool(s) enabling artifact creation/listing tied to user workspace, ensuring idempotent operations.
  - [ ] 2.3 Execute TDD loop for `tests/test_resources.py` covering resource/template discovery and workspace isolation.
  - [ ] 2.4 Capture demo workspace examples (`docs/workspace-examples/`) generated entirely via MCP interactions.
  - [ ] 2.5 Update documentation describing the round-trip flow and how to mount external workspaces during runs.

- [ ] 3.0 Validate remote MCP client integration
  - Demo Criteria: Connect a secondary MCP-aware client (e.g., Claude Desktop) over HTTP to trigger prompts and tools successfully.
  - Proof Artifact(s): Connection configuration snippet and client-side screenshot/log showing prompt execution results.
  - [ ] 3.1 Harden HTTP transport configuration (CORS headers, host/port envs) in `fastmcp.json` and `mcp_server/config.py`.
  - [ ] 3.2 Draft client onboarding instructions in `docs/operations.md` for FastMCP Inspector, Claude Desktop, and VS Code MCP plugin.
  - [ ] 3.3 Record validated client session (screenshots/logs) invoking prompts/resources via HTTP endpoint.
  - [ ] 3.4 Add integration test (async) using `fastmcp.Client` to call prompts over HTTP within pytest suite.

- [ ] 4.0 Package and deploy for Kubernetes
  - Demo Criteria: Build Docker image, apply Kustomize overlay to deploy in a test cluster, and verify `/mcp/health` readiness plus metrics endpoints.
  - Proof Artifact(s): Docker build log, rendered Kubernetes manifest, and `kubectl` output confirming pod readiness.
  - [ ] 4.1 Author Dockerfile leveraging `uv` for dependency sync and multi-stage build with non-root runtime user.
  - [ ] 4.2 Provide container entrypoints/scripts (`uvx fastmcp run`) supporting both STDIO and HTTP configurations.
  - [ ] 4.3 Create base and overlay Kustomize manifests defining config maps, secrets placeholders, volume mounts, and readiness probes.
  - [ ] 4.4 Document Kubernetes deployment process and environment variables in `docs/operations.md` including sample manifests.
  - [ ] 4.5 Run deployment smoke test (kind or remote cluster) capturing `kubectl` outputs and `/mcp/health` check results.

- [ ] 5.0 Showcase protocol extensions and observability
  - Demo Criteria: Trigger helper tools, emit notifications on new artifacts, exercise sampling request flow, and capture structured logs/metrics.
  - Proof Artifact(s): Test run outputs covering tools/notifications/sampling; log excerpts illustrating structured events and metrics export.
  - [ ] 5.1 Implement `mcp_server/tools.py` helper tools (list artifacts, create spec stub, summarize diff) with corresponding FastMCP decorators.
  - [ ] 5.2 Build notification broadcaster (`mcp_server/notifications.py`) emitting events on workspace file creation with hooks into FastMCP emitter.
  - [ ] 5.3 Implement sampling orchestrator (`mcp_server/sampling.py`) requesting client-generated summaries and handling responses.
  - [ ] 5.4 Add structured logging/metrics setup (`mcp_server/logging.py`) and expose `/mcp/health` readiness route.
  - [ ] 5.5 Drive TDD cycle for `tests/test_tools_protocol.py` validating tools, notifications, sampling, and logging signals.
  - [ ] 5.6 Capture observability outputs (logs, metrics sample) and summarize guidance in `docs/operations.md`.
