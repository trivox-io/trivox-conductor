"""
Core registry module for managing endpoint role registrations.
"""

from __future__ import annotations

from .role_registries import ROLE_REGISTRIES
from .watcher_registry import WatcherRegistry

__all__ = [
    "ROLE_REGISTRIES",
    "WatcherRegistry",
]
