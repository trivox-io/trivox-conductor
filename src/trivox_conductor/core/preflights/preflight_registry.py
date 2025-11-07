"""
Preflight registry to manage preflight checks for different roles.
"""

from __future__ import annotations

from typing import Dict, List

from .preflight_types import PreflightCheck, Role


class PreflightRegistry:
    """
    Registry for preflight checks categorized by adapter roles.

    :cvar _checks: Mapping of roles to their registered preflight checks.
    """

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
    def register(cls, role: Role, check: PreflightCheck):
        """
        Register a preflight check for a specific role.

        :param role: The adapter role (e.g., 'capture', 'uploader').
        :type role: Role

        :param check: The preflight check instance to register.
        :type check: PreflightCheck
        """
        cls._checks[role][check.id] = check

    @classmethod
    def get(cls, role: Role, id: str) -> PreflightCheck:
        """
        Retrieve a registered preflight check by role and ID.

        :param role: The adapter role (e.g., 'capture', 'uploader').
        :type role: Role

        :param id: The unique identifier of the preflight check.
        :type id: str

        :return: The corresponding preflight check instance.
        :rtype: PreflightCheck
        """
        try:
            return cls._checks[role][id]
        except KeyError as e:
            raise KeyError(
                f"Unknown preflight '{id}' for role '{role}'"
            ) from e

    @classmethod
    def list_for_role(cls, role: Role) -> List[PreflightCheck]:
        """
        List all registered preflight checks for a specific role.

        :param role: The adapter role (e.g., 'capture', 'uploader').
        :type role: Role
        """
        return list(cls._checks[role].values())
