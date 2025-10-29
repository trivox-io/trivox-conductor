
from __future__ import annotations
from typing import Dict, Optional
from trivox_conductor.common.logger import logger
from trivox_conductor.core.contracts.watcher import WatcherAdapter
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.events import topics
from trivox_conductor.core.registry.watcher_registry import WatcherRegistry
from trivox_conductor.core.services.base_service import BaseService
from .settings import ReplaySettingsModel
from .correlate import SessionCorrelator


class ReplayWatcherService(BaseService[ReplaySettingsModel, WatcherAdapter]):
    """
    Subscribes/controls the WatcherAdapter and normalizes detections to events.
    """
    
    SECTION = "replay"
    MODEL = ReplaySettingsModel

    def __init__(self, registry: WatcherRegistry, settings: Dict, correlator: Optional[SessionCorrelator] = None):
        """
        :param registry: WatcherRegistry instance for adapter management.
        :type registry: WatcherRegistry
        
        :param settings: Configuration dictionary for ReplaySettingsModel.
        :type settings: Dict
        
        :param correlator: Optional SessionCorrelator for filename to session mapping.
        :type correlator: Optional[SessionCorrelator]
        """
        super().__init__(registry, settings)
        self._correlator = correlator or SessionCorrelator()

    def start(self, fallback_session: Optional[str] = None):
        """
        Start the active WatcherAdapter with configured settings.
        
        :param fallback_session: Optional fallback session ID for detections.
        :type fallback_session: Optional[str]
        """
        adapter = self._require_adapter()
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
