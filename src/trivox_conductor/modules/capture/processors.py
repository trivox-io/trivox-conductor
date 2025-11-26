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
from trivox_conductor.core.observers.bootstrap import attach_all_observers
from trivox_conductor.core.observers.observer_base import ObserverContext
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
from trivox_conductor.core.trivox_context import trivox_context

from .constants import CAPTURE_MODULE
from .services import CaptureService


class CaptureCommandProcessor(TrivoxCaptureCommandProcessor):
    """
    Command processor for Capture module commands.
    """

    ROLE = CAPTURE_MODULE.role
    SERVICE_CLS = CaptureService
    ACTION_MAP = {k: k for k in CAPTURE_MODULE.actions}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.debug("Setup observers context")

        # TODO: This context is basically the same as trivox_context; unify them
        # Also, attach observers in the parent class
        ctx = ObserverContext(
            session_id=self._session_id,
            profile=trivox_context.profile,
            profile_overrides=trivox_context.overrides,
        )

        attach_all_observers(ctx)

    def build_service(self):
        return CaptureService(
            CaptureRegistry,
            settings,
            session_id=self._session_id,
            pipeline_profile=trivox_context.profile,
            profile_overrides=trivox_context.overrides,
        )

    def run(self):
        # Implement the command processing logic here
        logger.debug("Running CaptureCommandProcessor")
        return super().run()
