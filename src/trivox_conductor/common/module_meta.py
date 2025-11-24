from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from trivox_conductor.constants import Role


def _normalize_key(name: str) -> str:
    """Normalize a module key; use kebab/snake as-is, lowercase."""
    return name.strip().lower()


def _to_title(name: str) -> str:
    """
    Convert 'capture', 'capture_obs', 'capture-obs' -> 'Capture Obs'.
    """
    s = name.replace("-", " ").replace("_", " ")
    return s.title()


def _to_snake(name: str) -> str:
    """
    Convert 'Capture Obs', 'capture-obs' -> 'capture_obs'.
    (Very naive, but good enough for module names.)
    """
    s = name.replace("-", " ").replace(" ", "_")
    return s.lower()


def _to_kebab(name: str) -> str:
    """
    Convert 'Capture Obs', 'capture_obs' -> 'capture-obs'.
    """
    s = name.replace("_", " ").replace(" ", "-")
    return s.lower()


@dataclass(frozen=True)
class ModuleMeta:
    """
    Shared metadata / helpers for a Trivox module.

    You give it:
      - a `key`   -> canonical ID (ex: 'capture', 'watcher', 'color-grade')
      - actions   -> list/tuple of action strings
      - optional display title (otherwise derived)

    It gives you:
      - role (for preflights / checks)
      - command name
      - settings section name
      - main view id / title
      - normalized key forms (snake/kebab/title)
    """

    key: Role
    actions: Tuple[str, ...] = ()
    explicit_title: str | None = None

    def __post_init__(self):
        if not self.key:
            raise ValueError("ModuleMeta.key cannot be empty")

    # -------- identities --------

    @property
    def role(self) -> Role:
        """
        Role for preflights/checks.
        """
        return self.key

    @property
    def normalized_key(self) -> str:
        """
        Canonical normalized key (used for command/section names).
        For now it's just lowercased key.
        """
        return _normalize_key(self.key)

    @property
    def command_name(self) -> str:
        """CLI command name, ex: `capture`."""
        return self.normalized_key

    @property
    def settings_section(self) -> str:
        """Settings section / module key, ex: `capture`."""
        return self.normalized_key

    # -------- UI helpers --------

    @property
    def title(self) -> str:
        """Human-friendly module title."""
        return self.explicit_title or _to_title(self.normalized_key)

    @property
    def main_view_id(self) -> str:
        """Default main view id, ex: `capture_main`."""
        return f"{_to_snake(self.normalized_key)}_main"

    @property
    def main_view_title(self) -> str:
        """Default main view title (UI tab name)."""
        return self.title

    # -------- transforms --------

    @property
    def snake(self) -> str:
        return _to_snake(self.normalized_key)

    @property
    def kebab(self) -> str:
        return _to_kebab(self.normalized_key)

    @property
    def title_case(self) -> str:
        return _to_title(self.normalized_key)

    @property
    def camel(self) -> str:
        parts = self.snake.split("_")
        return parts[0] + "".join(p.capitalize() for p in parts[1:])

    @property
    def all_actions(self) -> Tuple[str, ...]:
        return self.actions

    def has_action(self, name: str) -> bool:
        return name in self.actions
