# Slash Command Generator

The Slash Command Generator automates the creation of slash command files for AI code assistants like Claude Code, Cursor, Windsurf, and others. It generates command files from markdown prompts, supporting multiple agents and formats.

## Overview

The generator reads markdown prompts from the `prompts/` directory and produces command files in the appropriate format for each configured AI assistant. It supports:

- **Multiple agents**: 14 supported AI assistants with different command formats
- **Auto-detection**: Automatically detects configured agents in your workspace
- **Dry run mode**: Preview changes without writing files
- **Safe overwrite handling**: Prompts before overwriting existing files with backup support

## Installation

The CLI is installed as part of the project dependencies:

```bash
uv sync
```

## Usage

### Running Commands

After installation, use `uv run` to execute the command:

```bash
uv run sdd-generate-commands [OPTIONS]
```

### Basic Usage

Generate commands for all auto-detected agents:

```bash
uv run sdd-generate-commands
```

### Agent Selection

Generate commands for specific agents:

```bash
uv run sdd-generate-commands --agents claude-code --agents cursor
```

### Dry Run

Preview changes without writing files:

```bash
uv run sdd-generate-commands --dry-run
```

### List Supported Agents

View all available agents:

```bash
uv run sdd-generate-commands --list-agents
```

### Custom Prompts Directory

Specify a custom prompts directory:

```bash
uv run sdd-generate-commands --prompts-dir ./my-prompts
```

### Overwrite Handling

When existing command files are detected, the generator will prompt you for action:

- **Cancel**: Abort the operation (no files modified)
- **Overwrite**: Replace the existing file
- **Backup**: Create a timestamped backup before overwriting
- **Overwrite All**: Apply the overwrite decision to all remaining files

To skip prompts and auto-overwrite:

```bash
uv run sdd-generate-commands --yes
```

## Supported Agents

The following agents are supported:

| Agent | Display Name | Format | Extension |
|-------|--------------|--------|-----------|
| `claude-code` | Claude Code | Markdown | `.md` |
| `claude-desktop` | Claude Desktop | Markdown | `.md` |
| `cursor` | Cursor | Markdown | `.md` |
| `cody` | Cody | Markdown | `.md` |
| `continue` | Continue | Markdown | `.md` |
| `bloop` | Bloop | Markdown | `.md` |
| `cursor-context` | Cursor Context | Markdown | `.md` |
| `gemini-cli` | Gemini CLI | TOML | `.toml` |
| `gemini-app` | Gemini App | TOML | `.toml` |
| `gemini-chat` | Gemini Chat | TOML | `.toml` |
| `gemini-emacs` | Gemini Emacs | TOML | `.toml` |
| `gemini-neovim` | Gemini Neovim | TOML | `.toml` |
| `gemini-jupyter` | Gemini Jupyter | TOML | `.toml` |
| `gemini-fleet` | Gemini Fleet | TOML | `.toml` |

## Command File Formats

### Markdown Format

Markdown-based agents (Claude Code, Cursor, etc.) use frontmatter with a body:

```markdown
---
name: command-name
description: Command description
tags:
  - tag1
  - tag2
arguments:
  - name: arg1
    description: Argument description
    required: true
enabled: true
---

# Command Name

Command body content.

$ARGUMENTS
```

### TOML Format

TOML-based agents (Gemini variants) use TOML syntax:

```toml
name = "command-name"
description = "Command description"
tags = ["tag1", "tag2"]

[[arguments]]
name = "arg1"
description = "Argument description"
required = true

enabled = true

[body]
content = """
# Command Name

Command body content.

{{args}}
"""
```

## Prompt Structure

Prompts are markdown files with YAML frontmatter. Key fields:

- **name**: Unique command identifier
- **description**: Human-readable description
- **tags**: List of tags for categorization
- **arguments**: List of command arguments
- **enabled**: Whether the command is active (default: true)
- **agent_overrides**: Agent-specific customization
- **body**: Markdown content for the command

See `prompts/` directory for examples.

## Directory Structure

Generated files are placed in agent-specific directories:

```text
.claude/commands/        # Claude Code, Claude Desktop
.cursor/commands/        # Cursor
.cody/commands/          # Cody
.continue/commands/      # Continue
.bloop/commands/        # Bloop
.gemini/commands/       # Gemini variants
```

## Examples

### Generate for Detected Agents

```bash
# Auto-detect agents
uv run sdd-generate-commands

# Output:
# Detected agents: claude-code, cursor
#
# Generation complete:
#   Prompts loaded: 3
#   Files written: 6
```

### Preview Changes

```bash
# See what would be generated
uv run sdd-generate-commands --dry-run

# Output:
# DRY RUN complete:
#   Prompts loaded: 3
#   Files would be written: 6
```

### Safe Overwrite with Backup

```bash
# Prompt for overwrite action
uv run sdd-generate-commands

# When prompted:
# > File exists: .claude/commands/my-command.md
# > [c]ancel, [o]verwrite, [b]ackup, [a]ll overwrite: b
#
# Output:
# Generation complete:
#   Prompts loaded: 3
#   Files written: 6
#   Backups created: 2
#     - .claude/commands/my-command.md.20251022_180812.bak
#     - .cursor/commands/my-command.md.20251022_180812.bak
```

## Configuration

### Base Path

Specify a custom base directory for output:

```bash
uv run sdd-generate-commands --base-path /path/to/project
```

### Environment Variables

Configuration can be set via environment variables:

- `SDD_PROMPTS_DIR`: Default prompts directory (default: `prompts`)
- `SDD_BASE_PATH`: Default base path for output files

## Troubleshooting

### No Agents Detected

If no agents are detected, manually specify agents:

```bash
uv run sdd-generate-commands --agents claude-code
```

### Existing Files Not Prompting

The generator only prompts when files exist and `--yes` is not set. To prompt for overwrite:

```bash
# Don't use --yes flag
uv run sdd-generate-commands
```

### Backup Files Not Created

Ensure you select "backup" when prompted, or use `--yes` with a custom overwrite action:

```bash
# Backups are created automatically when selecting 'backup' option
```

## Integration with SDD Workflow

The Slash Command Generator complements the Spec-Driven Development workflow:

1. **Generate prompts** using the SDD workflow
2. **Place prompts** in the `prompts/` directory
3. **Generate commands** using `uv run sdd-generate-commands`
4. **Test commands** in your AI assistant
5. **Iterate** based on feedback

## See Also

- [README.md](../README.md) - Project overview
- [operations.md](./operations.md) - MCP server operations
- [mcp-prompt-support.md](./mcp-prompt-support.md) - MCP prompt support details
