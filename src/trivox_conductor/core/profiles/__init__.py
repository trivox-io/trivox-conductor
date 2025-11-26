"""
Profile management for Trivox Conductor.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import trivox_conductor.constants as trivox_constants
from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings

from .profile_manager import ProfileManager

_PROFILES_PATH = (
    Path(trivox_constants.ROOT_DIR)
    / "src"
    / "trivox_conductor"
    / "profiles.yml"
)

# internal cache
_profile_manager: Optional[ProfileManager] = None


def get_profile_manager() -> ProfileManager:
    """
    Lazily build and cache the ProfileManager.

    This must only be called after settings.populate(), which is done in
    `initialize()`.
    """
    global _profile_manager
    if _profile_manager is not None:
        return _profile_manager

    pipelines_dir = settings.get("app.pipelines_dir", None)
    extra_dir: Optional[Path]
    if pipelines_dir:
        extra_dir = Path(pipelines_dir)
    else:
        extra_dir = None

    _profile_manager = ProfileManager.from_base_and_dir(
        base_path=_PROFILES_PATH,
        extra_dir=extra_dir,
    )
    return _profile_manager
