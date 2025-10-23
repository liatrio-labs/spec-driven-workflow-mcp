"""Typer CLI for generating slash commands."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated, Any

import questionary
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from slash_commands import (
    SlashCommandWriter,
    detect_agents,
    get_agent_config,
    list_agent_keys,
)

app = typer.Typer(
    name="sdd-generate-commands",
    help="Generate slash command files for AI code assistants",
)

console = Console()


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
    target_path: Annotated[
        Path | None,
        typer.Option(
            "--target-path",
            "-t",
            help="Target directory for output paths (defaults to home directory)",
        ),
    ] = None,
    detection_path: Annotated[
        Path | None,
        typer.Option(
            "--detection-path",
            "-d",
            help="Directory to search for agent configurations (defaults to home directory)",
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
        # Create Rich table
        table = Table(title="Supported Agents")
        table.add_column("Agent Key", style="cyan", no_wrap=True)
        table.add_column("Display Name", style="magenta")
        table.add_column("Target Path", style="blue")
        table.add_column("Detected", justify="center")

        # Get home directory for checking paths
        home_dir = Path.home()

        for agent_key in list_agent_keys():
            try:
                agent = get_agent_config(agent_key)
                # Check if command directory exists
                command_path = home_dir / agent.command_dir
                exists = command_path.exists()
                detected = "[green]✓[/green]" if exists else "[red]✗[/red]"

                table.add_row(
                    agent_key,
                    agent.display_name,
                    f"~/{agent.command_dir}",
                    detected,
                )
            except KeyError:
                table.add_row(agent_key, "Unknown", "N/A", "[red]✗[/red]")

        console.print(table)
        return

    # Detect agents if not specified
    if agents is None or len(agents) == 0:
        # Use detection_path if specified, otherwise target_path, otherwise home directory
        detection_dir = (
            detection_path
            if detection_path is not None
            else (target_path if target_path is not None else Path.home())
        )
        detected = detect_agents(detection_dir)
        if not detected:
            print("Error: No agents detected.", file=sys.stderr)
            print(f"Detection path: {detection_dir}", file=sys.stderr)
            print("\nTo fix this:", file=sys.stderr)
            print(
                "  1. Ensure at least one agent directory exists (e.g., .claude, .cursor, .gemini)",
                file=sys.stderr,
            )
            print(
                "  2. Or use --agents to specify agents manually: --agents claude-code",
                file=sys.stderr,
            )
            print(
                "  3. Or use --detection-path to search in a different directory", file=sys.stderr
            )
            sys.exit(2)  # Validation error

        # Interactive selection: all detected agents pre-selected
        if not yes:
            selected_agents = _prompt_agent_selection(detected)
            if not selected_agents:
                print("Cancelled: No agents selected.", file=sys.stderr)
                sys.exit(1)  # User cancellation
            agents = [agent.key for agent in selected_agents]
        else:
            # If --yes is used, auto-select all detected agents
            agents = [agent.key for agent in detected]
            print(f"Detected agents: {', '.join(agents)}")
    else:
        print(f"Selected agents: {', '.join(agents)}")

    # Determine target path (default to home directory)
    actual_target_path = target_path if target_path is not None else Path.home()

    # Create writer
    overwrite_action = "overwrite" if yes else None
    writer = SlashCommandWriter(
        prompts_dir=prompts_dir,
        agents=agents,
        dry_run=dry_run,
        base_path=actual_target_path,
        overwrite_action=overwrite_action,
    )

    # Generate commands
    try:
        result = writer.generate()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nTo fix this:", file=sys.stderr)
        print("  - Ensure the prompts directory exists", file=sys.stderr)
        print(
            f"  - Check that --prompts-dir points to a valid directory (current: {prompts_dir})",
            file=sys.stderr,
        )
        sys.exit(3)  # I/O error (e.g., prompts directory doesn't exist)
    except KeyError as e:
        print(f"Error: Invalid agent key: {e}", file=sys.stderr)
        print("\nTo fix this:", file=sys.stderr)
        print("  - Use --list-agents to see all supported agents", file=sys.stderr)
        print("  - Ensure agent keys are spelled correctly", file=sys.stderr)
        print(f"  - Valid agent keys: {', '.join(list_agent_keys())}", file=sys.stderr)
        sys.exit(2)  # Validation error (invalid agent key)
    except PermissionError as e:
        print(f"Error: Permission denied: {e}", file=sys.stderr)
        print("\nTo fix this:", file=sys.stderr)
        print("  - Check file and directory permissions", file=sys.stderr)
        print("  - Ensure you have write access to the output directory", file=sys.stderr)
        print("  - Try running with elevated permissions if needed", file=sys.stderr)
        sys.exit(3)  # I/O error (permission denied)
    except OSError as e:
        print(f"Error: I/O error: {e}", file=sys.stderr)
        print("\nTo fix this:", file=sys.stderr)
        print("  - Check that the output directory is writable", file=sys.stderr)
        print("  - Ensure there's sufficient disk space", file=sys.stderr)
        print(
            f"  - Verify the path exists: {actual_target_path}",
            file=sys.stderr,
        )
        sys.exit(3)  # I/O error (file system errors)
    except RuntimeError as e:
        if "Cancelled" in str(e):
            print("Cancelled: Operation cancelled by user.", file=sys.stderr)
            sys.exit(1)  # User cancellation
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


@app.command()
def cleanup(
    agents: Annotated[
        list[str] | None,
        typer.Option(
            "--agents",
            "-a",
            help=(
                "Agent keys to clean (can be specified multiple times). "
                "If not specified, cleans all agents."
            ),
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Show what would be deleted without actually deleting files",
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
    target_path: Annotated[
        Path | None,
        typer.Option(
            "--target-path",
            "-t",
            help="Target directory to search for generated files (defaults to home directory)",
        ),
    ] = None,
    include_backups: Annotated[
        bool,
        typer.Option(
            "--include-backups/--no-backups",
            help="Include backup files in cleanup (default: True)",
        ),
    ] = True,
) -> None:
    """Clean up generated slash command files."""
    # Determine target path (default to home directory)
    actual_target_path = target_path if target_path is not None else Path.home()

    # Create writer for finding files
    writer = SlashCommandWriter(
        prompts_dir=Path("prompts"),  # Not used for cleanup
        agents=[],
        dry_run=dry_run,
        base_path=actual_target_path,
    )

    # Find files
    found_files = writer.find_generated_files(agents=agents, include_backups=include_backups)

    if not found_files:
        console.print("[green]No generated files found.[/green]")
        return

    # Display what will be deleted in a table
    table = Table(title=f"Found {len(found_files)} file(s) to delete")
    table.add_column("File Path", style="cyan", no_wrap=False)
    table.add_column("Agent", style="magenta")
    table.add_column("Type", style="yellow", justify="center")

    # Group files by agent for better readability
    files_by_agent: dict[str, list[dict[str, Any]]] = {}
    for file_info in found_files:
        agent = file_info["agent_display_name"]
        if agent not in files_by_agent:
            files_by_agent[agent] = []
        files_by_agent[agent].append(file_info)

    # Add rows to table
    for agent, files in sorted(files_by_agent.items()):
        for file_info in files:
            type_display = {
                "command": "[green]command[/green]",
                "backup": "[yellow]backup[/yellow]",
            }.get(file_info["type"], file_info["type"])
            table.add_row(
                str(file_info["path"]),
                agent,
                type_display,
            )

    console.print()
    console.print(table)

    # Prompt for confirmation
    if not yes:
        console.print()
        console.print(
            Panel(
                "[bold red]⚠️  WARNING: This will permanently delete "
                "the files listed above.[/bold red]",
                title="Confirm Deletion",
                border_style="red",
            )
        )
        confirmed = questionary.confirm("Are you sure you want to proceed?", default=False).ask()
        if not confirmed:
            console.print("[yellow]Cleanup cancelled.[/yellow]")
            sys.exit(1)

    # Perform cleanup
    try:
        result = writer.cleanup(agents=agents, include_backups=include_backups, dry_run=dry_run)
    except Exception as e:
        console.print(f"[bold red]Error during cleanup: {e}[/bold red]")
        sys.exit(3)

    # Print summary in a panel
    mode = "DRY RUN" if dry_run else "Cleanup"
    deleted_text = "would be" if dry_run else ""
    summary_lines = [
        f"Files {deleted_text} deleted: [bold green]{result['files_deleted']}[/bold green]",
    ]
    if result.get("errors"):
        summary_lines.append(f"Errors: [bold red]{len(result['errors'])}[/bold red]")
        for error in result["errors"]:
            summary_lines.append(f"  - {error['path']}: {error['error']}")

    console.print()
    console.print(
        Panel(
            "\n".join(summary_lines),
            title=f"{mode} Complete",
            border_style="green" if not result.get("errors") else "red",
        )
    )


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
