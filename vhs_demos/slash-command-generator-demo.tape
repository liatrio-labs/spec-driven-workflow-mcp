# Output slash-command-generator-demo.gif
# Output slash-command-generator-demo.webm
# Output frames/
Output ./vhs_demos/output/slash-command-generator-demo.mp4

# Comprehensive demo of the Slash Command Generator
Set FontSize 14
Set Width 1000
# Set Height 563
Set Padding 30
Set TypingSpeed 40ms
Set BorderRadius 25
Set Margin 15
Set MarginFill "#24AE1D"
Set Theme {
  "name": "Liatrio Dark",
  "black": "#111111",
  "red": "#FF5100",
  "green": "#24AE1D",
  "yellow": "#89DF00",
  "blue": "#007DAA",
  "magenta": "#FFAA00",
  "cyan": "#00C1DB",
  "white": "#eeeeee",

  "brightBlack": "#3a3a3a",
  "brightRed": "#FF5100",
  "brightGreen": "#24AE1D",
  "brightYellow": "#89DF00",
  "brightBlue": "#007DAA",
  "brightMagenta": "#FFAA00",
  "brightCyan": "#00C1DB",
  "brightWhite": "#ffffff",

  "background": "#111111",
  "foreground": "#eeeeee",
  "selection": "#3a3a3a",
  "cursor": "#89DF00"
}

# Introduction
Type "# 🎯 Spec-driven Workflow: Slash Command Generator Demo 🎯" Enter 2 Sleep 250ms # Short Wait
Type "# Generate native slash commands for the Spec-driven Workflow in all of your AI assistants!" Enter 2 Sleep 250ms # Short Wait

# Show help
Type@4ms "uv run sdd-commands generate --help"
Enter 2
Wait
Sleep 3000ms # Extra Long Wait

# Clear screen
Ctrl+L

# Show the prompts directory structure
Type "# The following prompts are available:" Enter
Type@4ms "ls -1 prompts/" Enter 2
Wait
Sleep 1000ms # Medium Wait

# Show example prompt structure
Type "# Here is an example of the prompt structure:" Enter
Type@4ms "head -n 20 prompts/manage-tasks.md"
Enter 2
Wait
Sleep 3000ms # Extra Long Wait

# Clear screen
Ctrl+L

# List supported agents
Type "# You can view the list of supported AI tools:" Enter
Type@4ms "uv run sdd-commands generate --list-agents"
Enter 2
Wait
Sleep 3000ms # Extra Long Wait

# Dry run to preview what would be generated
Type "# Let's do a dry run to preview what would be generated for an agent like Claude Code:" Enter
Type@4ms "uv run sdd-commands generate --dry-run" Enter
Wait+Screen /Select agents/ Sleep 250ms # Short Wait
Down Space Sleep 400ms # Short Wait
Down Space Sleep 400ms # Short Wait
Down Space Sleep 400ms # Short Wait
Down Space Sleep 400ms # Short Wait
Down Space Sleep 400ms # Short Wait
Enter 2
Sleep 3000ms # Extra Long Wait

Type "# You can also specify an agent via the --agent flag:" Enter
Type@4ms "uv run sdd-commands generate --agent claude-code --dry-run     "
Ctrl+C
Sleep 3000ms # Extra Long Wait

# Clear screen
Ctrl+L

# Show there is nothing in the commands directory
Type "# Before generating, let's confirm there are no custom commands present for Claude Code:"
Sleep 250ms # Short Wait
Enter
Type@4ms "ls -1 ~/.claude/commands/"
Enter 2
Wait
Sleep 1000ms # Medium Wait

# Generate commands for detected agents
Type "# Now let's generate the commands for Claude Code:"
Sleep 250ms # Short Wait
Enter
Type@4ms "uv run sdd-commands generate --agent claude-code"
Sleep 250ms # Short Wait
Enter 2
Wait
Sleep 3000ms # Extra Long Wait

# Show generated files
Type "# And verify the generated files:"
Sleep 250ms # Short Wait
Enter
Type@4ms "ls -1 ~/.claude/commands/"
Sleep 250ms # Short Wait
Enter 2
Wait
Sleep 3000ms # Extra Long Wait

# Clear screen
Ctrl+L

# Show example generated command
Type "# Let's inspect one of the generated commands:"
Sleep 250ms # Short Wait
Enter
Type@4ms "head -n 27 ~/.claude/commands/manage-tasks.md"
Sleep 1000ms # Medium Wait
Enter 2
Wait
Sleep 3000ms # Extra Long Wait

# Clear screen
Ctrl+L

