"""
Capture Service
===============

High-level orchestration for capture operations using the active
:class:`~trivox_conductor.core.contracts.capture.CaptureAdapter`. Encapsulates
preflight checks, adapter configuration, and state persistence.

Features
--------
- **Typed config** via :class:`CaptureSettingsModel` (``SECTION='capture'``).
- **Preflight**: lightweight checks (adapter health, etc.) before starting.
- **Overrides**: merge CLI-supplied connection params into adapter config.
- **State persistence**: stores minimal runtime state to survive new CLI invocations.
- **Events**: publishes bus notifications on start/stop.

Public API
----------
- ``list_scenes(overrides=None) -> List[str]``
- ``list_profiles(overrides=None) -> List[str]``
- ``start(session_id, scene=None, profile=None, overrides=None)``
- ``stop(overrides=None)``

Error model
-----------
- Raises ``RuntimeError`` if preflight fails or no adapter is configured.
- Adapter-specific failures are surfaced as ``RuntimeError`` with actionable messages.

Separation of concerns
----------------------
All external I/O is delegated to the adapter; this service composes policy and flow.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Optional, List, Dict, Mapping, Any
from trivox_conductor.common.logger import logger
from trivox_conductor.core.contracts.capture import CaptureAdapter
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.events import topics
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
from trivox_conductor.core.services.base_service import BaseService

from .settings import CaptureSettingsModel
from .state import CaptureState
from .preflight import CapturePreflight
from .state_store import CaptureStateStore


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
        self._store = CaptureStateStore()
        # Load persisted state if no in-memory state provided
        self._state = state or self._store.load()
    
    # ----- Queries -----
    def list_scenes(self, *, overrides: Optional[Mapping[str, Any]] = None) -> List[str]:
        """
        List available capture scenes from the active adapter.
        
        :return: List of scene names.
        :rtype: List[str]
        """
        adapter = self._get_configured_adapter(overrides=overrides)
        return adapter.list_scenes() if adapter else []

    def list_profiles(self, *, overrides: Optional[Mapping[str, Any]] = None) -> List[str]:
        """
        List available capture profiles from the active adapter.
        
        :return: List of profile names.
        :rtype: List[str]
        """
        adapter = self._get_configured_adapter(overrides=overrides)
        return adapter.list_profiles() if adapter else []

    # ----- Commands -----
    def start(self, session_id: str, *, scene: Optional[str] = None, profile: Optional[str] = None, overrides: Optional[Mapping[str, Any]] = None):
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
        
        cfg_dict = asdict(self._settings)
        cfg_dict["session_id"] = session_id
        if overrides:
            cfg_dict.update(overrides)
        adapter = self._get_configured_adapter(overrides=cfg_dict)
        # --- Preflight: collect failures and bail once, with a helpful message ---
        failures: list[str] = []

        # 1) OBS health
        ok, msg = self._preflight.check_obs_health(adapter)
        if not ok:
            failures.append(f"obs: {msg}")
        else:
            logger.debug(f"capture.preflight_ok - obs: {msg}")

        # 2) Disk space (best effort). Resolve record dir:
        #    priority: CLI override 'record_dir' -> adapter.get_record_directory() -> skip
        record_dir: Optional[str] = None
        if overrides and "record_dir" in overrides and overrides["record_dir"]:
            record_dir = str(overrides["record_dir"])
        else:
            get_dir = getattr(adapter, "get_record_directory", None)
            if callable(get_dir):
                try:
                    record_dir = get_dir()  # expect a str
                except Exception as e:
                    logger.debug(f"capture.preflight_warn - get_record_directory failed: {e}")

        if record_dir:
            min_gb = float(cfg_dict.get("min_record_free_gb", 5.0))
            ok, msg = self._preflight.check_disk_space(record_dir, min_gb=min_gb)
            if not ok:
                failures.append(f"disk: {msg}")
            else:
                logger.debug(f"capture.preflight_ok - disk: {msg}")
        else:
            logger.debug("capture.preflight_skip - disk: record directory unknown (override 'record_dir' to enable check)")

        # 3) Minecraft foreground (optional strictness; default False)
        enforce_mc_fg = bool(cfg_dict.get("enforce_mc_foreground", False))
        if enforce_mc_fg:
            ok, msg = self._preflight.check_minecraft_foreground()
            if not ok:
                failures.append(f"minecraft: {msg}")
            else:
                logger.debug(f"capture.preflight_ok - minecraft: {msg}")
        else:
            logger.debug("capture.preflight_skip - minecraft: enforcement disabled")

        if failures:
            error_msg = "Preflight failed: " + "; ".join(failures)
            logger.error(f"capture.preflight_failed - {error_msg}")
            raise RuntimeError(error_msg)

        # --- Safe to proceed: select scene/profile, then start ---
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
        self._store.save(self._state)
        BUS.publish(topics.MANIFEST_UPDATED, {"session_id": session_id, "event": "capture.start"})

    def stop(self, *, overrides: Optional[Mapping[str, Any]] = None):
        """
        Stop the capture process using the active adapter.

        :raises RuntimeError: If no adapter is configured.
        """
        if not self._state.is_recording:
            self._state = self._store.load()

        adapter = self._get_configured_adapter(overrides=overrides)
        # Adapter is the source of truth
        is_recording_now = False
        try:
            is_recording_now = adapter.is_recording()
        except Exception as e:
            logger.warning(f"capture.adapter_is_recording_probe_failed: {e}")

        if not (self._state.is_recording or is_recording_now):
            logger.info("capture.stop_ignored - not recording (memory & adapter)")
            return

        # Try to stop anyway; StopRecord is idempotent on OBS side.
        adapter.stop_capture()
        self._state.stop()
        self._store.save(self._state)
