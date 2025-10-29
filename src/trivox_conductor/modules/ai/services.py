
from __future__ import annotations
from typing import Dict, Any, List
from trivox_conductor.core.contracts.ai import AIBrainAdapter
from trivox_conductor.core.registry.ai_registry import AIRegistry
from trivox_conductor.core.services.base_service import BaseService
from .settings import AISettingsModel


class AIBrainService(BaseService[AISettingsModel, AIBrainAdapter]):
    """Turns a manifest snippet + vibe into 3 options (hook/caption/hashtags)."""
    
    SECTION = "ai"
    MODEL = AISettingsModel

    def __init__(self, registry: AIRegistry, settings: Dict) -> None:
        super().__init__(registry, settings)

    def generate(self, manifest_snippet: Dict[str, Any]) -> Dict[str, Any]:
        adapter = self._require_adapter()
        return adapter.generate_options(manifest_snippet)


class BeatMarkerService(BaseService[AISettingsModel, AIBrainAdapter]):
    """
    Optional helper for mapping song features to visual beat markers.
    Kept separate from AIBrainService to respect SRP.
    """
    
    SECTION = "ai"
    MODEL = AISettingsModel
    
    def __init__(self, registry: AIRegistry, settings: Dict) -> None:
        super().__init__(registry, settings)
        
    def markers_from_features(self, features: Dict) -> List[int]:
        # TODO: simple tempo → milliseconds conversion; leave stubbed
        return []
