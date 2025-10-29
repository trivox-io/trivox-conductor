from __future__ import annotations
from typing import Optional
from trivox_conductor.common.registry.endpoint_registry import EndpointRegistry
from trivox_conductor.core.contracts.color import ColorAdapter

class ColorRegistry(EndpointRegistry[ColorAdapter]):
    endpoint_base: type = ColorAdapter
    _active: Optional[str] = None
    @classmethod
    def set_active(cls, name: str) -> None:
        if name not in cls._registry: raise KeyError(f"Color '{name}' not registered.")
        cls._active = name
    @classmethod
    def get_active(cls) -> Optional[ColorAdapter]:
        return cls._registry.get(cls._active) if cls._active else None
