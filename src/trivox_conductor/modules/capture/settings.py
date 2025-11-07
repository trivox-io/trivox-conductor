"""
Capture Settings Model & Registration
====================================

Defines the ``CaptureSettingsModel`` dataclass and registers a concrete
:class:`~trivox_conductor.common.settings.base_settings.BaseSettings` entry named
``"capture"``. Values represent *non-sensitive* defaults; secrets can be provided
via local overrides.

Contents
--------
- Defaults used by the capture service (scene/profile).
- OBS connection parameters (``host``, ``port``, ``password``, ``request_timeout_sec``).
- ``@register_setting()`` binds ``CaptureSettings`` into the global settings registry.

Notes
-----
- ``password`` should be set via local settings or environment-backed secrets.
- The service can merge **CLI overrides** on top of these defaults at runtime.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from trivox_conductor.common.settings.base_settings import BaseSettings
from trivox_conductor.common.settings.settings_registry import register_setting


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
    # OBS connection
    host: str = "127.0.0.1"
    port: int = 4455
    password: str = ""  # set in your local secrets or settings
    request_timeout_sec: float = 3.0


@register_setting()
class CaptureSettings(BaseSettings):
    """
    Settings for the Capture module.
    """

    name = "capture"

    def __init__(self):
        super().__init__(asdict(CaptureSettingsModel()))
