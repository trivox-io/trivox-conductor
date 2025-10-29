
import os
from trivox_conductor.core.registry.base_loader import load_descriptors, import_adapter_from_descriptor
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
from trivox_conductor.core.registry.watcher_registry import WatcherRegistry
    # ... set others

from trivox_conductor.common.module_loader import load_all_modules
from trivox_conductor.common.logging import setup_logging
from trivox_conductor.common.logger import logger

# ... import other registries

def load_local_plugins(pkg_root="trivox_conductor"):
    plugins_root = os.path.join(os.path.dirname(__file__), "plugins")
    descs = load_descriptors(os.path.abspath(plugins_root))
    logger.debug(f"Plugin descriptors loaded: {descs}")
    for d in descs:
        clazz = import_adapter_from_descriptor(d, pkg_root=pkg_root)
        name = clazz.__name__.lower()

        # Register into the right registry (name + class!)
        if d.role == "capture":
            CaptureRegistry.register(name, clazz)
        elif d.role == "watcher":
            WatcherRegistry.register(name, clazz)
        # TODO: add mux/color/uploader/notifier/ai when you add their plugins

    # choose actives (from settings)
    CaptureRegistry.set_active("obsadapter")        # class name lower() by default
    WatcherRegistry.set_active("replaywatcheradapter")


def initialize():
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
    logger.info("Trivox Conductor application started.")

if __name__ == "__main__":
    initialize()
