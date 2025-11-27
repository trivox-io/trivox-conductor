from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Mapping, Optional

from trivox_conductor.common.logger import logger
from trivox_conductor.core.events import topics
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.services.base_service import BaseService

from .contracts import WatcherAdapter
from .correlate import SessionCorrelator
from .registry import WatcherRegistry
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
        **kwargs,
    ):
        """
        :param registry: WatcherRegistry instance for adapter management.
        :type registry: WatcherRegistry

        :param settings: Configuration dictionary for WatcherSettingsModel.
        :type settings: Dict

        :param correlator: Optional SessionCorrelator for filename to session mapping.
        :type correlator: Optional[SessionCorrelator]
        """
        super().__init__(registry, settings, **kwargs)
        self._correlator = kwargs.get("correlator") or SessionCorrelator()

    def start(
        self,
    ):
        """
        Start the active WatcherAdapter with configured settings.
        """
        if not self._session_id:
            raise ValueError("session_id is required")

        cfg_dict = asdict(self._settings)
        cfg_dict["session_id"] = self._session_id
        if self._profile_overrides:
            cfg_dict.update(self._profile_overrides)
        logger.debug(
            f"Applying overrides to WatcherAdapter config: {cfg_dict}"
        )
        adapter = self._get_configured_adapter(overrides=cfg_dict)
        self._configure_adapter(adapter)
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
