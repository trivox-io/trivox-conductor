from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from trivox_conductor.common.logger import logger
from trivox_conductor.core.events import topics
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.observers.observer_base import (
    BaseObserver,
    ObserverContext,
)
from trivox_conductor.core.observers.observers_registry import ObserverRegistry
from trivox_conductor.core.profiles.profile_models import (
    Adapter,
    PipelineProfile,
)


class WatcherAutoStartObserver(BaseObserver):
    """
    Starts the watcher when capture starts, if enabled in profile.hooks.watcher.

    We accept a `start_watcher(session_id: Optional[str])` callable so this
    can be wired to a WatcherService instance in GUI or a long-running daemon.
    """

    @classmethod
    def key(cls) -> str:
        return "watcher_autostart"

    def __init__(self, context: ObserverContext) -> None:
        super().__init__(context)
        self._profile: PipelineProfile = context.profile
        self._watcher_service = context.watcher_service

        self._cfg = {}
        if self._profile:
            self._cfg = self._profile.hooks.get("watcher", {}) or {}
        self._enabled = bool(self._cfg.get("start_on_capture_started", False))

    def attach(self) -> None:
        if not self._profile:
            logger.debug(
                "WatcherAutoStartObserver: no active profile, skipping attach"
            )
            return
        if not self._watcher_service:
            logger.debug(
                "WatcherAutoStartObserver: no watcher_service in context, skipping attach"
            )
            return
        if not self._enabled:
            logger.debug(
                "WatcherAutoStartObserver: disabled for profile %s",
                self._profile.key,
            )
            return

        # BUS.subscribe(topics.CAPTURE_STARTED, self._on_capture_started)
        logger.debug(
            "WatcherAutoStartObserver attached for profile %s",
            self._profile.key,
        )

    def _on_capture_started(self, payload: Dict[str, Any]) -> None:
        logger.debug("WatcherAutoStartObserver received CAPTURE_STARTED event")
        if payload.get("event") != "capture.started":
            return
        session_id: Optional[str] = payload.get("session_id")
        logger.info(
            "WatcherAutoStartObserver: starting watcher for session %s",
            session_id,
        )
        watch_adapter: Adapter = next(
            adapter
            for adapter in self._profile.adapters.values()
            if adapter.role == "watcher"
        )
        # watcher_service.start can accept Optional[str]
        self._watcher_service.start(
            session_id=session_id, overrides=watch_adapter.overrides
        )


ObserverRegistry.register(
    WatcherAutoStartObserver.key(), WatcherAutoStartObserver
)
