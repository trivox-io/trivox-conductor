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
from typing import Any, Dict, List, Mapping, Optional

from trivox_conductor.common.logger import logger
from trivox_conductor.core.contracts.capture import CaptureAdapter
from trivox_conductor.core.events import topics
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.preflights.preflight_engine import run_preflights
from trivox_conductor.core.profiles.profile_models import PipelineProfile
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
from trivox_conductor.core.services.base_service import BaseService

from .preflight import CapturePreflight
from .settings import CaptureSettingsModel
from .state import CaptureState
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
    def list_scenes(
        self, *, overrides: Optional[Mapping[str, Any]] = None
    ) -> List[str]:
        """
        List available capture scenes from the active adapter.

        :return: List of scene names.
        :rtype: List[str]
        """
        adapter = self._get_configured_adapter(overrides=overrides)
        return adapter.list_scenes() if adapter else []

    def list_profiles(
        self, *, overrides: Optional[Mapping[str, Any]] = None
    ) -> List[str]:
        """
        List available capture profiles from the active adapter.

        :return: List of profile names.
        :rtype: List[str]
        """
        adapter = self._get_configured_adapter(overrides=overrides)
        return adapter.list_profiles() if adapter else []

    # ----- Commands -----
    def start(
        self,
        session_id: str,
        *,
        scene: Optional[str] = None,
        profile: Optional[str] = None,
        overrides: Optional[Mapping[str, Any]] = None,
        pipeline_profile: Optional[PipelineProfile] = None,
    ):
        """
        Start the capture process using the active adapter.

        :param session_id: The session ID for the capture operation.
        :type session_id: str

        :param scene: Optional scene name to select before starting.
        :type scene: Optional[str]

        :param profile: Optional profile name to select before starting.
        :type profile: Optional[str]

        :param overrides: Optional mapping of connection overrides.
        :type overrides: Optional[Mapping[str, Any]]

        :raises RuntimeError: If preflight checks fail or no adapter is configured.
        """
        if not session_id:
            raise ValueError("session_id is required")

        # Build merged config (base settings + overrides + session_id)
        cfg_dict = asdict(self._settings)
        cfg_dict["session_id"] = session_id
        if overrides:
            cfg_dict.update(overrides)

        adapter = self._get_configured_adapter(overrides=cfg_dict)

        # --- Preflight: collect failures and bail once, with a helpful message ---
        failures = run_preflights(
            role="capture",
            profile=pipeline_profile,
            adapter=adapter,
            base_settings=cfg_dict,
            session_id=session_id,
        )

        required_failures = [f for f in failures if f.required]
        soft_failures = [f for f in failures if not f.required]

        if required_failures:
            msg = "; ".join(f"{f.id}: {f.message}" for f in required_failures)
            logger.error("capture.preflight_failed - %s", msg)
            raise RuntimeError("Preflight failed: " + msg)

        for f in soft_failures:
            logger.warning(
                "capture.preflight_soft_fail - %s: %s", f.id, f.message
            )

        # You can keep this before or after preflights; I’m leaving it here as you had it
        if self._state.is_recording:
            logger.info(
                "capture.already_recording - %s", self._state.session_id
            )
            return

        # --- Safe to proceed: select scene/profile, then start ---
        try:
            # Prefer explicit CLI args, then pipeline/config overrides, then model defaults
            chosen_scene = (
                scene
                or cfg_dict.get("default_scene")
                or getattr(self._settings, "default_scene", None)
            )
            chosen_profile = (
                profile
                or cfg_dict.get("default_profile")
                or getattr(self._settings, "default_profile", None)
            )

            logger.debug(
                "capture.selecting - scene=%r (arg=%r, cfg=%r), "
                "profile=%r (arg=%r, cfg=%r)",
                chosen_scene,
                scene,
                cfg_dict.get("default_scene"),
                chosen_profile,
                profile,
                cfg_dict.get("default_profile"),
            )

            if chosen_scene:
                adapter.select_scene(chosen_scene)
            if chosen_profile:
                adapter.select_profile(chosen_profile)

        except Exception as e:
            logger.error(
                "capture.select_failed - %s - Scene: %r, Profile: %r",
                str(e),
                chosen_scene,
                chosen_profile,
            )
            raise

        adapter.start_capture()
        self._state.start(session_id)
        self._store.save(self._state)
        logger.info("capture.started - session_id=%s", self._state.session_id)
        BUS.publish(
            topics.MANIFEST_UPDATED,
            {
                "session_id": session_id,
                "event": "capture.start",
                "profile_key": (
                    pipeline_profile.key if pipeline_profile else None
                ),
            },
        )

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
            logger.info(
                "capture.stop_ignored - not recording (memory & adapter)"
            )
            return

        # Try to stop anyway; StopRecord is idempotent on OBS side.
        adapter.stop_capture()
        self._state.stop()
        self._store.save(self._state)

        BUS.publish(
            topics.MANIFEST_UPDATED,
            {
                "session_id": self._state.session_id,
                "event": "capture.stop",
                # we don’t know profile_key here yet, so leave None or resolve later
                "profile_key": None,
            },
        )
