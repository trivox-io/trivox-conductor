"""
Capture Command Processor
=========================

Implements the runtime behavior for the ``capture`` CLI command. Translates parsed
arguments into service calls, including optional connection overrides and selection
preferences.

Responsibilities
----------------
- Build a :class:`~trivox_conductor.modules.capture.services.CaptureService`.
- Pass through **overrides** (``host``, ``port``, ``password``, ``request_timeout_sec``).
- Invoke actions: ``start``, ``stop``, ``list_scenes``, ``list_profiles``.
- Log a concise audit line with action and result.

Design notes
------------
- The processor is intentionally thin: it performs no OBS I/O itself.
- ``_overrides`` includes only user-provided values to avoid clobbering base settings.
"""

from __future__ import annotations

from trivox_conductor.common.base_processor import (
    TrivoxCaptureCommandProcessor,
)
from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
from trivox_conductor.core.manifests.manifest_service import ManifestService
from trivox_conductor.core.observers.base_observer import ObserverContext
from trivox_conductor.core.observers.bootstrap import attach_all_observers
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
from trivox_conductor.core.registry.watcher_registry import WatcherRegistry
from trivox_conductor.core.session.session_manager import SessionManager
from trivox_conductor.modules.watcher.services import WatcherService

from .services import CaptureService


class CaptureCommandProcessor(TrivoxCaptureCommandProcessor):
    """
    Command processor for Capture module commands.
    """

    ROLE = "capture"
    SERVICE_CLS = CaptureService
    ACTION_MAP = {
        "start": "start",
        "stop": "stop",
        "list_scenes": "list_scenes",
        "list_profiles": "list_profiles",
    }
    _session_id: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Optional selections
        self._cli_session_id: str = self._kwargs.get("session_id", None)
        self._scene = self._kwargs.get("scene")
        self._profile = self._kwargs.get("profile")

        # Connection overrides (only include if provided)
        overrides = {
            k: v
            for k, v in {
                "host": self._kwargs.get("host"),
                "port": self._kwargs.get("port"),
                "password": self._kwargs.get("password"),
                "request_timeout_sec": self._kwargs.get("request_timeout_sec"),
            }.items()
            if v is not None
        }
        self.set_pipeline_profile(overrides)
        logger.debug("Setup observers context")
        manifest_service = ManifestService(
            # optionally pass custom root: Path("..."),
        )
        watcher_service = WatcherService(
            WatcherRegistry, settings=settings.get("watcher", {})
        )

        ctx = ObserverContext(
            profile_key=self._pipeline_profile_key,
            profile=self._pipeline_profile,
            manifest_service=manifest_service,
            watcher_service=watcher_service,
        )

        attach_all_observers(ctx)

    def build_service(self):
        return CaptureService(CaptureRegistry, settings)

    def build_call_kwargs(self, action: str) -> dict:
        if action == "start":
            return {
                "session_id": self._session_id,
                "scene": self._scene,
                "profile": self._profile,
                "overrides": self._overrides,
                "pipeline_profile": self._pipeline_profile,
            }
        if action == "stop":
            return {"overrides": self._overrides}
        if action in ("list_scenes", "list_profiles"):
            return {"overrides": self._overrides}
        return {}

    def run(self):
        # Implement the command processing logic here
        logger.debug("Running CaptureCommandProcessor")
        session = SessionManager.ensure_session(
            session_id=self._cli_session_id,
            label=f"{self._pipeline_profile_key or 'capture'}",
        )
        self._session_id = session.id
        return super().run()
