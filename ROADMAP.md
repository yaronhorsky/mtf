# Roadmap

This roadmap captures the first implementation target and the larger ideas that are intentionally deferred. The goal is to keep the MVP focused while preserving the full product direction.

## MVP

- Create a Python CLI named `moveo-fintech`.
- Provide a one-line installer using `curl ... | bash`.
- Run `moveo-fintech setup` automatically after installation.
- Start setup with colorful `MOVEO FINTECH` ASCII art.
- Derive the user's name, email, and installed agents automatically.
- Prompt for required missing identity information.
- Present the derived setup summary and ask for confirmation.
- Ask for the user's role after identity confirmation.
- Confirm the final setup before writing configuration.
- Support `moveo-fintech setup edit` for changing setup at any time.
- Store local user configuration under `~/.moveo_fintech/`.
- Detect Claude, Kiro, and OpenCode global configurations.
- Treat skills as agent-agnostic knowledge artifacts.
- Maintain a repo-backed skill registry.
- Show each skill's one-line description from the registry.
- Support `moveo-fintech skill list`.
- Support `moveo-fintech skill show <skill-id>`.
- Support `moveo-fintech skill install` with an interactive multi-select list.
- Support `moveo-fintech skill install <skill-id>` for direct installs.
- Install skills globally into all configured agents.
- Generate agent-specific adaptations at install time when needed.
- Support Claude global skills.
- Support Kiro global steering files.
- Support OpenCode global skills.
- Track installed skills in local MFT state.
- Support `moveo-fintech skill remove` with an interactive multi-select list of installed skills.
- Support `moveo-fintech skill remove <skill-id>`.
- Remove skills from all configured agents.
- Remove only skills that were installed through MFT.
- Detect local changes before removing installed skill files.
- Prompt for approval before committing removals.
- Support `moveo-fintech skill share <path>`.
- Validate skills as part of `share`.
- Prompt for missing skill metadata during `share`.
- Show a share summary and ask for confirmation before adding the skill.
- Support help for every command and subcommand.
- Support shell autocomplete out of the box.
- Support dynamic autocomplete for registry skills and installed skills.
- Use colorful output and friendly selectors for setup and user prompts.

## Post-MVP

- Add an API server layer that reuses the same core logic as the CLI.
- Add a web UI for teammates who do not want to use the terminal.
- Add a TUI for richer terminal workflows.
- Add GitHub-backed publishing for shared skills.
- Add automated pull request creation for new shared skills.
- Add a skill suggestion and improvement flow.
- Add review and approval workflows for marketplace changes.
- Add local LLM-assisted metadata generation.
- Add CI-assisted metadata enrichment and validation.
- Add skill versioning.
- Add skill update and upgrade commands.
- Add richer diff viewing before removing locally changed skills.
- Add managed markers for installed skills when needed.
- Add adapter refresh commands for regenerating agent-specific files.
- Add a developer-only command for installing MFT development context into coding agents.
- Add enterprise authentication if the API server becomes shared infrastructure.
- Add audit trails for shared, installed, updated, and removed skills.
- Add server-side search and filtering.
- Add role-based skill recommendations.
- Add skill ownership and maintainership metadata.
- Add deprecation support for outdated skills.
- Add changelogs for skills.
- Add support for more coding agents over time.

## Testing Roadmap

- Add unit tests for identity detection.
- Add unit tests for agent detection.
- Add unit tests for setup configuration generation.
- Add unit tests for skill metadata validation.
- Add unit tests for skill ID normalization.
- Add unit tests for registry read/write behavior.
- Add unit tests for install state tracking.
- Add unit tests for installed skill hashing.
- Add unit tests for local-change detection before removal.
- Add unit tests for Claude adapter rendering.
- Add unit tests for Kiro steering adapter rendering.
- Add unit tests for OpenCode adapter rendering.
- Add CLI tests for top-level help.
- Add CLI tests for every command and subcommand help output.
- Add CLI tests for `moveo-fintech setup`.
- Add CLI tests for `moveo-fintech setup edit`.
- Add CLI tests for `moveo-fintech skill list`.
- Add CLI tests for `moveo-fintech skill show <skill-id>`.
- Add CLI tests for `moveo-fintech skill install`.
- Add CLI tests for `moveo-fintech skill install <skill-id>`.
- Add CLI tests for `moveo-fintech skill remove`.
- Add CLI tests for `moveo-fintech skill remove <skill-id>`.
- Add CLI tests for `moveo-fintech skill share <path>`.
- Add fixture-based tests for valid and invalid skills.
- Add smoke tests for the install script.
- Add shell completion tests where practical.
- Add GitHub Actions CI.
- Require CI to pass before merging pull requests.
- Add branch protection for `master`.
- Require feature branches and pull requests for all changes.
