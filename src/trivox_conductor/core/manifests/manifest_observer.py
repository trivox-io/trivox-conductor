from __future__ import annotations

from typing import Any, Dict

from trivox_conductor.common.logger import logger
from trivox_conductor.core.events import topics
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.observers.observer_base import (
    BaseObserver,
    ObserverContext,
)
from trivox_conductor.core.observers.observers_registry import ObserverRegistry

from .manifest_service import ManifestService


class ManifestObserver(BaseObserver):
    """
    Observer that reacts to CAPTURE_STARTED events and writes them
    into SessionManifest via ManifestService.
    """

    @classmethod
    def key(cls) -> str:
        return "manifest"

    def __init__(self, context: ObserverContext) -> None:
        super().__init__(context)
        logger.debug("Initializing ManifestObserver")
        self._service: ManifestService = context.manifest_service

    def attach(self) -> None:
        if not self._service:
            logger.debug(
                "ManifestObserver: no manifest_service in context, skipping attach"
            )
            return
        logger.debug(
            "ManifestObserver subscribing to topic %r", topics.CAPTURE_STARTED
        )
        # BUS.subscribe(topics.CAPTURE_STARTED, self._on_capture_started)
        # BUS.subscribe(topics.CAPTURE_STOPPED, self._on_capture_stopped)
        logger.debug("ManifestObserver attached")

    def _on_capture_started(self, payload: Dict[str, Any]) -> None:
        logger.debug("ManifestObserver received CAPTURE_STARTED event")
        session_id = payload.pop("session_id")
        profile_key = payload.pop("profile_key", None)
        event = topics.CAPTURE_STARTED

        if not session_id:
            logger.debug("manifest.observer.skip - missing session_id/event")
            return

        # lazily call into ManifestService
        self._service.start_session(session_id, profile_key)
        self._service.append_event(session_id, event, payload)

    def _on_capture_stopped(self, payload: Dict[str, Any]) -> None:
        logger.debug("ManifestObserver received CAPTURE_STOPPED event")
        session_id = payload.pop("session_id")
        event = topics.CAPTURE_STOPPED

        if not session_id:
            logger.debug("manifest.observer.skip - missing session_id/event")
            return

        self._service.append_event(session_id, event, payload)
        self._service.close_session(session_id)


# register in the registry
ObserverRegistry.register(ManifestObserver.key(), ManifestObserver)
