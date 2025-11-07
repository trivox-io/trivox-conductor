from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Mapping, Optional

from trivox_conductor.common.logger import logger
from trivox_conductor.core.contracts.watcher import WatcherAdapter
from trivox_conductor.core.events import topics
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.registry.watcher_registry import WatcherRegistry
from trivox_conductor.core.services.base_service import BaseService

from .correlate import SessionCorrelator
from .settings import WatcherSettingsModel


class WatcherService(BaseService[WatcherSettingsModel, WatcherAdapter]):
    """
    Subscribes/controls the WatcherAdapter and normalizes detections to events.
    """

    SECTION = "watcher"
    MODEL = WatcherSettingsModel

    def __init__(
        self,
        registry: WatcherRegistry,
        settings: Dict,
        correlator: Optional[SessionCorrelator] = None,
    ):
        """
        :param registry: WatcherRegistry instance for adapter management.
        :type registry: WatcherRegistry

        :param settings: Configuration dictionary for WatcherSettingsModel.
        :type settings: Dict

        :param correlator: Optional SessionCorrelator for filename to session mapping.
        :type correlator: Optional[SessionCorrelator]
        """
        super().__init__(registry, settings)
        self._correlator = correlator or SessionCorrelator()

    def start(
        self,
        session_id: Optional[str] = None,
        overrides: Optional[Mapping[str, Any]] = None,
    ):
        """
        Start the active WatcherAdapter with configured settings.

        :param session_id: Optional fallback session ID for detections.
        :type session_id: Optional[str]
        """
        if not session_id:
            raise ValueError("session_id is required")

        cfg_dict = asdict(self._settings)
        cfg_dict["session_id"] = session_id
        if overrides:
            cfg_dict.update(overrides)
        logger.debug(
            f"Applying overrides to WatcherAdapter config: {cfg_dict}"
        )
        adapter = self._get_configured_adapter(overrides=cfg_dict)
        self._configure_adapter(adapter)
        logger.debug(f"Path to watch: {self._settings.watch_path}")
        adapter.set_watch_path(self._settings.watch_path)
        adapter.start()
        # Real adapter would emit events; here we keep service ready for extra rules.

    def stop(self):
        """
        Stop the active WatcherAdapter.
        """
        adapter = self._require_adapter()
        adapter.stop()

    def on_raw_detect(self, payload: Dict) -> None:
        """
        Optional hook to post-process adapter detection (stability, correlation).

        :param payload: Raw detection payload from the adapter.
        :type payload: Dict
        """
        path: str = payload["path"]
        session = self._correlator.correlate(path, fallback_session=None)
        normalized = dict(payload)
        normalized["session_id"] = session
        BUS.publish(topics.REPLAY_RENDER_DETECTED, normalized)
