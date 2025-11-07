from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any, Protocol, Optional, Literal

Role = Literal["capture", "watcher", "mux", "color", "uploader", "notifier", "ai"]


@dataclass
class PreflightContext:
    role: Role
    settings: Mapping[str, Any] # merged settings+overrides+params
    adapter: Any # CaptureAdapter / WatcherAdapter / ...
    session_id: Optional[str] = None
    profile_key: Optional[str] = None


@dataclass
class PreflightFailure:
    id: str
    message: str
    required: bool


class PreflightCheck(Protocol):
    id: str
    role: Role
    default_required: bool
    adapter_name: Optional[str]     # only run for this adapter.meta["name"], or None for any

    def __call__(self, ctx: PreflightContext) -> Optional[PreflightFailure]:
        ...
