from __future__ import annotations
from typing import Optional, Type
from trivox_conductor.common.registry.endpoint_registry import EndpointRegistry
from trivox_conductor.core.contracts.capture import CaptureAdapter

class CaptureRegistry(EndpointRegistry[CaptureAdapter]):
    endpoint_base: type = CaptureAdapter
    _active: Optional[str] = None
    _active_instance: Optional[CaptureAdapter] = None  # cache

    @classmethod
    def set_active(cls, name: str) -> None:
        if name not in cls._registry:
            raise KeyError(f"Capture adapter '{name}' not registered.")
        cls._active = name
        cls._active_instance = None  # reset instance on change

    @classmethod
    def get_active_class(cls) -> Optional[Type[CaptureAdapter]]:
        if cls._active is None:
            return None
        return cls._registry.get(cls._active)

    @classmethod
    def get_active(cls) -> Optional[CaptureAdapter]:
        if cls._active is None:
            return None
        if cls._active_instance is None:
            cls._active_instance = cls.instantiate(cls._active)  # from EndpointRegistry
        return cls._active_instance
