from __future__ import annotations

from dataclasses import asdict, dataclass

from trivox_conductor.common.settings.base_settings import BaseSettings
from trivox_conductor.common.settings.settings_registry import register_setting


@dataclass(frozen=True)
class AISettingsModel:
    """
    Configuration data for the AI module.

    :cvar model_name (str): Name of the AI model to use.
    :cvar hashtags_target (int): Target number of hashtags to generate.
    :cvar spotify_cache_ttl_s (int): Time-to-live for Spotify cache in seconds.
    """

    model_name: str = "gpt-4o-mini"
    hashtags_target: int = 10
    spotify_cache_ttl_s: int = 86400


@register_setting()
class AISettings(BaseSettings):
    """
    Settings for the AI module.
    """

    name = "ai"

    def __init__(self):
        super().__init__(asdict(AISettingsModel()))
