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
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
from trivox_conductor.core.services.base_service import BaseService

from .constants import CAPTURE_MODULE
from .settings import CaptureSettingsModel
from .state_store import CaptureStateStore


class CaptureService(BaseService[CaptureSettingsModel, CaptureAdapter]):
    """
    Orchestrates capture operations using the active CaptureAdapter.
    DIP: depends on CaptureRegistry (abstraction), not a concrete adapter.
    """

    SECTION = CAPTURE_MODULE.key
    MODEL = CaptureSettingsModel

    def __init__(
        self,
        registry: CaptureRegistry,
        settings: Dict,
        **kwargs,
    ):
        """
        :param registry: CaptureRegistry instance for adapter management.
        :type registry: CaptureRegistry
        """
        super().__init__(
            registry,
            settings,
            **kwargs,
        )

        self._store = CaptureStateStore()
        # Load persisted state if no in-memory state provided
        self._state = self._store.load()

    # ----- Queries -----
    def list_scenes(self) -> List[str]:
        """
        List available capture scenes from the active adapter.

        :return: List of scene names.
        :rtype: List[str]
        """
        adapter = self._get_configured_adapter(
            overrides=self._profile_overrides
        )
        return adapter.list_scenes() if adapter else []

    def list_profiles(self) -> List[str]:
        """
        List available capture profiles from the active adapter.

        :return: List of profile names.
        :rtype: List[str]
        """
        adapter = self._get_configured_adapter(
            overrides=self._profile_overrides
        )
        return adapter.list_profiles() if adapter else []

    # ----- Commands -----
    def start(self):
        """
        Start the capture process using the active adapter.

        :raises RuntimeError: If preflight checks fail or no adapter is configured.
        """
        logger.debug(
            "capture.start_initiated - session_id=%s", self._session_id
        )
        if not self._session_id:
            raise ValueError("session_id is required")

        # Build merged config (base settings + overrides + session_id)
        cfg_dict: dict[str, Any] = {"session_id": self._session_id}
        if self._profile_overrides:
            cfg_dict.update(self._profile_overrides)
        logger.debug(f"Capture config for start: {cfg_dict}")

        adapter = self._get_configured_adapter(overrides=cfg_dict)
        logger.debug("capture.adapter_configured - %s", adapter)

        # --- Preflight: collect failures and bail once, with a helpful message ---
        failures = run_preflights(
            role=CAPTURE_MODULE.key,
            profile=self._pipeline_profile,
            adapter=adapter,
            base_settings=cfg_dict,
            session_id=self._session_id,
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

        logger.info("capture.preflight_passed - proceeding to start")

        adapter.start_capture()
        self._state.start(self._session_id)
        self._store.save(self._state)
        logger.info("capture.started - session_id=%s", self._state.session_id)
        BUS.publish(
            topics.CAPTURE_STARTED,
            {
                "session_id": self._state.session_id,
                "profile_key": (
                    self._pipeline_profile.key
                    if self._pipeline_profile
                    else None
                ),
            },
        )

    def stop(self):
        """
        Stop the capture process using the active adapter.

        :raises RuntimeError: If no adapter is configured.
        """
        if not self._state.is_recording:
            self._state = self._store.load()

        adapter = self._get_configured_adapter(
            overrides=self._profile_overrides
        )
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

        # BUS.publish(
        #     topics.CAPTURE_STOPPED,
        #     {
        #         "session_id": self._state.session_id,
        #     },
        # )
