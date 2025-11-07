"""
Registry for WatcherAdapter implementations.
"""

from __future__ import annotations

from typing import Optional, Type

from trivox_conductor.common.registry.endpoint_registry import EndpointRegistry
from trivox_conductor.core.contracts.watcher import WatcherAdapter

from .role_registries import register_role_registry


class WatcherRegistry(EndpointRegistry[WatcherAdapter]):
    endpoint_base: type = WatcherAdapter
    _active: Optional[str] = None
    _active_instance: Optional[WatcherAdapter] = None  # cache

    @classmethod
    def set_active(cls, name: str) -> None:
        if name not in cls._registry:
            raise KeyError(f"Watcher adapter '{name}' not registered.")
        cls._active = name
        cls._active_instance = None  # reset instance on change

    @classmethod
    def get_active_class(cls) -> Optional[Type[WatcherAdapter]]:
        if cls._active is None:
            return None
        return cls._registry.get(cls._active)

    @classmethod
    def get_active(cls) -> Optional[WatcherAdapter]:
        if cls._active is None:
            return None
        if cls._active_instance is None:
            cls._active_instance = cls.instantiate(
                cls._active
            )  # from EndpointRegistry
        return cls._active_instance


register_role_registry("watcher", WatcherRegistry)
