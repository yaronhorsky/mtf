from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.table import Table

from mft import __version__
from mft.config import load_config
from mft.setup_flow import run_setup, run_setup_edit
from mft.ui import console, print_config_summary


app = typer.Typer(
    help="Moveo Fintech Tools: share practical team knowledge through the moveo-fintech CLI.",
    no_args_is_help=True,
)
setup_app = typer.Typer(help="Set up or edit your local MFT configuration.")
skill_app = typer.Typer(help="List, install, remove, share, and validate skills.")


def version_callback(value: bool) -> None:
    if value:
        console.print(f"moveo-fintech {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the installed moveo-fintech version.",
    ),
) -> None:
    """Moveo Fintech Tools."""


@setup_app.callback(invoke_without_command=True)
def setup_callback(ctx: typer.Context) -> None:
    """Run first-time setup."""
    if ctx.invoked_subcommand is None:
        run_setup()


@setup_app.command("edit")
def setup_edit() -> None:
    """Edit your saved MFT setup."""
    run_setup_edit()


@app.command()
def whoami() -> None:
    """Show the current MFT identity, role, and configured agents."""
    config = load_config()
    if not config:
        console.print("[yellow]Moveo Fintech is not set up yet. Run:[/yellow] [bold]moveo-fintech setup[/bold]")
        raise typer.Exit(1)

    print_config_summary(
        "Current MFT setup",
        name=config.name,
        email=config.email,
        role=config.role,
        agents=config.agents,
    )


def complete_skill_ids(incomplete: str) -> list[str]:
    return []


def complete_installed_skill_ids(incomplete: str) -> list[str]:
    return []


@skill_app.command("list")
def skill_list() -> None:
    """List marketplace skills."""
    table = Table(title="Available skills")
    table.add_column("ID", style="cyan")
    table.add_column("Area", style="magenta")
    table.add_column("Description", style="white")
    console.print(table)
    console.print("[yellow]Skill registry is not implemented yet.[/yellow]")


@skill_app.command("show")
def skill_show(
    skill_id: str = typer.Argument(..., help="Skill ID to show.", autocompletion=complete_skill_ids),
) -> None:
    """Show details for one marketplace skill."""
    console.print(f"[yellow]Skill show is not implemented yet:[/yellow] {skill_id}")


@skill_app.command("install")
def skill_install(
    skill_id: Optional[str] = typer.Argument(
        None,
        help="Skill ID to install. Omit to open the interactive selector.",
        autocompletion=complete_skill_ids,
    ),
) -> None:
    """Install one skill or choose skills interactively."""
    if skill_id:
        console.print(f"[yellow]Skill install is not implemented yet:[/yellow] {skill_id}")
    else:
        console.print("[yellow]Interactive skill install is not implemented yet.[/yellow]")


@skill_app.command("remove")
def skill_remove(
    skill_id: Optional[str] = typer.Argument(
        None,
        help="Installed skill ID to remove. Omit to open the interactive selector.",
        autocompletion=complete_installed_skill_ids,
    ),
) -> None:
    """Remove one installed MFT skill or choose installed skills interactively."""
    if skill_id:
        console.print(f"[yellow]Skill remove is not implemented yet:[/yellow] {skill_id}")
    else:
        console.print("[yellow]Interactive skill remove is not implemented yet.[/yellow]")


@skill_app.command("share")
def skill_share(
    path: Path = typer.Argument(..., exists=True, help="Path to a skill file or folder."),
) -> None:
    """Share a local skill file or folder with the marketplace."""
    console.print(f"[yellow]Skill share is not implemented yet:[/yellow] {path}")


@skill_app.command("validate")
def skill_validate(
    path: Path = typer.Argument(..., exists=True, help="Path to a skill file or folder."),
) -> None:
    """Validate a local skill file or folder."""
    console.print(f"[yellow]Skill validate is not implemented yet:[/yellow] {path}")


app.add_typer(setup_app, name="setup")
app.add_typer(skill_app, name="skill")
