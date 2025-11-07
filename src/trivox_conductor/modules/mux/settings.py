from __future__ import annotations

from dataclasses import asdict, dataclass

from trivox_conductor.common.settings.base_settings import BaseSettings
from trivox_conductor.common.settings.settings_registry import register_setting


@dataclass(frozen=True)
class MuxSettingsModel:
    """
    Configuration data for the Mux module.

    :cvar ffmpeg_path (str): Path to the ffmpeg executable.
    :cvar normalize (bool): Flag to enable audio normalization.
    :cvar loudness_target_lufs (float): Target loudness in LUFS for normalization.
    :cvar desktop_device (str): Default desktop audio device.
    :cvar mic_device (str): Default microphone audio device.
    """

    ffmpeg_path: str = "ffmpeg"
    normalize: bool = True
    loudness_target_lufs: float = -16.0
    desktop_device: str = "default"
    mic_device: str = "default"


@register_setting()
class MuxSettings(BaseSettings):
    """
    Settings for the Mux module.
    """

    name = "mux"

    def __init__(self):
        super().__init__(asdict(MuxSettingsModel()))
