
from __future__ import annotations

from dataclasses import dataclass, asdict
from trivox_conductor.common.settings.settings_registry import register_setting
from trivox_conductor.common.settings.base_settings import BaseSettings


@dataclass(frozen=True)
class ColorSettingsModel:
    """
    Configuration data for the Color module.
    
    :cvar resolve_preset (str): Default DaVinci Resolve preset name.
    :cvar lut_name (str): Default LUT file name.
    :cvar output_dir (str): Default output directory for color graded files.
    """

    resolve_preset: str = "IG_1080x1920_LUT"
    lut_name: str = "Penrose_BW.cube"
    output_dir: str = "IGColor"


@register_setting()
class ColorSettings(BaseSettings):
    """
    Settings for the Color module.
    """
    
    name = "color"

    def __init__(self):
        super().__init__(asdict(ColorSettingsModel()))
