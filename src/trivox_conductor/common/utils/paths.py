from __future__ import annotations

import os
from pathlib import Path

import trivox_conductor.constants as trivox_constants


def get_repo_root() -> Path:
    """
    Best-effort repo root: the directory that contains the 'trivox_conductor'
    package. This matches how you're currently resolving the .trivox_conductor
    folder relative to src.
    """
    # __file__ is .../src/trivox_conductor/common/utils/paths.py
    here = Path(__file__).resolve()
    return here.parents[4]  # .../trivox-conductor/


def get_app_root() -> Path:
    """
    Root for all app data (.trivox_conductor).

    Resolution order:
      1) TRIVOX_DATA_DIR (full path)
      2) repo_root / ".trivox_conductor" (current dev behavior)
    """
    env = os.getenv(str(trivox_constants.ENV_VARS.data_dir))
    if env:
        return Path(env).expanduser().resolve()

    return get_repo_root() / trivox_constants.DATA.data_dir_name


def get_settings_dir() -> Path:
    """
    Directory that holds settings YAML files.

    Resolution order:
      1) TRIVOX_CONFIG_PATH (for backward compatibility)
      2) <app_root> / "settings"
    """
    env = os.getenv(str(trivox_constants.ENV_VARS.config_dir))
    if env:
        return Path(env).expanduser().resolve()

    return get_app_root() / "settings"


def get_manifests_dir() -> Path:
    """
    Directory that holds manifests.
    """
    return get_app_root() / "manifests"


def ensure_dir(path: Path) -> Path:
    """
    Ensure a directory exists and return it.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
