"""
Core registry module for managing endpoint role registrations.
"""

from __future__ import annotations

from .capture_registry import CaptureRegistry
from .role_registries import ROLE_REGISTRIES

__all__ = [
    "ROLE_REGISTRIES",
    "CaptureRegistry",
]
