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

| Agent | Display Name | Format | Extension | Reference |
|-------|--------------|--------|-----------|-----------|
| `amazon-q-developer` | Amazon Q Developer | Markdown | `.md` | [Home](https://aws.amazon.com/q/developer/) · [Docs](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html) |
| `amp` | Amp | Markdown | `.md` | [Home](https://ampcode.com/) · [Docs](https://ampcode.com/manual) |
| `auggie-cli` | Auggie CLI | Markdown | `.md` | [Home](https://www.augmentcode.com/product/CLI) · [Docs](https://docs.augmentcode.com/cli/overview) |
| `claude-code` | Claude Code | Markdown | `.md` | [Home](https://docs.claude.com/) · [Docs](https://docs.claude.com/en/docs/claude-code/overview) |
| `codebuddy-cli` | CodeBuddy CLI | Markdown | `.md` | [Home](https://www.codebuddy.ai/) · [Docs](https://docs.codebuddy.com/) |
| `codex-cli` | Codex CLI | Markdown | `.md` | [Home](https://developers.openai.com/codex) · [Docs](https://developers.openai.com/codex/cli/) |
| `cursor` | Cursor | Markdown | `.md` | [Home](https://cursor.com/) · [Docs](https://cursor.com/docs) |
| `gemini-cli` | Gemini CLI | TOML | `.toml` | [Home](https://github.com/google-gemini/gemini-cli) · [Docs](https://geminicli.com/docs/) |
| `github-copilot` | GitHub Copilot | Markdown | `.md` | [Home](https://github.com/features/copilot/cli) · [Docs](https://docs.github.com/en/copilot) |
| `kilo-code` | Kilo Code | Markdown | `.md` | [Home](https://kilocode.ai/) · [Docs](https://kilocode.ai/docs/) |
| `opencode` | opencode | Markdown | `.md` | [Home](https://opencode.ai/) · [Docs](https://opencode.ai/docs/) |
| `qwen-code` | Qwen Code | TOML | `.toml` | [Home](https://github.com/QwenLM/qwen-code) · [Docs](https://qwenlm.github.io/qwen-code-docs/) |
| `roo-code` | Roo Code | Markdown | `.md` | [Home](https://github.com/RooCodeInc/Roo-Code) · [Docs](https://docs.roocode.com/) |
| `windsurf` | Windsurf | Markdown | `.md` | [Home](https://windsurf.com/editor) · [Docs](https://docs.windsurf.com/) |

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

TOML-based agents (Gemini CLI, Qwen Code) use TOML syntax:

```toml
[command]
name = "command-name"
description = "Command description"
tags = ["tag1", "tag2"]
enabled = true

[command.arguments]
required = { "arg1" = "Argument description" }
optional = {}

[command.body]
text = """
# Command Name

Command body content.

{{args}}
"""

[command.meta]
category = "example"
agent = "gemini-cli"
agent_display_name = "Gemini CLI"
command_dir = ".gemini/commands"
command_format = "toml"
command_file_extension = ".toml"
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
.claude/commands/        # Claude Code
.cursorrules/commands/  # Cursor
.gemini/commands/       # Gemini CLI
.github/copilot/commands/  # GitHub Copilot
.qwen/commands/        # Qwen Code
.windsurfrules/commands/  # Windurf
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
