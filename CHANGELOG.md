# CHANGELOG

<!-- version list -->

## v1.4.0 (2025-10-18)

### Bug Fixes

- Correct typo ([#11](https://github.com/liatrio-labs/spec-driven-workflow/pull/11),
  [`cdb0bd9`](https://github.com/liatrio-labs/spec-driven-workflow/commit/cdb0bd933c780afc8357db3aac78496f003f534c))

### Features

- Add opencode configuration ([#11](https://github.com/liatrio-labs/spec-driven-workflow/pull/11),
  [`cdb0bd9`](https://github.com/liatrio-labs/spec-driven-workflow/commit/cdb0bd933c780afc8357db3aac78496f003f534c))

- **ci**: Enhance opencode workflow with comprehensive triggers
  ([#11](https://github.com/liatrio-labs/spec-driven-workflow/pull/11),
  [`cdb0bd9`](https://github.com/liatrio-labs/spec-driven-workflow/commit/cdb0bd933c780afc8357db3aac78496f003f534c))

- **ci**: Restrict opencode workflow to authorized users only
  ([#11](https://github.com/liatrio-labs/spec-driven-workflow/pull/11),
  [`cdb0bd9`](https://github.com/liatrio-labs/spec-driven-workflow/commit/cdb0bd933c780afc8357db3aac78496f003f534c))


## v1.3.1 (2025-10-18)

### Bug Fixes

- Remove title field from generate-spec prompt
  ([#12](https://github.com/liatrio-labs/spec-driven-workflow/pull/12),
  [`a58be56`](https://github.com/liatrio-labs/spec-driven-workflow/commit/a58be5602a2b9527758d581d57a299a1d33190e8))

- Update repo name in chainguard config
  ([#14](https://github.com/liatrio-labs/spec-driven-workflow/pull/14),
  [`0696e5d`](https://github.com/liatrio-labs/spec-driven-workflow/commit/0696e5dd02871a86f3ccd0793ac509535473c3de))


## v1.3.0 (2025-10-16)

### Bug Fixes

- Make entry point callable for console script
  ([#10](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/10),
  [`17cffda`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/17cffdadda0f58046f7c6e84b2974c44070264ba))

### Features

- Add CLI entry point and include prompts in package
  ([#10](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/10),
  [`17cffda`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/17cffdadda0f58046f7c6e84b2974c44070264ba))


## v1.2.0 (2025-10-16)

### Bug Fixes

- Add newline at end of claude.yml
  ([`d03e86e`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/d03e86ea47de61a151830ed313426fd0cf3e356d))

- Trigger on issue edited instead of assigned
  ([`d03e86e`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/d03e86ea47de61a151830ed313426fd0cf3e356d))

### Chores

- Remove automatic PR review workflow
  ([`d03e86e`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/d03e86ea47de61a151830ed313426fd0cf3e356d))

### Features

- Add timeout and concurrency controls to Claude workflow
  ([`d03e86e`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/d03e86ea47de61a151830ed313426fd0cf3e356d))

- Restrict Claude workflow to authorized users only
  ([`d03e86e`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/d03e86ea47de61a151830ed313426fd0cf3e356d))

### Refactoring

- Simplify author association checks
  ([`d03e86e`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/d03e86ea47de61a151830ed313426fd0cf3e356d))


## v1.1.0 (2025-10-15)

### Bug Fixes

- Address coderabbit review feedback
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

- Remove unnecessary bootstrap file
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

- **prompts**: Construct prompt content with TextContent
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

### Build System

- Configure dev tooling for pre-commit
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

### Chores

- Linter fix ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

- Mark task 1.0 as complete ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

- Rebase cleanup ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

- Remove pytest-anyio package, it's not necessary
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

### Documentation

- Add operations guide and update README
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

- Add spec for initial MCP implementation
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

- Update task status and mark deferred features
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

### Features

- Establish FastMCP server foundation
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

### Refactoring

- Adopt standard FastMCP server.py convention
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))

- **prompts**: Model markdown prompt metadata
  ([#2](https://github.com/liatrio-labs/spec-driven-workflow-mcp/pull/2),
  [`0b4044d`](https://github.com/liatrio-labs/spec-driven-workflow-mcp/commit/0b4044d1f836d62028c5e788c8ec43dee3ef1520))


## v1.0.0 (2025-10-10)

- Initial Release
