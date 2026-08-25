from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


CONFIG_DIR = Path.home() / ".moveo_fintech"
CONFIG_PATH = CONFIG_DIR / "config.yaml"


@dataclass(frozen=True)
class UserConfig:
    name: str
    email: str
    role: str
    agents: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "user": {
                "name": self.name,
                "email": self.email,
                "role": self.role,
            },
            "agents": {
                "default": self.agents,
            },
        }


def load_config() -> UserConfig | None:
    if not CONFIG_PATH.exists():
        return None

    data = yaml.safe_load(CONFIG_PATH.read_text()) or {}
    user = data.get("user", {})
    agents = data.get("agents", {}).get("default", [])

    name = user.get("name")
    email = user.get("email")
    role = user.get("role")

    if not name or not email or not role:
        return None

    return UserConfig(
        name=str(name),
        email=str(email),
        role=str(role),
        agents=[str(agent) for agent in agents],
    )


def save_config(config: UserConfig) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(yaml.safe_dump(config.as_dict(), sort_keys=False))
