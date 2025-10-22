# Specification: Python-Driven Slash Command Generator

## Introduction/Overview

The Spec Driven Development (SDD) workflow currently exposes its three core prompts (`generate-spec`, `generate-task-list-from-spec`, `manage-tasks`) through an MCP server. However, MCP prompt support is not uniformly implemented across AI coding tools, creating friction for users who want to leverage these prompts in their preferred development environment.

This feature solves that problem by generating native slash commands for 14+ AI coding tools (Claude Code, Cursor, Windsurf, Gemini CLI, etc.) directly from the existing prompt files. Users will be able to run a single command to generate slash commands for all their configured AI tools, making the SDD workflow universally accessible regardless of tool choice.

The solution will be entirely Python-driven (no bash scripts), use Test-Driven Development (TDD), and integrate seamlessly with the existing codebase infrastructure.

## Goals

1. Enable users to generate native slash commands for 14+ AI coding tools from SDD's existing prompt files
2. Auto-detect which AI tools are configured in a target project
3. Provide an interactive CLI with Typer that allows users to review and modify tool selection before generation
4. Support safe overwriting with options to cancel, overwrite, or backup existing commands
5. Maintain extensibility through a simple base class system for adding new AI tools
6. Build the feature using strict TDD methodology with comprehensive unit test coverage
7. Support agent-specific metadata overrides in prompt frontmatter

## User Stories

1. **As a developer using Claude Code**, I want to generate `/sdd-generate-spec`, `/sdd-generate-task-list-from-spec`, and `/sdd-manage-tasks` slash commands in my project so that I can use the SDD workflow natively without relying on MCP.

2. **As a team lead**, I want to generate slash commands for multiple AI tools (Cursor, Windsurf, Claude Code) so that team members can use the SDD workflow regardless of their preferred IDE.

3. **As a developer maintaining SDD prompts**, I want to periodically regenerate slash commands when prompts are updated so that all projects stay in sync with the latest workflow improvements.

4. **As a solo developer**, I want the tool to auto-detect which AI coding tools I have configured (by checking for `.claude/`, `.cursor/`, etc.) and present me with an editable list so I don't generate unnecessary files.

5. **As a cautious user**, I want to be prompted before overwriting existing slash commands, with options to cancel, overwrite, or create backups, so I don't accidentally lose customizations.

6. **As a contributor**, I want to easily add support for new AI tools by implementing a simple base class so that the codebase stays maintainable as the ecosystem evolves.

## Demoable Units of Work

### Slice 1: Core Data Models & Configuration

**Purpose**: Establish the foundational data structures for agent configurations and prompt formats.
**Users**: Internal (developers working on subsequent slices)
**Demo Criteria**:

- `AgentConfig` dataclass can represent 14 AI tools with their directory paths, formats, and file extensions
- `CommandFormat` enum distinguishes between Markdown and TOML formats
- `SUPPORTED_AGENTS` list contains all 14 agents
**Proof Artifacts**:
- Run: `pytest tests/test_config.py -v`
- All tests pass demonstrating proper data model initialization

### Slice 2: Format Generators (Markdown & TOML)

**Purpose**: Convert `MarkdownPrompt` objects into agent-specific command file formats.
**Users**: Internal (writer module depends on this)
**Demo Criteria**:

- `MarkdownCommandGenerator` produces valid `.md` files with frontmatter and `$ARGUMENTS` placeholder
- `TomlCommandGenerator` produces valid `.toml` files with `{{args}}` placeholder
- Both generators handle agent-specific metadata overrides from prompt frontmatter
**Proof Artifacts**:
- Run: `pytest tests/test_generators.py -v`
- Generated output files match expected format snapshots

### Slice 3: Slash Command Writer Module

**Purpose**: Orchestrate prompt loading and command file generation for multiple agents.
**Users**: CLI (depends on this), Python API users
**Demo Criteria**:

- `SlashCommandWriter` can load all prompts from `/prompts` directory
- Can generate commands for a single agent with specified prefix
- Can generate commands for multiple agents in one call
- Respects dry-run mode (returns what would be created without writing files)
**Proof Artifacts**:
- Run: `pytest tests/test_writer.py -v`
- Test output shows correct file paths and counts for multi-agent generation

### Slice 4: Interactive CLI with Auto-Detection

**Purpose**: Provide a Typer-based CLI that auto-detects configured AI tools and presents an editable selection list.
**Users**: Developers running the command in their projects
**Demo Criteria**:

