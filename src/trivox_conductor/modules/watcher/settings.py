from __future__ import annotations

from dataclasses import asdict, dataclass

from trivox_conductor.common.settings.base_settings import BaseSettings
from trivox_conductor.common.settings.settings_registry import register_setting


@dataclass
class WatcherSettingsModel:
    """
    Configuration data for the Watcher module.

    :cvar watch_path (str): Path to watch for replay files.
    :cvar stable_wait_ms (int): Milliseconds to wait for file stability.
    :cvar filename_slug (str): Optional default slug for filenames.
    """

    watch_path: str = ""
    stable_wait_ms: int = 1500
    filename_slug: str = ""  # optional default slug


@register_setting()
class WatcherSettings(BaseSettings):
    """
    Settings for the Watcher module.
    """

    name = "watcher"

    def __init__(self):
        super().__init__(asdict(WatcherSettingsModel()))
