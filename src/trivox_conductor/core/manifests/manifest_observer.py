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
    Observer that reacts to MANIFEST_UPDATED events and writes them
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
            "ManifestObserver subscribing to topic %r", topics.MANIFEST_UPDATED
        )
        BUS.subscribe(topics.MANIFEST_UPDATED, self._on_manifest_updated)
        logger.debug("ManifestObserver attached")

    def _on_manifest_updated(self, payload: Dict[str, Any]) -> None:
        logger.debug("ManifestObserver received MANIFEST_UPDATED event")
        session_id = payload.get("session_id")
        event = payload.get("event")
        profile_key = payload.get("profile_key")

        if not session_id or not event:
            logger.debug("manifest.observer.skip - missing session_id/event")
            return

        # lazily call into ManifestService
        if event == "capture.start":
            self._service.start_session(session_id, profile_key)

        self._service.append_event(session_id, event, payload)

        if event == "capture.stop":
            self._service.close_session(session_id)


# register in the registry
ObserverRegistry.register(ManifestObserver.key(), ManifestObserver)