- Running `sdd-generate-commands` in a project with `.claude/` and `.cursor/` directories auto-detects both
- Presents interactive checklist allowing user to enable/disable detected agents
- Supports `--agents` flag for non-interactive explicit selection
- Supports `--list-agents` to show all 14 supported tools
- Supports `--dry-run` to preview without writing
**Proof Artifacts**:
- Run: `sdd-generate-commands --list-agents` (shows all 14 agents)
- Run in test project: shows detected agents with interactive prompt
- Screenshot/terminal recording of interactive selection flow

### Slice 5: Safe Overwrite Handling

**Purpose**: Detect existing slash command files and prompt user for action.
**Users**: Developers regenerating commands or running in existing projects
**Demo Criteria**:

- When existing commands detected, presents options: Cancel, Overwrite, Backup+Overwrite
- Backup option creates `.bak` files with timestamps
- Cancel option exits without changes
- User choice applies to all files or can be per-file (configurable)
**Proof Artifacts**:
- Run in project with existing commands: shows prompt with 3 options
- Choose "Backup+Overwrite": verify `.bak` files created with timestamp
- Run: `ls -la .claude/commands/*.bak` (shows backup files)

### Slice 6: Agent-Specific Metadata Overrides

**Purpose**: Allow prompts to specify different descriptions or settings per agent.
**Users**: SDD maintainers customizing prompt behavior per tool
**Demo Criteria**:

- Prompt YAML frontmatter supports `agent_overrides` section
- Example: Different descriptions for Claude Code vs Gemini CLI
- Generators apply overrides when present, fall back to defaults otherwise
**Proof Artifacts**:
- Modified prompt file with `agent_overrides` section
- Run generation: verify different descriptions in `.claude/commands/` vs `.gemini/commands/`
- Run: `diff .claude/commands/sdd-generate-spec.md .gemini/commands/sdd-generate-spec.toml` (shows description differences)

### Slice 7: Documentation & Integration

**Purpose**: Document the feature for users and integrate into existing project patterns.
**Users**: SDD users, contributors
**Demo Criteria**:

- README.md has brief overview and link to detailed docs
- `/docs/slash-command-generator.md` contains comprehensive usage guide
- `pyproject.toml` includes `sdd-generate-commands` script entry point
- `pyproject.toml` includes Typer as dependency
**Proof Artifacts**:
- View: `/docs/slash-command-generator.md` (comprehensive guide exists)
- Run: `sdd-generate-commands --help` (shows usage from installed package)
- README has link to new docs file

## Functional Requirements

### Core Generation (FR1-FR5)

**FR1**: The system must load prompt files from `/prompts` directory using the existing `load_markdown_prompt` function from `mcp_server/prompt_utils.py`.

**FR2**: The system must support generating slash commands for exactly 14 AI coding tools:

- Claude Code (`.claude/commands/*.md`)
- Cursor (`.cursorrules/commands/*.md`)
- Windsurf (`.windsurfrules/commands/*.md`)
- Gemini CLI (`.gemini/commands/*.toml`)
- GitHub Copilot (`.github/copilot/commands/*.md`)
- opencode (`.opencode/commands/*.md`)
- Codex CLI (`.codex/commands/*.md`)
- Kilo Code (`.kilo/commands/*.md`)
- Auggie CLI (`.auggie/commands/*.md`)
- Roo Code (`.roo/commands/*.md`)
- CodeBuddy CLI (`.codebuddy/commands/*.md`)
- Amazon Q Developer (`.aws/q/commands/*.md`)
- Amp (`.amp/commands/*.md`)
- Qwen Code (`.qwen/commands/*.toml`)

**FR3**: The system must generate commands with a fixed prefix `sdd-` (e.g., `/sdd-generate-spec`).

**FR4**: The system must support two output formats:

- **Markdown** (`.md`): YAML frontmatter + prompt body, uses `$ARGUMENTS` placeholder
- **TOML** (`.toml`): TOML-formatted command block, uses `{{args}}` placeholder

**FR5**: The system must create necessary parent directories if they don't exist (e.g., create `.claude/commands/` if missing).

### Auto-Detection & Interactive Selection (FR6-FR8)

**FR6**: The system must auto-detect configured AI tools by checking for the presence of their configuration directories in the target project (e.g., `.claude/`, `.cursor/`, `.windsurf/`).

**FR7**: The system must present an interactive selection of detected agents using Typer's `typer.confirm()` or custom prompts, allowing users to enable/disable specific tools before generation proceeds. For multi-selection, use a library like `questionary` or prompt for each agent individually.

**FR8**: The system must support non-interactive mode via `--agents` CLI option for explicit agent selection (e.g., `--agents claude-code cursor`). This ensures the tool can be used in automated scripts and CI/CD pipelines.

### Safe Overwriting (FR9-FR11)

