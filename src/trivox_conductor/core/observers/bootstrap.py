from __future__ import annotations

from trivox_conductor.common.logger import logger

from .base_observer import BaseObserver, ObserverContext
from .observers_registry import ObserverRegistry


def attach_all_observers(context: ObserverContext) -> None:
    """
    Instantiate and attach all registered observers.

    Each observer decides (based on context/profile/hooks) whether to actually
    subscribe to any topics.
    """
    logger.debug(f"Observers {list(ObserverRegistry.all())}")
    for name in ObserverRegistry.names():
        cls = ObserverRegistry.get(name)
        logger.error("Attaching observer '%s'...", name)
        logger.debug("With class: %s", cls)
        try:
            observer: BaseObserver = cls(context)  # type: ignore[call-arg]
            observer.attach()
            logger.debug("Observer '%s' attached", name)
        except Exception as e:
            logger.exception("Observer '%s' failed to attach: %s", name, e)
