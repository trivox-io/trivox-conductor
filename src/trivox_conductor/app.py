"""
Main application entry point for Trivox Conductor.
"""

import os
from typing import Optional

from trivox_conductor.common.logger import logger
from trivox_conductor.common.logging import setup_logging
from trivox_conductor.common.module_loader import load_all_modules
from trivox_conductor.common.registry.endpoint_registry import EndpointRegistry
from trivox_conductor.core.observers.observers_loader import load_all_observers
from trivox_conductor.core.registry import ROLE_REGISTRIES
from trivox_conductor.core.registry.base_loader import (
    import_adapter_from_descriptor,
    load_descriptors,
)


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

        registry: EndpointRegistry = ROLE_REGISTRIES.get(descriptor.role)
        if not registry:
            logger.warning(
                "Unknown plugin role '%s' for %s", descriptor.role, descriptor
            )
            continue

        registry.register(name, clazz)

    logger.info("Local plugins loaded and registered.")


def initialize():
    """
    Initialize the Trivox Conductor application.

    - Setup logging with appropriate overrides.
    - Load all modules to register commands, settings, and strategies.
    - Load local plugins from the 'plugins' directory.
    """
    setup_logging(
        overrides={
            "handlers": {
                "file": {
                    "maxBytes": 10485760,
                    "backupCount": 5,
                },
            },
            "root": {"level": "INFO"},
            "loggers": {
                "trivox_conductor": {
                    "level": "DEBUG",
                    "propagate": True,
                },
            },
        }
    )
    load_all_modules()
    load_local_plugins()
    load_all_observers()
    logger.info("Trivox Conductor application started.")


if __name__ == "__main__":
    initialize()