**FR9**: The system must detect if target slash command files already exist before writing.

**FR10**: When existing files are detected, the system must prompt the user with three options using `typer.prompt()` with a custom choice prompt or individual `typer.confirm()` calls:

- **Cancel**: Exit without making changes (use `raise typer.Abort()`)
- **Overwrite**: Replace existing files
- **Backup+Overwrite**: Create timestamped `.bak` files before replacing

**FR11**: Backup files must use the format `{original-filename}.{timestamp}.bak` (e.g., `sdd-generate-spec.md.20250121-143052.bak`).

### Extensibility (FR12-FR13)

**FR12**: The system must provide a `CommandGenerator` abstract base class with a single `generate()` method that subclasses implement for specific formats.

**FR13**: Adding support for a new AI tool must require only:

1. Adding a new `AgentConfig` entry to `SUPPORTED_AGENTS`
2. Optionally creating a new `CommandGenerator` subclass if a new format is needed

### Metadata & Overrides (FR14-FR15)

**FR14**: The system must support agent-specific metadata overrides in prompt frontmatter using an `agent_overrides` section:

```yaml
---
name: generate-spec
description: Default description
agent_overrides:
  gemini-cli:
    description: "Custom description for Gemini CLI"
  cursor:
    description: "Custom description for Cursor"
---
```

**FR15**: When generating commands, the system must apply agent-specific overrides if present, otherwise use default metadata values.

### CLI Interface (FR16-FR21)

**FR16**: The system must provide a Typer-based CLI accessible via `sdd-generate-commands` command.

**FR17**: The CLI must support the following options using Typer's `Annotated` syntax for type clarity:

