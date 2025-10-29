from __future__ import annotations
from dataclasses import asdict
from typing import Optional, List, Dict
from trivox_conductor.common.logger import logger
from trivox_conductor.core.contracts.capture import CaptureAdapter
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.events import topics
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
from trivox_conductor.core.services.base_service import BaseService

from .settings import CaptureSettingsModel
from .state import CaptureState
from .preflight import CapturePreflight


class CaptureService(BaseService[CaptureSettingsModel, CaptureAdapter]):
    """
    Orchestrates capture operations using the active CaptureAdapter.
    DIP: depends on CaptureRegistry (abstraction), not a concrete adapter.
    """

    SECTION = "capture"
    MODEL = CaptureSettingsModel

    def __init__(
        self,
        registry: CaptureRegistry,
        settings: Dict,
        preflight: Optional[CapturePreflight] = None,
        state: Optional[CaptureState] = None,
    ):
        """
        :param registry: CaptureRegistry instance for adapter management.
        :type registry: CaptureRegistry
        
        :param preflight: Optional CapturePreflight instance for checks.
        :type preflight: Optional[CapturePreflight]
        
        :param state: Optional CaptureState instance for runtime state.
        :type state: Optional[CaptureState]
        """
        super().__init__(registry, settings)
        self._preflight = preflight or CapturePreflight()
        self._state = state or CaptureState()

    # ----- Queries -----
    def list_scenes(self) -> List[str]:
        """
        List available capture scenes from the active adapter.
        
        :return: List of scene names.
        :rtype: List[str]
        """
        adapter = self._registry.get_active()
        return adapter.list_scenes() if adapter else []

    def list_profiles(self) -> List[str]:
        """
        List available capture profiles from the active adapter.
        
        :return: List of profile names.
        :rtype: List[str]
        """
        adapter = self._registry.get_active()
        return adapter.list_profiles() if adapter else []

    # ----- Commands -----
    def start(self, session_id: str, *, scene: Optional[str] = None, profile: Optional[str] = None):
        """
        Start the capture process using the active adapter.
        
        :param session_id: The session ID for the capture operation.
        :type session_id: str
        
        :param scene: Optional scene name to select before starting.
        :type scene: Optional[str]
        
        :param profile: Optional profile name to select before starting.
        :type profile: Optional[str]
        
        :raises RuntimeError: If preflight checks fail or no adapter is configured.
        """
        if not session_id:
            raise ValueError("session_id is required")
        if self._state.is_recording:
            logger.info(f"capture.already_recording - {self._state.session_id}")
            return

        ok, msg = self._preflight.check_obs_health()
        if not ok:
            logger.error(f"capture.preflight_failed - {msg}")
            raise RuntimeError(f"Preflight failed: {msg}")
        logger.debug(f"capture.preflight_ok - {msg}")

        adapter = self._require_adapter()
        cfg_dict = asdict(self._settings)
        cfg_dict["session_id"] = session_id
        adapter.configure(cfg_dict, {})

        try:
            chosen_scene = scene or self._settings.default_scene
            if chosen_scene:
                adapter.select_scene(chosen_scene)
            chosen_profile = profile or self._settings.default_profile
            if chosen_profile:
                adapter.select_profile(chosen_profile)
        except Exception as e:
            logger.error(f"capture.select_failed - {str(e)} - Scene: {chosen_scene}, Profile: {chosen_profile}")
            raise

        adapter.start_capture()
        self._state.start(session_id)
        BUS.publish(topics.MANIFEST_UPDATED, {"session_id": session_id, "event": "capture.start"})

    def stop(self):
        """
        Stop the capture process using the active adapter.

        :raises RuntimeError: If no adapter is configured.
        """
        if not self._state.is_recording:
            logger.info("Capture not recording; ignoring stop")
            return
        adapter = self._require_adapter()
        adapter.stop_capture()
        self._state.stop()
