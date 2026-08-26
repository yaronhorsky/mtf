# Moveo Fintech Context

This file is the canonical development context for people building Moveo Fintech Tools. Agent-specific project files such as `AGENTS.md`, `CLAUDE.md`, and Kiro steering files should point here instead of duplicating these rules.

This context is for development of this repository. It is not meant to be installed globally into every coding agent by default.

## Product

Moveo Fintech Tools, exposed through the `moveo-fintech` CLI, is a collaborative knowledge-sharing tool for the Moveo fintech team.

The tool helps developers, QA engineers, and product managers share practical professional knowledge, including workflows, skills, debugging tips, bug-handling flows, QA practices, PM practices, and team-specific operating knowledge.

## Users

- Developers.
- QA engineers.
- Product managers.
- Teammates who may not be terminal-native.

## Core Principles

- MFT should be useful for both technical and non-technical teammates.
- The CLI is the first frontend, not the whole product.
- Business logic should live outside command handlers so it can later be reused by an API server, TUI, or web UI.
- Skills are agent-agnostic knowledge artifacts.
- Agent-specific files are generated or adapted at install time.
- Persistent and destructive operations must show a summary and ask for confirmation.
- Every command and subcommand must support help.
- Autocomplete should work wherever practical.

## Initial Architecture

The MVP should use a Python CLI named `moveo-fintech`.

The repository should eventually separate command handling from reusable core logic:

```text
CLI / future API / future Web UI / future TUI
  -> reusable core logic
  -> repo-backed registry and local MFT state
```

The first implementation can stay simple, but should avoid putting marketplace behavior directly inside Typer command functions.

## Setup Rules

Setup runs automatically after installation.

Setup should:

- Print colorful `MOVEO FINTECH` ASCII art first.
- Derive the user's name, email, and installed agents automatically.
- Prompt only for required missing identity information.
- Present the derived information to the user.
- Ask the user to confirm the derived information.
- Ask for the user's role only after identity confirmation.
- Ask for final confirmation before saving configuration.
- Save configuration under `~/.moveo_fintech/`.
- End with a message saying setup is done.
- Tell the user they can change anything at any time using `moveo-fintech setup edit`.

Detected agents should include:

- Claude.
- Kiro steering.
- OpenCode.

## Skill Model

Skills are canonical, agent-agnostic knowledge artifacts.

Skill metadata should not contain `supported_agents`. All skills should be installable into all currently supported agents through adapters.

The canonical skill should include:

- `id`.
- `name`.
- `description`.
- `area`.
- `created_by`.
- `tags`.
- `version`.

The skill description is the marketplace one-liner shown by `moveo-fintech skill list` and by interactive install selectors.

Allowed areas are:

- `dev`.
- `qa`.
- `pm`.
- `general`.

## Skill Commands

Use human product language.

Prefer:

- `share` instead of `upload`.
- `remove` instead of `delete`.
- `setup edit` for changing configuration.

Initial skill commands:

```bash
moveo-fintech skill list
moveo-fintech skill show <skill-id>
moveo-fintech skill install
moveo-fintech skill install <skill-id>
moveo-fintech skill remove
moveo-fintech skill remove <skill-id>
moveo-fintech skill share <path>
moveo-fintech skill validate <path>
```

## Install Rules

`moveo-fintech skill install` without a skill ID opens an interactive multi-select list of marketplace skills.

`moveo-fintech skill install <skill-id>` installs one skill directly.

Skills are installed into all agents configured for the user. The command should not expose per-skill agent support because skills are agent-agnostic.

Before installation, show a summary that includes:

- Selected skills.
- Target agents.
- One-line descriptions where useful.

Ask for confirmation before writing files.

## Remove Rules

`moveo-fintech skill remove` without a skill ID opens an interactive multi-select list of installed MFT skills.

`moveo-fintech skill remove <skill-id>` removes one installed MFT skill.

Remove from all configured agents. Do not include `--agent` for removal in the MVP.

Only remove skills that were installed by MFT and recorded in local MFT state.

Before removal, detect whether installed skill files changed since installation. If changes are detected, warn the user and ask how to proceed.

Always show a removal summary and ask for approval before deleting files.

## Share Rules

`moveo-fintech skill share <path>` turns a local skill file or folder into a marketplace skill.

Share should:

- Read the provided file or folder.
- Parse existing metadata if present.
- Prompt for missing metadata.
- Validate the skill.
- Normalize the skill structure.
- Generate or prepare agent-specific adaptations where needed.
- Show a summary.
- Ask for confirmation before adding it to the local marketplace.

## Agent Targets

Initial global install targets:

```text
Claude:
~/.claude/skills/<skill-id>/SKILL.md

Kiro:
~/.kiro/steering/<skill-id>.md

OpenCode:
~/.config/opencode/skills/<skill-id>/SKILL.md
```

## CLI UX

Use Typer for command structure, help, and completion support.

Use Rich for colorful output, panels, summaries, and tables.

Use questionary for confirmations, role choices, and multi-select flows.

The CLI should remain friendly to teammates who are not comfortable with terminals.

## Autocomplete

Autocomplete should be supported broadly.

Required dynamic completions:

- `moveo-fintech skill show <tab>` should complete marketplace skill IDs.
- `moveo-fintech skill install <tab>` should complete marketplace skill IDs.
- `moveo-fintech skill remove <tab>` should complete installed MFT skill IDs.
- `moveo-fintech skill share <tab>` should use path completion.
- `moveo-fintech skill validate <tab>` should use path completion.

## Development Workflow

Development should happen through GitHub issues, feature branches, and pull requests.

Use this model:

- One issue per task.
- One branch per issue.
- One worktree per branch when working in parallel.
- One pull request per issue.

Do not work directly on `master`.

When given a GitHub issue URL:

1. Read the issue body and acceptance criteria.
2. Read this file.
3. Read `ROADMAP.md` only to understand deferred work and future direction.
4. Check the issue dependency status and blockers.
5. Confirm the current branch matches the issue's suggested branch.
6. Implement only the issue scope.
7. Do not implement out-of-scope items.
8. Run the verification commands from the issue.
9. Summarize changed files and test results.

## Dependency Guardrail

Before implementing a GitHub issue, check whether the issue is blocked.

Do not implement an issue if:

- It has a `status:blocked` label.
- Its `Dependency status` section says it is blocked.
- Its `Blocked by` section lists open issues.

If the issue is blocked, stop and report the blockers instead of writing code.

Only implement issues that are explicitly ready, either by a `status:ready` label or a `Dependency status` section that says `Ready now`.

When working in parallel, prefer worktrees created from the bare repository:

```bash
cd ../moveo_fintech.git
git worktree add ../moveo_fintech-<short-name> -b feature/<branch-name> master
```

If already inside a task-specific worktree, continue there.

## Repository Rules

The intended GitHub setup is:

- No direct pushes to `master`.
- Work through feature branches.
- Pull requests are required.
- Pull requests require approval before merge.
- Repository ownership and approval rules will be configured later.

Do not modify unrelated user changes.

## Agent Project Files

Agent-specific project files are bootstraps only.

Use:

- `AGENTS.md` for OpenCode.
- `CLAUDE.md` for Claude.
- `.kiro/steering/moveo-fintech.md` for Kiro.

These files should instruct the agent to read this `CONTEXT.md` file and check `ROADMAP.md`. They should not become independent sources of truth.

## Deferred Ideas

Deferred ideas belong in `ROADMAP.md`. Do not overbuild them into the MVP unless explicitly requested.
