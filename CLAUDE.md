# Claude Project Instructions

This file is the Claude project bootstrap for Moveo Fintech Tools.

Before making changes, read `CONTEXT.md`. It is the canonical source of truth for product rules, architecture, workflow, CLI UX, setup behavior, skills, autocomplete, and repository conventions.

Also check `ROADMAP.md` for deferred work and future direction. Do not implement deferred roadmap items unless the user explicitly asks for them.

Follow the workflow in `CONTEXT.md`:

- One issue per task.
- One branch per issue.
- Use worktrees for parallel work. For small sequential fixes, a normal feature branch is fine.
- One pull request per issue.

Do not work directly on `master`.

When given a GitHub issue URL, read the issue body and acceptance criteria, check dependency status, confirm the branch matches the suggested branch, implement only the issue scope, run verification, and summarize changed files and test results.

Do not implement blocked issues. If an issue has `status:blocked`, says `Dependency status: Blocked`, or lists open blockers, stop and report the blockers instead of writing code.

Important reminders:

- Keep CLI handlers thin.
- Put reusable logic outside command handlers.
- Support `--help` for every command and subcommand.
- Support autocomplete where practical.
- Use Typer, Rich, questionary, and PyYAML.
- Skills are agent-agnostic.
- Do not add `supported_agents` to skill metadata.
- Show summaries and ask for confirmation before persistent or destructive changes.
- Do not modify unrelated user changes.
