from __future__ import annotations

from typing import Any, Dict

from trivox_conductor.common.logger import logger
from trivox_conductor.core.events import topics
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.observers.base_observer import (
    BaseObserver,
    ObserverContext,
)
from trivox_conductor.core.observers.observers_registry import ObserverRegistry
from trivox_conductor.core.profiles.profile_models import PipelineProfile


class NotificationObserver(BaseObserver):
    """
    Pushes human-readable notifications to USER_NOTIFICATION
    based on profile.hooks.notify.
    """

    @classmethod
    def key(cls) -> str:
        return "notifications"

    def __init__(self, context: ObserverContext) -> None:
        super().__init__(context)
        self._profile: PipelineProfile = context.profile
        self._notify_cfg: Dict[str, Any] = {}
        if self._profile:
            self._notify_cfg = self._profile.hooks.get("notify", {}) or {}

    def attach(self) -> None:
        if not self._profile:
            logger.debug(
                "NotificationObserver: no active profile, skipping attach"
            )
            return
        if not self._notify_cfg:
            logger.debug(
                "NotificationObserver: no hooks.notify config, skipping attach"
            )
            return

        BUS.subscribe(topics.MANIFEST_UPDATED, self._on_manifest_updated)
        logger.debug(
            "NotificationObserver attached for profile %s", self._profile.key
        )

    def _emit(self, title: str, message: str, payload: Dict[str, Any]) -> None:
        # If you later have a ui_notifier in context, you can use it here.
        BUS.publish(
            topics.USER_NOTIFICATION,
            {
                "title": title,
                "message": message,
                **payload,
            },
        )

    def _on_manifest_updated(self, payload: Dict[str, Any]) -> None:
        logger.debug("NotificationObserver received MANIFEST_UPDATED event")
        event = payload.get("event")
        session_id = payload.get("session_id")

        if event == "capture.start" and self._notify_cfg.get(
            "capture_started", False
        ):
            self._emit(
                title="Capture started",
                message=f"Session {session_id} is now recording.",
                payload=payload,
            )
        elif event == "capture.stop" and self._notify_cfg.get(
            "capture_stopped", False
        ):
            self._emit(
                title="Capture stopped",
                message=f"Session {session_id} has stopped recording.",
                payload=payload,
            )


ObserverRegistry.register(NotificationObserver.key(), NotificationObserver)
