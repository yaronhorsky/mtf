from __future__ import annotations

import getpass
import subprocess
from pathlib import Path


def _git_config(key: str, *, global_config: bool) -> str | None:
    args = ["git", "config"]
    if global_config:
        args.append("--global")
    args.append(key)

    try:
        result = subprocess.run(args, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return None

    value = result.stdout.strip()
    return value or None


def detect_name() -> str | None:
    return (
        _git_config("user.name", global_config=True)
        or _git_config("user.name", global_config=False)
        or getpass.getuser()
        or None
    )


def detect_email() -> str | None:
    return _git_config("user.email", global_config=True) or _git_config(
        "user.email", global_config=False
    )


def detect_agents() -> list[str]:
    home = Path.home()
    candidates = {
        "claude": [
            home / ".claude",
            home / ".claude.json",
            home / ".claude" / "settings.json",
        ],
        "kiro": [
            home / ".kiro",
            home / ".kiro" / "steering",
        ],
        "opencode": [
            home / ".config" / "opencode",
            home / ".config" / "opencode" / "opencode.json",
            home / ".config" / "opencode" / "opencode.jsonc",
            home / ".config" / "opencode" / "skills",
            home / ".opencode",
        ],
    }

    return [agent for agent, paths in candidates.items() if any(path.exists() for path in paths)]
