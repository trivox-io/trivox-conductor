from __future__ import annotations
from typing import Dict, List
from .preflight_types import PreflightCheck, Role


class PreflightRegistry:
    _checks: Dict[Role, Dict[str, PreflightCheck]] = {
        "capture": {},
        "watcher": {},
        "mux": {},
        "color": {},
        "uploader": {},
        "notifier": {},
        "ai": {},
    }

    @classmethod
    def register(cls, role: Role, check: PreflightCheck) -> None:
        cls._checks[role][check.id] = check

    @classmethod
    def get(cls, role: Role, id: str) -> PreflightCheck:
        try:
            return cls._checks[role][id]
        except KeyError as e:
            raise KeyError(f"Unknown preflight '{id}' for role '{role}'") from e

    @classmethod
    def list_for_role(cls, role: Role) -> List[PreflightCheck]:
        return list(cls._checks[role].values())
