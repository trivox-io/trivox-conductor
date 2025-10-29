
from __future__ import annotations

from dataclasses import dataclass, asdict
from trivox_conductor.common.settings.settings_registry import register_setting
from trivox_conductor.common.settings.base_settings import BaseSettings


@dataclass(frozen=True)
class HandoffSettingsModel:
    """
    Configuration data for the Handoff module.
    
    :cvar rclone_remote (str): Rclone remote name.
    :cvar dest_root (str): Destination root path for handoff.
    :cvar slack_channel (str): Slack channel for notifications.
    :cvar discord_channel (str): Discord channel for notifications.
    """

    rclone_remote: str = "drive:"
    dest_root: str = "/IG/Clips"
    slack_channel: str = "#conductor"
    discord_channel: str = "clips"


@register_setting()
class HandoffSettings(BaseSettings):
    """
    Settings for the Handoff module.
    """
    
    name = "handoff"

    def __init__(self):
        super().__init__(asdict(HandoffSettingsModel()))
