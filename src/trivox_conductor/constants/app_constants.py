from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import toml


def _populate_version_from_pyproject() -> str:
    """Populate version from pyproject.toml if available."""
    pyproject_path = ROOT_DIR / "pyproject.toml"
    if pyproject_path.exists():
        try:
            with pyproject_path.open("r", encoding="utf-8") as f:
                pyproject_data = toml.load(f)
                return pyproject_data.get("project", {}).get(
                    "version", "0.0.0"
                )
        except ImportError:
            pass
    return "0.0.0"


ROOT_DIR = Path(__file__).resolve().parents[3]
APP_VERSION = _populate_version_from_pyproject()
CLI_DOCS = """
DEV: python manage.py <command> [<args>]
PROD: trivox_conductor <command> [<args>]
"""


@dataclass(frozen=True)
class AppInfo:
    """Application information."""

    name: str
    codename: str
    version: str


@dataclass(frozen=True)
class EnvVars:
    data_dir: str
    config_dir: str


@dataclass(frozen=True)
class CLIInfo:
    executable_name: str
    description: str
    usage: str


@dataclass(frozen=True)
class DataInfo:
    data_dir_name: str


@dataclass(frozen=True)
class LoggerConstants:
    logger_name: str
    file_path: str
