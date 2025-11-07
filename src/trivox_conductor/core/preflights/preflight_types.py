"""
Preflight check types and protocols.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Mapping, Optional, Protocol

Role = Literal[
    "capture", "watcher", "mux", "color", "uploader", "notifier", "ai"
]


@dataclass
class PreflightContext:
    """
    Context provided to preflight checks.

    :cvar  role: The adapter role (e.g., 'capture', 'uploader').
    :cvar  settings: Merged settings for the preflight check.
    :cvar  adapter: The adapter instance being checked.
    :cvar  session_id: Optional session identifier.
    :cvar  profile_key: Optional profile key for identification.
    """

    role: Role
    settings: Mapping[str, Any]  # merged settings+overrides+params
    adapter: Any  # CaptureAdapter / WatcherAdapter / ...
    session_id: Optional[str] = None
    profile_key: Optional[str] = None


@dataclass
class PreflightFailure:
    """
    Represents a failure from a preflight check.

    :cvar id: The unique identifier of the preflight check.
    :cvar message: Description of the failure.
    :cvar required: Whether this preflight was required.
    """

    id: str
    message: str
    required: bool


class PreflightCheck(Protocol):
    """
    Protocol for preflight check implementations.

    :cvar id: Unique identifier for the preflight check.
    :cvar role: The adapter role this check is for.
    :cvar default_required: Whether this check is required by default.
    :cvar adapter_name: Optional specific adapter name this check applies to.
    """

    id: str
    role: Role
    default_required: bool
    adapter_name: Optional[
        str
    ]  # only run for this adapter.meta["name"], or None for any

    def __call__(self, ctx: PreflightContext) -> Optional[PreflightFailure]:
        """
        Execute the preflight check.

        :param ctx: The preflight context.
        :type ctx: PreflightContext

        :return: A PreflightFailure if the check fails, or None if it passes.
        :rtype: Optional[PreflightFailure]
        """
