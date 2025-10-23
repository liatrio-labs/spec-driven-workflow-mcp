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

Generate commands for all auto-detected agents in your home directory:

```bash
uv run sdd-generate-commands
```

**Note**: By default, the generator:

- Detects agents in your home directory (`~`)
- Generates command files in your home directory
- Use `--detection-path` to search in a different directory
- Use `--target-path` to generate files in a different location

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

### Detection Path

Specify a custom directory to search for agents:

```bash
uv run sdd-generate-commands --detection-path /path/to/project
```

**Note**: By default, the generator searches for agents in your home directory. Use `--detection-path` to search in a different location (e.g., current directory for project-specific detection).

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

#### Backup File Management

Backup files are created with the format `filename.ext.YYYYMMDD-HHMMSS.bak` (e.g., `manage-tasks.md.20250122-143059.bak`).

**Important**: Backup files are **not automatically cleaned up**. Periodically review and remove old backup files to keep your workspace clean:

```bash
# Find all backup files
find . -name "*.bak" -type f

# Remove backup files older than 30 days
find . -name "*.bak" -type f -mtime +30 -delete
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
.cursor/commands/  # Cursor
.gemini/commands/       # Gemini CLI
.github/copilot/commands/  # GitHub Copilot
.qwen/commands/        # Qwen Code
.windsurfrules/commands/  # Windurf
```

## Examples

### List Supported Agents

```bash
uv run sdd-generate-commands --list-agents
```

**Output**:

```text
Supported agents:
  amazon-q-developer   - Amazon Q Developer
  amp                  - Amp
  auggie-cli           - Auggie CLI
  claude-code          - Claude Code
  cursor               - Cursor
  gemini-cli           - Gemini CLI
  github-copilot       - GitHub Copilot
  kilo-code            - Kilo Code
  opencode             - opencode
  qwen-code            - Qwen Code
  roo-code             - Roo Code
  windsurf             - Windsurf
```

### Generate for Detected Agents

```bash
# Auto-detect agents
uv run sdd-generate-commands --yes
```

**Output**:

```text
Detected agents: claude-code, cursor

Generation complete:
  Prompts loaded: 3
  Files written: 6

Files:
  - .claude/commands/manage-tasks.md
    Agent: Claude Code (claude-code)
  - .claude/commands/generate-spec.md
    Agent: Claude Code (claude-code)
  - .claude/commands/generate-task-list-from-spec.md
    Agent: Claude Code (claude-code)
  - .cursor/commands/manage-tasks.md
    Agent: Cursor (cursor)
  - .cursor/commands/generate-spec.md
    Agent: Cursor (cursor)
  - .cursor/commands/generate-task-list-from-spec.md
    Agent: Cursor (cursor)
```

### Preview Changes

```bash
# See what would be generated
uv run sdd-generate-commands --dry-run --yes
```

**Output**:

```text
Detected agents: claude-code, cursor

DRY RUN complete:
  Prompts loaded: 3
  Files would be written: 6

Files:
  - .claude/commands/manage-tasks.md
    Agent: Claude Code (claude-code)
  - .claude/commands/generate-spec.md
    Agent: Claude Code (claude-code)
  - .claude/commands/generate-task-list-from-spec.md
    Agent: Claude Code (claude-code)
  - .cursor/commands/manage-tasks.md
    Agent: Cursor (cursor)
  - .cursor/commands/generate-spec.md
    Agent: Cursor (cursor)
  - .cursor/commands/generate-task-list-from-spec.md
    Agent: Cursor (cursor)
```

### Safe Overwrite with Backup

```bash
# Prompt for overwrite action (without --yes)
uv run sdd-generate-commands
```

**Interactive prompt**:

```text
File already exists: .claude/commands/manage-tasks.md
What would you like to do?
  > Cancel
    Overwrite this file
    Create backup and overwrite
    Overwrite all existing files
```

**Output after selecting "Create backup and overwrite"**:

```text
Generation complete:
  Prompts loaded: 3
  Files written: 6
  Backups created: 2
    - .claude/commands/manage-tasks.md.20250122-143059.bak
    - .cursor/commands/manage-tasks.md.20250122-143059.bak

Files:
  - .claude/commands/manage-tasks.md
    Agent: Claude Code (claude-code)
  - .claude/commands/generate-spec.md
    Agent: Claude Code (claude-code)
  - ...
```

### Generate for Specific Agents

```bash
uv run sdd-generate-commands --agents claude-code --agents gemini-cli --yes
```

**Output**:

```text
Selected agents: claude-code, gemini-cli

Generation complete:
  Prompts loaded: 3
  Files written: 6

Files:
  - .claude/commands/manage-tasks.md
    Agent: Claude Code (claude-code)
  - .claude/commands/generate-spec.md
    Agent: Claude Code (claude-code)
  - .claude/commands/generate-task-list-from-spec.md
    Agent: Claude Code (claude-code)
  - .gemini/commands/manage-tasks.toml
    Agent: Gemini CLI (gemini-cli)
  - .gemini/commands/generate-spec.toml
    Agent: Gemini CLI (gemini-cli)
  - .gemini/commands/generate-task-list-from-spec.toml
    Agent: Gemini CLI (gemini-cli)
```

