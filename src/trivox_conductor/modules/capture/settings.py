
from __future__ import annotations

from dataclasses import dataclass, asdict
from trivox_conductor.common.settings.settings_registry import register_setting
from trivox_conductor.common.settings.base_settings import BaseSettings


@dataclass(frozen=True)
class CaptureSettingsModel:
    """
    Configuration data for the Capture module.
    
    :cvar default_scene (str): Default scene name.
    :cvar default_profile (str): Default profile name.
    :cvar beep_on_start_stop (bool): Flag to enable beep sound on start/stop.
    :cvar overlay_enabled (bool): Flag to enable overlay display.
    """

    default_scene: str = ""
    default_profile: str = ""
    beep_on_start_stop: bool = True
    overlay_enabled: bool = False


@register_setting()
class CaptureSettings(BaseSettings):
    """
    Settings for the Capture module.
    """
    
    name = "capture"

    def __init__(self):
        super().__init__(asdict(CaptureSettingsModel()))
