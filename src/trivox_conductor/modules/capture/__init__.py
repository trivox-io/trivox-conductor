"""
Capture Module
==============

Entry point package for the "capture" feature-set: CLI command/processor,
service orchestration, runtime state, persistence, preflight checks, and a
plugin-backed adapter (e.g., OBS).

Subpackages / Files
-------------------
- ``commands``: CLI surface for ``capture``.
- ``processors``: bridges CLI args to service calls.
- ``services``: orchestration + state handling.
- ``state`` / ``state_store``: minimal session state + JSON persistence.
- ``preflight``: health checks before starting.
- ``settings``: defaults and registry wiring for the ``capture`` section.

Adapters live under ``trivox_conductor.plugins`` and are discovered/registered
by the application bootstrap.
"""

from .commands import CaptureCommand
from .settings import CaptureSettings
from .preflights import DiskSpaceCheck, WindowForegroundCheck

__all__ = [
    "CaptureCommand",
    "CaptureSettings",
    "DiskSpaceCheck",
    "WindowForegroundCheck",
]
