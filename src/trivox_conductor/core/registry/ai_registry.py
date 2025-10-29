from __future__ import annotations
from typing import Optional
from trivox_conductor.common.registry.endpoint_registry import EndpointRegistry
from trivox_conductor.core.contracts.ai import AIBrainAdapter

class AIRegistry(EndpointRegistry[AIBrainAdapter]):
    endpoint_base: type = AIBrainAdapter
    _active: Optional[str] = None
    @classmethod
    def set_active(cls, name: str) -> None:
        if name not in cls._registry: raise KeyError(f"AI '{name}' not registered.")
        cls._active = name
    @classmethod
    def get_active(cls) -> Optional[AIBrainAdapter]:
        return cls._registry.get(cls._active) if cls._active else None
