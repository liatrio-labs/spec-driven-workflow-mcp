"""Typer CLI for generating slash commands."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import questionary
import typer

from slash_commands import SlashCommandWriter, detect_agents, get_agent_config, list_agent_keys

app = typer.Typer(
    name="sdd-generate-commands",
    help="Generate slash command files for AI code assistants",
)


def _prompt_agent_selection(detected_agents: list) -> list:
    """Prompt user to select which agents to generate commands for.

    Args:
        detected_agents: List of detected agent configurations

    Returns:
        List of selected agent configurations (empty if cancelled)
    """

    choices = [
        questionary.Choice(
            f"{agent.display_name} ({agent.key})",
            agent,
            checked=True,  # Pre-check all detected agents
        )
        for agent in detected_agents
    ]

    selected = questionary.checkbox(
        "Select agents to generate commands for (use space to select/deselect, enter to confirm):",
        choices=choices,
    ).ask()

    if selected is None:
        # User pressed Ctrl+C
        return []

    return selected


@app.command()
def generate(  # noqa: PLR0913 PLR0912 PLR0915
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
    ] = False,
    base_path: Annotated[
        Path | None,
        typer.Option(
            "--base-path",
            "-b",
            help="Base directory for output paths",
        ),
    ] = None,
    detection_path: Annotated[
        Path | None,
        typer.Option(
            "--detection-path",
            "-d",
            help="Directory to search for agent configurations (defaults to current directory)",
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
        # Use detection_path if specified, otherwise base_path, otherwise current directory
        detection_dir = (
            detection_path
            if detection_path is not None
            else (base_path if base_path is not None else Path.cwd())
        )
        detected = detect_agents(detection_dir)
        if not detected:
            print("No agents detected. Use --agents to specify agents manually.")
            print(f"Detection path: {detection_dir}")
            sys.exit(1)

        # Interactive selection: all detected agents pre-selected
        if not yes:
            selected_agents = _prompt_agent_selection(detected)
            if not selected_agents:
                print("No agents selected. Exiting.")
                sys.exit(1)
            agents = [agent.key for agent in selected_agents]
        else:
            # If --yes is used, auto-select all detected agents
            agents = [agent.key for agent in detected]
            print(f"Detected agents: {', '.join(agents)}")
    else:
        print(f"Selected agents: {', '.join(agents)}")

    # Create writer
    overwrite_action = "overwrite" if yes else None
    writer = SlashCommandWriter(
        prompts_dir=prompts_dir,
        agents=agents,
        dry_run=dry_run,
        base_path=base_path,
        overwrite_action=overwrite_action,
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
    except RuntimeError as e:
        if "Cancelled" in str(e):
            print("Operation cancelled by user.", file=sys.stderr)
            sys.exit(1)
        raise

    # Print summary
    mode = "DRY RUN" if dry_run else "Generation"
    print(f"\n{mode} complete:")
    print(f"  Prompts loaded: {result['prompts_loaded']}")
    print(f"  Files {'would be' if dry_run else ''} written: {result['files_written']}")
    if result.get("backups_created"):
        print(f"  Backups created: {len(result['backups_created'])}")
        for backup in result["backups_created"]:
            print(f"    - {backup}")
    print("\nFiles:")
    for file_info in result["files"]:
        print(f"  - {file_info['path']}")
        print(f"    Agent: {file_info['agent_display_name']} ({file_info['agent']})")


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
