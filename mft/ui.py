from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


console = Console()


ASCII_ART = r"""
███╗   ███╗ ██████╗ ██╗   ██╗███████╗ ██████╗
████╗ ████║██╔═══██╗██║   ██║██╔════╝██╔═══██╗
██╔████╔██║██║   ██║██║   ██║█████╗  ██║   ██║
██║╚██╔╝██║██║   ██║╚██╗ ██╔╝██╔══╝  ██║   ██║
██║ ╚═╝ ██║╚██████╔╝ ╚████╔╝ ███████╗╚██████╔╝
╚═╝     ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝ ╚═════╝

███████╗██╗███╗   ██╗████████╗███████╗ ██████╗██╗  ██╗
██╔════╝██║████╗  ██║╚══██╔══╝██╔════╝██╔════╝██║  ██║
█████╗  ██║██╔██╗ ██║   ██║   █████╗  ██║     ███████║
██╔══╝  ██║██║╚██╗██║   ██║   ██╔══╝  ██║     ██╔══██║
██║     ██║██║ ╚████║   ██║   ███████╗╚██████╗██║  ██║
╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝
"""


def print_banner() -> None:
    console.print(Text(ASCII_ART, style="bold cyan"))


def print_config_summary(title: str, *, name: str, email: str, role: str | None, agents: list[str]) -> None:
    table = Table(show_header=False, box=None)
    table.add_column("Field", style="bold magenta")
    table.add_column("Value", style="white")
    table.add_row("Name", name or "missing")
    table.add_row("Email", email or "missing")
    table.add_row("Role", role or "not selected yet")
    table.add_row("Agents", ", ".join(agents) if agents else "none detected")
    console.print(Panel(table, title=title, border_style="cyan"))
