from __future__ import annotations

import questionary
import typer

from mft.config import UserConfig, load_config, save_config
from mft.detect import detect_agents, detect_email, detect_name
from mft.ui import console, print_banner, print_config_summary


ROLE_CHOICES = [
    questionary.Choice("Developer", value="dev"),
    questionary.Choice("QA", value="qa"),
    questionary.Choice("PM", value="pm"),
]

AGENT_CHOICES = [
    questionary.Choice("Claude", value="claude"),
    questionary.Choice("Kiro", value="kiro"),
    questionary.Choice("OpenCode", value="opencode"),
]


def _required_text(message: str, default: str | None = None) -> str:
    while True:
        value = questionary.text(message, default=default or "").ask()
        if value and value.strip():
            return value.strip()
        console.print("[red]This field is required.[/red]")


def _confirm(message: str, default: bool = True) -> bool:
    result = questionary.confirm(message, default=default).ask()
    return bool(result)


def _select_role(default: str | None = None) -> str:
    choices = [
        questionary.Choice(choice.title, value=choice.value, checked=choice.value == default)
        for choice in ROLE_CHOICES
    ]
    role = questionary.select("Choose your role:", choices=choices).ask()
    return str(role or default or "dev")


def _select_agents(defaults: list[str]) -> list[str]:
    choices = [
        questionary.Choice(choice.title, value=choice.value, checked=choice.value in defaults)
        for choice in AGENT_CHOICES
    ]
    agents = questionary.checkbox("Which agents should MFT manage?", choices=choices).ask()
    return [str(agent) for agent in agents] if agents else []


def _edit_identity(name: str | None, email: str | None, agents: list[str]) -> tuple[str, str, list[str]]:
    name = _required_text("Name:", default=name)
    email = _required_text("Email:", default=email)
    agents = _select_agents(agents)
    return name, email, agents


def run_setup() -> None:
    print_banner()
    console.print("[bold]Setting up your Moveo Fintech Tools workspace...[/bold]\n")

    name = detect_name()
    email = detect_email()
    agents = detect_agents()

    if not name:
        name = _required_text("We could not detect your name. Name:")
    if not email:
        email = _required_text("We could not detect your email. Email:")

    while True:
        print_config_summary(
            "Derived setup",
            name=name,
            email=email,
            role=None,
            agents=agents,
        )
        if _confirm("Use this derived information?"):
            break
        name, email, agents = _edit_identity(name, email, agents)

    role = _select_role()

    while True:
        print_config_summary(
            "Setup summary",
            name=name,
            email=email,
            role=role,
            agents=agents,
        )
        if _confirm("Save this setup?"):
            break

        edit_choice = questionary.select(
            "What would you like to edit?",
            choices=[
                questionary.Choice("Identity and agents", value="identity"),
                questionary.Choice("Role", value="role"),
                questionary.Choice("Cancel setup", value="cancel"),
            ],
        ).ask()
        if edit_choice == "identity":
            name, email, agents = _edit_identity(name, email, agents)
        elif edit_choice == "role":
            role = _select_role(role)
        else:
            console.print("[yellow]Setup cancelled. No configuration was saved.[/yellow]")
            raise typer.Exit(1)

    save_config(UserConfig(name=name, email=email, role=role, agents=agents))
    console.print("\n[bold green]Setup done.[/bold green]")
    console.print("You can change anything at any time using: [bold]moveo-fintech setup edit[/bold]")


def run_setup_edit() -> None:
    current = load_config()
    name = current.name if current else detect_name()
    email = current.email if current else detect_email()
    role = current.role if current else None
    agents = current.agents if current else detect_agents()

    print_banner()
    console.print("[bold]Editing your Moveo Fintech Tools setup...[/bold]\n")

    name, email, agents = _edit_identity(name, email, agents)
    role = _select_role(role)

    print_config_summary(
        "Updated setup summary",
        name=name,
        email=email,
        role=role,
        agents=agents,
    )
    if not _confirm("Save these changes?"):
        console.print("[yellow]No changes saved.[/yellow]")
        return

    save_config(UserConfig(name=name, email=email, role=role, agents=agents))
    console.print("[bold green]Setup updated.[/bold green]")
