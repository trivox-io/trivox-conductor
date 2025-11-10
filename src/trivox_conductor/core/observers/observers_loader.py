from __future__ import annotations

import importlib

from trivox_conductor.common.logger import logger

_OBSERVER_MODULES = [
    "trivox_conductor.core.manifests.manifest_observer",
    "trivox_conductor.core.observers.notifications",
    "trivox_conductor.core.observers.watcher_autostart",
]


def load_all_observers():
    for mod_name in _OBSERVER_MODULES:
        try:
            importlib.import_module(mod_name)
            logger.debug("Loaded observer module %s", mod_name)
        except Exception as e:
            logger.exception(
                "Failed to load observer module %s: %s", mod_name, e
            )
