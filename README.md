# Moveo Fintech Tools

`mft` is a collaborative tool for sharing professional knowledge across the Moveo fintech team.

It is designed for developers, QA engineers, and product managers who want a shared place for practical workflows, skills, debugging tips, bug-handling flows, QA practices, PM practices, and other team knowledge.

Created from Yaron's excellent instinct that team knowledge should be easy to share, easy to install, and useful for both technical and non-technical teammates.

## Installation 🚀

```bash
curl -fsSL https://raw.githubusercontent.com/<org>/moveo_fintech/master/scripts/install.sh | bash
```

This prepares Python, pipx, dependencies, shell completion, and then runs setup.

You can change setup later with:

```bash
mft setup edit
```

## Dependencies 🧰

The CLI is built with Python.

The installer prepares the runtime needed by the CLI, including:

- Python 3.11+.
- pipx when needed.
- Required Python packages.
- Shell completion where possible.

The core Python packages are expected to include:

- Typer.
- Rich.
- questionary.
- PyYAML.

## What MFT Does 💡

The first product area is the skill marketplace.

Skills are agent-agnostic professional knowledge artifacts. A skill can describe a workflow, debugging approach, QA checklist, product practice, bug-handling process, or any other reusable team knowledge.

MFT can then adapt and install those skills into supported agents such as Claude, Kiro steering, and OpenCode.

## Planned Commands 🧭

```bash
mft setup
mft setup edit
mft whoami
mft skill list
mft skill show <skill-id>
mft skill install
mft skill install <skill-id>
mft skill remove
mft skill remove <skill-id>
mft skill share <path>
mft skill validate <path>
```

Every command and subcommand should support `--help`.

Autocomplete should work out of the box where possible, including skill IDs and installed skill IDs.

## Setup ✨

Setup runs automatically after installation.

It derives the user's name, email, and installed agents, prompts for missing required information, asks for confirmation, asks for the user's role, and saves the configuration.

Setup starts with colorful `MOVEO FINTECH` ASCII art.

Anything can be changed later with:

```bash
mft setup edit
```

## CONTEXT.md 📘

`CONTEXT.md` is the development context for people building MFT itself.

It explains the product rules, setup behavior, skill model, CLI UX principles, architecture direction, and repository conventions.

It is not meant to be globally loaded into every coding agent by default. Use it when intentionally working on this repository.

## Roadmap 🗺️

See `ROADMAP.md` for the MVP scope, deferred ideas, and testing roadmap.

## Contributing 🤝

MFT is intended to be a collaborative team tool.

Contributions, pull requests, issues, improvement ideas, and new shared skills are welcome.

If you see a workflow, debugging trick, QA checklist, PM practice, or bug-handling pattern that could help the team, this project should make it easy to share.
