from __future__ import annotations

from typing import Dict
from trivox_conductor.core.contracts.color import ColorAdapter
from trivox_conductor.core.registry.color_registry import ColorRegistry
from trivox_conductor.core.services.base_service import BaseService
from .settings import ColorSettingsModel

class ColorService(BaseService[ColorSettingsModel, ColorAdapter]):
    """
    Drives the ColorAdapter (Resolve Free) with preset/LUT configuration.
    """
    
    SECTION = "color"
    MODEL = ColorSettingsModel

    def __init__(self, registry: ColorRegistry, settings: Dict) -> None:
        super().__init__(registry, settings)

    def color_pass(self, src_path: str) -> None:
        adapter = self._require_adapter()
        adapter.color_pass(src_path, self._settings.resolve_preset, self._settings.output_dir)