## Configuration

### Target Path

Specify a custom target directory for output:

```bash
uv run sdd-generate-commands --target-path /path/to/project
```

**Note**: By default, commands are generated in your home directory. Use `--target-path` to specify a different location.

### Environment Variables

Configuration can be set via environment variables:

- `SDD_PROMPTS_DIR`: Default prompts directory (default: `prompts`)
- `SDD_BASE_PATH`: Default base path for output files

## Troubleshooting

### No Agents Detected

**Error**: `Error: No agents detected.`

**Cause**: No agent directories (e.g., `.claude`, `.cursor`, `.gemini`) were found in the detection path.

**Solutions**:

1. **Create agent directories**: Ensure at least one agent directory exists in your workspace:

   ```bash
   mkdir -p .claude
   ```

2. **Specify agents manually**: Use `--agents` to explicitly select agents:

   ```bash
   uv run sdd-generate-commands --agents claude-code
   ```

3. **Use detection path**: Specify a different directory to search:

   ```bash
   uv run sdd-generate-commands --detection-path /path/to/home
   ```

4. **List supported agents**: See all available agents:

   ```bash
   uv run sdd-generate-commands --list-agents
   ```

### Invalid Agent Key

**Error**: `Error: Invalid agent key: <key>`

**Cause**: The specified agent key doesn't match any supported agent.

**Solutions**:

1. **Check agent keys**: Use `--list-agents` to see all valid agent keys:

   ```bash
   uv run sdd-generate-commands --list-agents
   ```

2. **Verify spelling**: Ensure agent keys are spelled correctly (e.g., `claude-code` not `claude_code`)

3. **Check documentation**: See the [Supported Agents](#supported-agents) section above for valid keys

### Permission Denied

**Error**: `Error: Permission denied: <path>`

**Cause**: Insufficient permissions to write to the output directory.

**Solutions**:

1. **Check permissions**: Verify write access to the output directory:

   ```bash
   ls -la .claude/
   ```

2. **Fix permissions**: Grant write access to the directory:

   ```bash
   chmod u+w .claude/
   ```

3. **Use different base path**: Specify a writable directory:

   ```bash
   uv run sdd-generate-commands --target-path /tmp/test-output
   ```

4. **Run with elevated permissions**: If appropriate, use `sudo`:

   ```bash
   sudo uv run sdd-generate-commands
   ```

### I/O Error

**Error**: `Error: I/O error: <details>`

**Cause**: File system or disk-related issues.

**Solutions**:

1. **Check disk space**: Ensure sufficient disk space is available:

   ```bash
   df -h .
   ```

2. **Verify path exists**: Ensure the output directory exists:

   ```bash
   mkdir -p .claude/commands
   ```

3. **Check for file locks**: Ensure no other process is accessing the files

4. **Try different location**: Use a different base path:

   ```bash
   uv run sdd-generate-commands --target-path /tmp/test-output
   ```

### Prompts Directory Not Found

**Error**: `Error: Prompts directory does not exist: <path>`

**Cause**: The specified prompts directory doesn't exist or is inaccessible.

**Solutions**:

1. **Verify prompts directory**: Check that the directory exists:

   ```bash
   ls -la prompts/
   ```

2. **Specify correct path**: Use `--prompts-dir` to point to the correct location:

   ```bash
   uv run sdd-generate-commands --prompts-dir /path/to/prompts
   ```

3. **Create prompts directory**: If missing, create it:

   ```bash
   mkdir -p prompts
   ```

### User Cancellation

**Error**: `Cancelled: Operation cancelled by user.`

**Exit Code**: 1

**Cause**: User cancelled the operation (e.g., Ctrl+C or selected "Cancel" in prompt).

**Note**: This is not an error but a normal cancellation. Simply re-run the command to try again.

### Format Errors

**Issue**: Generated files don't match expected format

**Cause**: Prompt structure or metadata doesn't match agent requirements.

**Solutions**:

1. **Check prompt format**: Ensure prompts follow the correct structure (see [Prompt Structure](#prompt-structure))

2. **Verify agent-specific overrides**: Check that `agent_overrides` in prompt metadata match agent requirements

3. **Review generated files**: Inspect the generated files to identify format issues:

   ```bash
   cat .claude/commands/command-name.md
   ```

4. **Test with dry-run**: Use `--dry-run` to preview output before writing

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

### Exit Codes

The CLI uses consistent exit codes:

- **0**: Success
- **1**: User cancellation (e.g., Ctrl+C, cancelled prompts)
- **2**: Validation error (invalid agent key, no agents detected)
- **3**: I/O error (permission denied, missing directory, disk full)

Use these codes to script error handling:

```bash
uv run sdd-generate-commands && echo "Success" || echo "Failed with exit code $?"
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
