from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
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
from trivox_conductor.modules.watcher.registry import WatcherRegistry
from trivox_conductor.modules.watcher.services import WatcherService


class WatcherAutoStartObserver(BaseObserver):
    """
    Starts the watcher when capture starts, if enabled in profile.hooks.watcher.

    We accept a `start_watcher(session_id: Optional[str])` callable so this
    can be wired to a WatcherService instance in GUI or a long-running daemon.
    """

    @classmethod
    def key(cls) -> str:
        return "autostart"

    def __init__(self, context: ObserverContext) -> None:
        super().__init__(context)
        self._profile: PipelineProfile = context.profile
        self._watcher_service = WatcherService(
            WatcherRegistry,
            settings,
            session_id=context.session_id,
            pipeline_profile=context.profile,
            profile_overrides=context.profile_overrides,
        )

        self._cfg = {}
        if self._profile:
            self._cfg = self._profile.hooks.get("watcher", {}) or {}
        self._enabled = bool(self._cfg.get("autostart_watcher", False))

    def attach(self) -> None:
        if not self._profile:
            logger.warning("no active profile, skipping attach")
            return
        if not self._watcher_service:
            logger.warning("no watcher_service in context, skipping attach")
            return
        if not self._enabled:
            logger.warning(
                "disabled for profile %s",
                self._profile.key,
            )
            return

        BUS.subscribe(topics.CAPTURE_STARTED, self._on_capture_started)
        logger.debug(
            "WatcherAutoStartObserver attached for profile %s",
            self._profile.key,
        )

    def _on_capture_started(self, payload: Dict[str, Any]) -> None:
        logger.debug(
            f"WatcherAutoStartObserver received CAPTURE_STARTED event {payload}"
        )
        session_id: Optional[str] = payload.get("session_id")
        logger.info(
            "starting watcher for session %s",
            session_id,
        )
        logger.debug(f"Profile adapters: {self._profile.adapters.values()}")
        watch_adapter: Adapter = next(
            adapter
            for adapter in self._profile.adapters.values()
            if adapter.role == "watcher"
        )
        logger.debug(
            "Using watcher adapter %s with overrides %s",
            watch_adapter.name,
            watch_adapter.overrides,
        )
        # watcher_service.start can accept Optional[str]
        self._watcher_service.start()


ObserverRegistry.register(
    WatcherAutoStartObserver.key(), WatcherAutoStartObserver
)
