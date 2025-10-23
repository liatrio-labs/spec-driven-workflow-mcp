# MCP Prompt Support

This guide tracks how well popular IDEs, CLIs, and agent shells load the Spec Driven Development (SDD) prompts exposed by the MCP server. Use it to choose the smoothest environment, understand current limitations, and contribute new findings.

## Support Matrix

| Tool | Version<br />Tested | Loads MCP? | Prompt Actions | Experience | Workarounds / Notes |
| --- | --- | --- | --- | --- | --- |
| Claude Code CLI | TBD | Yes | Slash commands generated automatically | Ideal | Prompts appear as native slash commands. |
| Claude Code Desktop | TBD | Yes | TBD | Ideal | Loads successfully; verifying how quickly prompts become slash commands. |
| Claude Code IDE (JetBrains) | TBD | Yes | TBD | Ideal | Successful load; documenting slash-command behavior. |
| Cursor | TBD | Yes | Implicit trigger (no slash commands) | Ideal | Natural-language requests ("generate a spec") invoke the prompts. |
| Gemini CLI | TBD | Yes | Slash commands generated automatically | Ideal | Prompts appear as native slash commands. |
| OpenCode | TBD | Yes | Implicit trigger (no slash commands) | Ideal | Prompts are invoked through natural language requests. |
| Windsurf | TBD | Yes | No | Not good | MCP loads but returns `Error: no tools returned.` Adding a dummy tool unblocks basic use. |
| VS Code | TBD | Yes | Slash commands generated, but not executed | Not good | Prompts appear as commands but are inserted verbatim into chat; AI ignores them. |
| Codex CLI | TBD | Yes | No | Non-existent | Prompts not recognized; manual copy/paste required. |
| Codex IDE Plugin | TBD | Yes | No | Non-existent | Same as CLI—no prompt awareness. |
| Goose | TBD | Yes | TBD | TBD | Loads successfully; behavior still being evaluated. |
| Crush | TBD | TBD | TBD | TBD | Awaiting confirmation. |
| Q Developer CLI | TBD | TBD | TBD | TBD | Awaiting confirmation. |
| Q Developer IDE Plugin | TBD | TBD | TBD | TBD | Awaiting confirmation. |

## Interpretation

- **Ideal** environments either supply native slash commands or automatically invoke the correct prompt flows from natural language requests.
- **Not good** means the MCP connection succeeds but prompt usage is clumsy or broken without manual intervention.
- **Non-existent** indicates the tool ignores MCP prompts entirely today.
- **TBD** rows invite contributors to validate behavior and update this document.

## Field Notes & Tips

- Tools that surface the prompts as first-class slash commands (Claude Code CLI/Desktop, Gemini CLI) provide the fastest path to running the SDD workflow without touching raw Markdown.
- When slash commands are absent but the tool still uses the MCP (Cursor, OpenCode), instruct the assistant with the stage name ("generate spec", "generate task list", etc.) to trigger the correct prompt.
- Windsurf currently requires registering a simple placeholder tool to prevent the `no tools returned` error. After that, prompts still are not recognized.
- VS Code recognizes the prompts but pastes the entire template back into chat. Until native execution improves, reference the relevant prompt file and run it manually in the chat window.

## How to Contribute Updates

1. Launch the MCP server with the environment you are testing.
2. Note whether prompts load automatically and how the assistant responds to each stage of the SDD workflow.
3. Capture any error messages or required workarounds.
4. Update the support matrix and notes above with your findings.
5. Open a pull request summarizing the change so the community keeps an accurate inventory.

Have results for a tool marked **TBD**? Please add them—this table is only as useful as the data we collectively maintain.