- `--target-dir PATH`: Target project directory (default: current directory)
- `--prompts-dir PATH`: Source prompts directory (default: package's `/prompts`)
- `--agents [NAMES...]`: Explicitly specify agents (disables auto-detect and interactive prompts)
- `--dry-run`: Show what would be generated without writing files
- `--list-agents`: Display all supported agents and exit
- `--yes` / `-y`: Skip all confirmation prompts (auto-confirm for CI/CD usage)

**FR18**: The CLI must default to generating commands in the current working directory.

**FR19**: The CLI must display a summary of generated files grouped by agent after completion.

**FR20**: The CLI must use clear, colored output via Typer's built-in Rich integration (automatically enabled when Rich is installed) to distinguish between normal messages, warnings, and errors. Use `typer.secho()` or `rich.console.Console` for styled output.

**FR21**: The CLI must exit with appropriate status codes:

- `0`: Success
- `1`: User cancelled operation
- `2`: Validation error (e.g., invalid agent name)
- `3`: I/O error (e.g., permission denied)

### Testing Requirements (FR22-FR24)

**FR22**: The system must be developed using Test-Driven Development (TDD), where tests are written before implementation code.

**FR23**: The system must have unit tests covering:

- Configuration data models (`test_config.py`)
- Format generators for Markdown and TOML (`test_generators.py`)
- Writer module for single-agent and multi-agent generation (`test_writer.py`)
- CLI argument parsing and validation (`test_cli.py`)

**FR24**: Tests must use pytest fixtures with appropriate scopes:

- Use `function` scope (default) for test-specific fixtures that need isolation
- Use `module` or `session` scope for expensive setup like sample prompt files
- Leverage fixture parametrization for testing multiple agent configurations
- Organize shared fixtures in `tests/conftest.py` for reusability
- Use `tmp_path` fixture (built-in) for temporary directories instead of custom solutions

## Non-Goals (Out of Scope)

1. **Watch Mode**: Automatic regeneration when prompt files change is not included in this iteration. Users must manually run the command when prompts are updated.

2. **MCP Tool Integration**: The slash command generator will not be exposed as an MCP tool in the initial implementation. It remains a standalone CLI utility.

3. **Configuration File Support**: No `.sdd-commands.yaml` or similar config file support. All options must be provided via CLI flags or interactive prompts.

4. **Windows Path Support**: Cross-platform file path handling is not a priority for the initial release. Unix-style paths are sufficient, though if Pathlib naturally handles Windows paths without extra work, that's acceptable.

5. **CI/CD Integration**: No pre-built GitHub Actions or CI/CD workflows for automated command generation.

6. **Versioning & Migrations**: No version tracking of generated commands or automatic migration when the SDD prompt format changes.

7. **Custom Format Plugins**: While extensibility is supported through base classes, loading external format generator plugins is out of scope.

8. **Partial Updates**: No support for updating a single command file. The tool operates at the agent level (regenerate all commands for an agent).

9. **Command Validation**: No runtime validation that generated commands work correctly in target AI tools (e.g., syntax checking TOML).

## Design Considerations

### Module Structure

```text
spec-driven-workflow/
├── slash_commands/          # New module
│   ├── __init__.py
│   ├── config.py           # AgentConfig, SUPPORTED_AGENTS
│   ├── generators.py       # CommandGenerator base + subclasses
│   ├── writer.py           # SlashCommandWriter
│   ├── cli.py              # Typer CLI interface
│   └── detection.py        # Auto-detection logic
├── tests/
│   ├── test_config.py      # Test data models
│   ├── test_generators.py  # Test format generation
│   ├── test_writer.py      # Test writer orchestration
│   ├── test_cli.py         # Test CLI parsing
│   └── fixtures/           # Sample prompts for testing
│       └── sample_prompt.md
└── docs/
    └── slash-command-generator.md  # Comprehensive usage guide
```

### Extensibility Pattern

The `CommandGenerator` abstract base class provides a simple extension point:

```python
from abc import ABC, abstractmethod

class CommandGenerator(ABC):
    @abstractmethod
    def generate(self, prompt: MarkdownPrompt, command_prefix: str = "") -> str:
        """Generate command file content from a MarkdownPrompt"""
        pass
```

New formats can be added by:

1. Subclassing `CommandGenerator`
2. Implementing the `generate()` method
3. Registering in `get_generator()` factory function

### Auto-Detection Logic

The detection module will check for directory existence:

```python
def detect_agents(target_dir: Path) -> list[AgentConfig]:
    """Return list of agents whose config directories exist in target"""
    detected = []
    for agent in SUPPORTED_AGENTS:
        config_path = target_dir / agent.command_dir.split('/')[0]  # e.g., .claude
        if config_path.exists():
            detected.append(agent)
    return detected
```

### Interactive Selection Flow

Using Typer's prompt capabilities:

1. Auto-detect configured agents
2. If none detected, use `typer.confirm()` to ask if user wants to generate for all agents
3. If some detected, present options for each agent using individual `typer.confirm()` calls with detected agents defaulting to `True` (opt-out model)
4. Alternative: Use `questionary` library for multi-select checkbox interface if richer interaction is needed
5. Proceed with selected agents

**Best Practice**: Prefer CLI options with `prompt=True` over direct interactive prompts when possible, as this allows non-interactive usage (e.g., `--agents claude-code cursor` for scripts).

### Agent-Specific Metadata Override Format

Prompts can specify per-agent customizations in frontmatter:

```yaml
---
name: generate-spec
description: Generate a specification document
agent_overrides:
  gemini-cli:
    description: "Create a detailed spec (Gemini optimized)"
  cursor:
    description: "Generate spec with Cursor integration"
---
```

Generators check for overrides and merge with base metadata.

## Technical Considerations

### Reuse Existing Infrastructure

- Leverage `mcp_server/prompt_utils.py` for prompt loading (no duplication)
- Use existing `MarkdownPrompt` dataclass
- Follow established code style (Ruff formatting, type hints)

### Dependencies

New dependencies required:

- **Typer**: For CLI framework with built-in Rich integration
- **Rich**: (optional but recommended) Already available in the ecosystem, provides enhanced output formatting
- **Pytest**: Already in dev dependencies, used for TDD workflow
- **Questionary** (optional): For advanced multi-select checkboxes if simple `typer.confirm()` loops are insufficient

**Note**: Typer automatically uses Rich for enhanced output if it's installed, requiring no additional configuration.

### CLI Implementation Pattern (Typer 2025 Best Practices)

Use the modern `Annotated` syntax for type clarity and maintainability:

```python
from typing import Annotated, Optional
from pathlib import Path
import typer

app = typer.Typer()

@app.command()
def generate(
    target_dir: Annotated[
        Path,
        typer.Option(help="Target project directory")
    ] = Path.cwd(),
    agents: Annotated[
        Optional[list[str]],
        typer.Option(help="Specific agents to generate for")
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Preview without writing files")
    ] = False,
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Skip confirmation prompts")
    ] = False,
):
    """Generate slash commands for AI coding tools."""
    # Implementation here
    pass
```

**Key benefits of `Annotated` syntax**:

- Type information and metadata in one place
- Better IDE support and type checking
- More maintainable than older `typer.Option()` as default value pattern
- Recommended by Typer documentation as of 2025

### TDD Workflow

Per requirement #7, development must follow strict TDD:

1. Write failing test for smallest unit of functionality
2. Implement minimal code to make test pass
3. Refactor while keeping tests green
4. Commit with descriptive message
5. Repeat

**Pytest Best Practices for TDD (2025)**:

- Use `tmp_path` fixture (built-in) for temporary file operations instead of custom solutions
- Organize shared fixtures in `tests/conftest.py` for reusability across test modules
- Use fixture parametrization to test multiple configurations without code duplication
- Choose appropriate fixture scopes:
  - `function` (default) for test isolation
  - `module` or `session` for expensive setup like loading sample prompts
- Leverage yield fixtures for clean setup/teardown patterns

Example TDD cycle for `MarkdownCommandGenerator`:

- Test: `test_markdown_generator_creates_valid_frontmatter()` (FAIL)
- Implement: Basic frontmatter generation (PASS)
- Test: `test_markdown_generator_handles_arguments_placeholder()` (FAIL)
- Implement: Argument substitution logic (PASS)
- Refactor: Extract helper methods, improve readability (PASS)

### File Writing Safety

All file operations use `pathlib.Path` for safety following modern best practices:

**Directory creation** (2025 best practice):

```python
file_path.parent.mkdir(parents=True, exist_ok=True)
```

- `parents=True`: Creates intermediate directories (equivalent to `mkdir -p`)
- `exist_ok=True`: No error if directory already exists

**File writing** (2025 best practice):

```python
file_path.write_text(content, encoding="utf-8")
```

- Always specify `encoding="utf-8"` explicitly for cross-platform compatibility
- `write_text()` handles file opening, writing, and closing automatically
- Creates file if it doesn't exist, overwrites if it does

**Backup creation**:

```python
from datetime import datetime
import shutil

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_path = file_path.with_suffix(f"{file_path.suffix}.{timestamp}.bak")
shutil.copy2(file_path, backup_path)  # Preserves metadata
```

## Success Metrics

1. **Test Coverage**: 80% code coverage for core modules (config, generators, writer)
2. **TDD Compliance**: All code has corresponding tests written *before* implementation
3. **Agent Support**: All 14 AI tools successfully generate working slash commands
4. **User Adoption**: At least 3 SDD users successfully generate commands in their projects within 2 weeks of release
5. **Documentation Clarity**: Zero confusion-related issues opened about basic usage (how to run, what flags to use)
6. **Generation Speed**: Generating commands for all 14 agents completes in under 2 seconds on standard hardware
7. **Error Rate**: Zero file corruption or permission errors during normal operation in manual testing

## Resolved Design Decisions

These questions have been resolved and should be implemented as specified:

1. **Prompt Argument Handling**: Implement placeholder support now (`$ARGUMENTS`, `{{args}}`), defer complex argument interpolation to future iteration.

2. **Backup Retention**: No automatic cleanup in v1. Document that users should periodically clean `.bak` files.

3. **Agent Priority/Ordering**: Detected agents will be presented in alphabetical order for predictability.

4. **Interactive Mode Defaults**: All detected agents will be pre-selected (opt-out model) since detection implies user has those tools configured.

5. **Error Handling Philosophy**: Continue with warnings when a single agent fails, report all failures at end. This allows partial success in degraded scenarios.

## Filename

This specification will be saved as:

```bash
/tasks/0003-spec-slash-command-generator.md
```

## Addendum: Detection Default Location Oversight

**Issue**: Specification oversight regarding default detection location

### Problem Statement

The original specification (FR6, FR18) implicitly assumed that slash commands would be generated per-project (in the current working directory). However, this conflicts with the intended use case where slash commands should be installed globally at the user's home directory level for universal access across all AI tools.

### Root Cause

FR6 states: "The system must auto-detect configured AI tools by checking for the presence of their configuration directories in the target project (e.g., `.claude/`, `.cursor/`, `.windsurf/`)."

FR18 states: "The CLI must default to generating commands in the current working directory."

This per-project approach makes sense for project-specific configurations but not for global slash commands that should be available across all projects.

### Intended Behavior

Slash commands should be installed globally by default at the user's home directory level because:

1. **Universal Access**: AI coding tools typically read slash commands from the user's home directory (e.g., `~/.claude/commands/`, `~/.gemini/commands/`)
2. **Consistency**: Users expect slash commands to work across all their projects, not just the current one
3. **Configuration Management**: Agent configurations (`.claude/`, `.gemini/`, etc.) are typically stored at the user level, not per-project

### Corrected Behavior

The CLI should default to detecting agents in the user's home directory (`~` or `$HOME`), not the current working directory. This allows:

- Auto-detection of agents configured globally
- Generation of slash commands in the correct location for universal access
- Optional override via `--detection-path` flag for project-specific use cases

### Implementation Impact

This oversight requires changing the default detection path from `Path.cwd()` to `Path.home()` while maintaining backward compatibility through CLI flags.
