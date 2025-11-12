# TODO: Improve module organization later
from __future__ import annotations

from .app_constants import (
    APP_VERSION,
    CLI_DOCS,
    ROOT_DIR,
    AppInfo,
    CLIInfo,
    DataInfo,
    EnvVars,
    LoggerConstants,
)
from .loader_constants import (
    ModuleLoaderInfo,
    ObserverLoaderInfo,
    PluginLoaderInfo,
)

__all__ = [
    "ROOT_DIR",
    "APP",
    "CLI",
    "DATA",
    "ENV_VARS",
    "LOGGER",
    "MODULES_LOADER",
    "PLUGINS_LOADER",
    "OBSERVERS_LOADER",
]

APP = AppInfo(
    name="Trivox Conductor",
    codename="trivox-conductor",
    version=APP_VERSION,
)

CLI = CLIInfo(
    executable_name="trivox_conductor",
    description="Trivox Conductor Command Line Interface",
    usage=CLI_DOCS,
)

DATA = DataInfo(
    data_dir_name=".trivox",
)

ENV_VARS = EnvVars(
    data_dir="TRIVOX_DATA_DIR",
    config_dir="TRIVOX_CONFIG_DIR",
)

LOGGER = LoggerConstants(
    logger_name="trivox_conductor",
    file_path=str(ROOT_DIR / ".trivox" / "logs" / "trivox_conductor.log"),
)

MODULES_LOADER = ModuleLoaderInfo(
    modules_package="trivox_conductor.modules",
    required_files=(
        "commands.py",
        "settings.py",
        "strategies.py",
        "ui.py",
    ),
)
PLUGINS_LOADER = PluginLoaderInfo(
    plugins_package_root="trivox_conductor.plugins",
    plugins_dir_name="plugins",
)
OBSERVERS_LOADER = ObserverLoaderInfo(
    packages=(
        "trivox_conductor.core.manifests",
        "trivox_conductor.core.observers",
    ),
    module_name_suffixes=("_observer",),
)