# Showcase automatic backup
Type "# The app detects existing commands and can create backups automatically:"
Sleep 250ms # Short Wait
Enter
Type@4ms "uv run sdd-commands generate --agent claude-code"
Sleep 250ms # Short Wait
Enter
Wait+Screen /File already exists/ Sleep 250ms # Short Wait
Down 1 Sleep 250ms # Short Wait
Down 1 Sleep 250ms # Short Wait
Enter
Wait+Screen /File already exists/ Sleep 250ms # Short Wait
Down 1 Sleep 250ms # Short Wait
Down 1 Sleep 250ms # Short Wait
Enter
Wait+Screen /File already exists/ Sleep 250ms # Short Wait
Down 1 Sleep 250ms # Short Wait
Down 1 Sleep 250ms # Short Wait
Enter
Wait
Enter 2
Sleep 3000ms # Extra Long Wait

# Clear screen
Ctrl+L

# Show backup files
Type "# Quick verification that the backup files exist:"
Sleep 250ms # Short Wait
Enter
Type@4ms "ls -1 ~/.claude/commands/"
Sleep 250ms # Short Wait
Enter 2
Wait
Sleep 3000ms # Extra Long Wait

# Clear screen
Ctrl+L

# Show version and timestamp metadata
Type "# Note the version and timestamp metadata in every prompt:"
Sleep 250ms # Short Wait
Enter
Type@4ms "head -n 20 ~/.claude/commands/manage-tasks.md"
Sleep 250ms # Short Wait
Enter 2
Wait
Sleep 1000ms # Medium Wait
Type "# The version and timestamp are automatically added by the tool to help you track"
Enter
Type "# changes over time."
Sleep 250ms # Short Wait
Enter
Sleep 3000ms # Extra Long Wait

# Clear screen
Ctrl+L

# Show cleanup functionality
Type "# The tool can also clean up any files it generated:"
Sleep 250ms # Short Wait
Enter
Type@4ms "uv run sdd-commands cleanup --agent claude-code --dry-run"
Sleep 250ms # Short Wait
Enter
Wait+Screen /.*/
Sleep 2000ms # Long Wait
Type "N"
Sleep 250ms # Short Wait
Enter
Sleep 3000ms # Extra Long Wait

# Clear screen
Ctrl+L

# Show advanced options
Type "# --- Advanced usage examples ---"
Sleep 250ms # Short Wait
Enter 2
Type "# 💡 Generate for specific target path"
Sleep 250ms # Short Wait
Enter 2
Type@4ms "uv run sdd-commands generate --target-path ./<your-current-project>     "
Ctrl+C
Enter 2
Type "# This is useful if you want to generate commands for a specific project"
Sleep 250ms # Short Wait
Enter 2
Sleep 2000ms # Long Wait
Type "# 💡 Use custom prompts directory"
Sleep 250ms # Short Wait
Enter 2
Type@4ms "uv run sdd-commands generate --prompts-dir ./<your-custom-prompts>     "
Ctrl+C
Enter 2
Type "# Use this to create slash commands for a custom set of prompts"
Sleep 250ms # Short Wait
Enter 2
Sleep 2000ms # Long Wait
Type "# 💡 Detect agents in different path"
Sleep 250ms # Short Wait
Enter 2
Type@4ms "uv run sdd-commands generate --detection-path ./<your-custom-project>     "
Ctrl+C
Enter 2
Type "# This will generate commands for the agents detected in the specified path"
Sleep 250ms # Short Wait
Enter 2
Sleep 2000ms # Long Wait

# Clear screen
Ctrl+L

# Final summary
Type "# 🎉 Spec-driven Workflow: Slash Command Generator Recap 🎉"
Sleep 250ms # Short Wait
Enter 3
Type@15ms "# ✅ Auto-detects AI assistants in your workspace"
Enter
Sleep 250ms # Short Wait
Type@15ms "# ✅ Supports major AI assistants"
Enter
Sleep 250ms # Short Wait
Type@15ms "# ✅ Converts markdown prompts to native command formats"
Enter
Sleep 250ms # Short Wait
Type@15ms "# ✅ Safe overwrite handling with backups"
Enter
Sleep 250ms # Short Wait
Type@15ms "# ✅ Dry-run mode for preview"
Enter
Sleep 250ms # Short Wait
Type@15ms "# ✅ Interactive agent selection"
Enter
Type@15ms "# ✅ Cleanup command for easy removal"
Enter
Enter 5
Sleep 250ms # Short Wait
Type "# Ready to supercharge your AI-native workflow!"
Sleep 1000ms # Medium Wait
Enter 2
Type "# Thanks for watching!"
Sleep 250ms # Short Wait
Enter 2
Type "# If you found this demo helpful, please give the tool a star on GitHub:"
Enter
Type "# https://github.com/liatrio-labs/spec-driven-workflow"
Sleep 1000ms # Medium Wait
