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

from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
from trivox_conductor.common.base_processor import TrivoxCaptureCommandProcessor
from trivox_conductor.core.registry.capture_registry import CaptureRegistry

from .services import CaptureService


class CaptureCommandProcessor(TrivoxCaptureCommandProcessor):
    """
    Command processor for Capture module commands.
    """
    
    def __init__(self, **kwargs):
        self._action: str = kwargs.get("action", "")
        self._session_id: str = kwargs.get("session_id", None)

        # Optional selections
        self._scene = kwargs.get("scene")
        self._profile = kwargs.get("profile")

        # Connection overrides (only include if provided)
        self._overrides = {
            k: v for k, v in {
                "host": kwargs.get("host"),
                "port": kwargs.get("port"),
                "password": kwargs.get("password"),
                "request_timeout_sec": kwargs.get("request_timeout_sec"),
            }.items() if v is not None
        }
    
    def run(self):
        # Implement the command processing logic here
        logger.debug("Running CaptureCommandProcessor")

        svc = CaptureService(CaptureRegistry, settings)

        ops = {
            "start": lambda: svc.start(
                self._session_id,
                scene=self._scene,
                profile=self._profile,
                overrides=self._overrides
            ),
            "stop": lambda: svc.stop(overrides=self._overrides),
            "list_scenes": lambda: svc.list_scenes(overrides=self._overrides),
            "list_profiles": lambda: svc.list_profiles(overrides=self._overrides),
        }
        try:
            fn = ops[self._action]
        except KeyError as e:
            raise ValueError(f"Unknown action: {self._action}") from e

        result = fn()
        logger.info(f"capture.action - {self._action} - {result}")
        return result
