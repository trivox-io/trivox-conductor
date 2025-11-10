from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from trivox_conductor.core.profiles.profile_models import PipelineProfile


@dataclass
class ObserverContext:
    """
    Shared runtime context for observers.

    Fill in what you actually have in the process that’s hosting observers
    (GUI/daemon/etc.). Everything is optional so observers can degrade gracefully.
    """

    profile_key: Optional[str] = None
    profile: Optional[PipelineProfile] = None

    # core services (optional)
    manifest_service: Any = None  # e.g. ManifestService
    watcher_service: Any = None  # e.g. WatcherService
    job_orchestrator: Any = None  # e.g. JobOrchestrator
    ui_notifier: Any = None  # e.g. GUI bridge, CLI printer, etc.


class BaseObserver(ABC):
    """
    Base class for all event observers.

    - Constructed with an ObserverContext
    - `attach()` wires BUS subscriptions
    """

    def __init__(self, context: ObserverContext) -> None:
        self._ctx = context

    @classmethod
    def key(cls) -> str:
        """
        Logical key. By default it's the lowercased class name,
        but you can override for nicer names.
        """
        return cls.__name__.lower()

    @abstractmethod
    def attach(self) -> None:
        """
        Wire BUS subscriptions. Called once during bootstrap.
        """
        ...
