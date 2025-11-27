"""
Main application entry point for Trivox Conductor.
"""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from typing import Optional

import trivox_conductor.constants as trivox_constants
from trivox_conductor.common.dynamic_loader import DynamicLoader
from trivox_conductor.common.logger import logger
from trivox_conductor.common.logging import resolve_log_levels, setup_logging
from trivox_conductor.common.registry.implementation_registry import (
    ImplementationRegistry,
)
from trivox_conductor.common.settings import settings
from trivox_conductor.common.settings.base_settings import BaseSettings
from trivox_conductor.common.settings.settings_registry import register_setting
from trivox_conductor.core.bootstrap import (
    ModulesLoader,
    ObserversLoader,
    PluginsLoader,
)
from trivox_conductor.core.registry import ROLE_REGISTRIES
from trivox_conductor.core.registry.base_loader import (
    import_adapter_from_descriptor,
    load_descriptors,
)


@dataclass(frozen=True)
class AppSettingsModel:
    """
    Configuration data for the Application.

    :cvar pipelines_dir (str): Directory path for storing pipeline configurations.
    """

    pipelines_dir: str = f"{trivox_constants.ROOT_DIR}/.trivox/profiles"


@register_setting()
class AppSettings(BaseSettings):
    """
    Settings for the Application.
    """

    name = "app"

    def __init__(self):
        super().__init__(asdict(AppSettingsModel()))


def load_local_plugins(pkg_root: Optional[str] = "trivox_conductor"):
    """
    Discover local plugins from the 'plugins' directory and register them
    into role-specific registries, based on plugin.yaml descriptors.

    This only registers implementations; it does NOT choose which adapter
    is 'active' for any role. That decision is made later by profiles or
    explicit CLI/GUI actions.
    """
    for reg in ROLE_REGISTRIES.values():
        logger.debug(f"Clearing registry for role: {reg}")
    plugins_root = os.path.join(os.path.dirname(__file__), "plugins")
    descriptors = load_descriptors(os.path.abspath(plugins_root))
    logger.debug(f"Plugin descriptors loaded: {descriptors}")

    for descriptor in descriptors:
        clazz = import_adapter_from_descriptor(descriptor, pkg_root=pkg_root)
        name = clazz.__name__.lower()

        registry: ImplementationRegistry = ROLE_REGISTRIES.get(descriptor.role)
        if not registry:
            logger.warning(
                "Unknown plugin role '%s' for %s", descriptor.role, descriptor
            )
            continue

        registry.register(name, clazz)

    logger.info("Local plugins loaded and registered.")


def initialize(verbose_level: Optional[int] = None) -> None:
    """
    Initialize the Trivox Conductor application.

    - Resolve logging levels.
    - Setup logging with appropriate overrides.
    - Load all modules to register commands, settings, and strategies.
    - Load local plugins from the 'plugins' directory.
    - Load Observers.
    - Populate settings. This must be done after loading modules/plugins.
    """
    app_level, root_level = resolve_log_levels(verbose_level)

    setup_logging(
        overrides={
            "handlers": {
                "file": {
                    "maxBytes": 10485760,
                    "backupCount": 5,
                    "filename": trivox_constants.LOGGER.file_path,
                },
            },
            "root": {"level": root_level},
            "loggers": {
                trivox_constants.LOGGER.logger_name: {
                    "level": app_level,
                    "propagate": True,
                },
            },
        }
    )

    loader = DynamicLoader()
    loader.register(ModulesLoader().build_spec())
    loader.register(PluginsLoader().build_spec())
    loader.register(ObserversLoader().build_spec())
    loader.load_all()
    settings.populate()
    logger.info("Trivox Conductor application started.")


if __name__ == "__main__":
    initialize()
if __name__ == "__main__":
    initialize()
