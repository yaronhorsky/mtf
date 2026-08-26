# Agent Instructions

When working in this repository, read `CONTEXT.md` before making changes.

Also check `ROADMAP.md` for deferred work and future direction. Do not implement deferred roadmap items unless the user explicitly asks for them.

## Workflow

Work should happen through GitHub issues, feature branches, and pull requests.

Use this model:

- One issue per task.
- One branch per issue.
- One worktree per branch when working in parallel.
- One pull request per issue.

Do not work directly on `master`.

## Starting A Task

When given a GitHub issue URL:

1. Read the issue body and acceptance criteria.
2. Read `CONTEXT.md`.
3. Read `ROADMAP.md` only to understand deferred work.
4. Confirm the current branch matches the issue's suggested branch.
5. Implement only the issue scope.
6. Do not implement out-of-scope items.
7. Run the verification commands from the issue.
8. Summarize changed files and test results.

## Worktree Expectations

If the user asks to work on an issue and no suitable worktree exists, recommend creating one from the bare repo:

```bash
cd ../moveo_fintech.git
git worktree add ../moveo_fintech-<short-name> -b feature/<branch-name> master
```

If already inside a task-specific worktree, continue there.

## Implementation Rules

Follow `CONTEXT.md` as the source of truth.

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
