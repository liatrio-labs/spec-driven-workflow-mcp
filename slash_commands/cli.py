"""Typer CLI for generating slash commands."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer

from slash_commands import SlashCommandWriter, detect_agents, get_agent_config, list_agent_keys

app = typer.Typer(
    name="sdd-generate-commands",
    help="Generate slash command files for AI code assistants",
)


@app.command()
def generate(  # noqa: PLR0913
    prompts_dir: Annotated[
        Path,
        typer.Option(
            "--prompts-dir",
            "-p",
            help="Directory containing prompt files",
        ),
    ] = Path("prompts"),
    agents: Annotated[
        list[str] | None,
        typer.Option(
            "--agents",
            "-a",
            help="Agent keys to generate commands for (can be specified multiple times)",
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Show what would be done without writing files",
        ),
    ] = False,
    yes: Annotated[
        bool,
        typer.Option(
            "--yes",
            "-y",
            help="Skip confirmation prompts",
        ),
    ] = True,
    base_path: Annotated[
        Path | None,
        typer.Option(
            "--base-path",
            "-b",
            help="Base directory for output paths",
        ),
    ] = None,
    list_agents_flag: Annotated[
        bool,
        typer.Option(
            "--list-agents",
            help="List all supported agents and exit",
        ),
    ] = False,
) -> None:
    """Generate slash command files for AI code assistants."""
    # Handle --list-agents
    if list_agents_flag:
        print("Supported agents:")
        for agent_key in list_agent_keys():
            try:
                agent = get_agent_config(agent_key)
                print(f"  {agent_key:20} - {agent.display_name}")
            except KeyError:
                print(f"  {agent_key:20} - Unknown")
        return

    # Detect agents if not specified
    if agents is None or len(agents) == 0:
        detected = detect_agents(base_path or Path.cwd())
        if not detected:
            print("No agents detected. Use --agents to specify agents manually.")
            sys.exit(1)
        agents = [agent.key for agent in detected]
        print(f"Detected agents: {', '.join(agents)}")

    # Create writer
    writer = SlashCommandWriter(
        prompts_dir=prompts_dir,
        agents=agents,
        dry_run=dry_run,
        base_path=base_path,
    )

    # Generate commands
    try:
        result = writer.generate()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Print summary
    mode = "DRY RUN" if dry_run else "Generation"
    print(f"\n{mode} complete:")
    print(f"  Prompts loaded: {result['prompts_loaded']}")
    print(f"  Files {'would be' if dry_run else ''} written: {result['files_written']}")
    print("\nFiles:")
    for file_info in result["files"]:
        print(f"  - {file_info['path']}")
        print(f"    Agent: {file_info['agent_display_name']} ({file_info['agent']})")


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
