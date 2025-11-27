from __future__ import annotations

from typing import Type

from trivox_conductor.common.registry.implementation_registry import (
    ImplementationRegistry,
)

from .observer_base import BaseObserver


class ObserverRegistry(ImplementationRegistry[BaseObserver]):
    """
    Registry for observer implementations (ManifestObserver, NotificationObserver, etc.).
    """

    implementation_base: type = BaseObserver


def register_observer(name: str, cls: Type[BaseObserver]) -> None:
    """
    Small helper if you prefer function-style registration.
    """
    ObserverRegistry.register(name, cls)
