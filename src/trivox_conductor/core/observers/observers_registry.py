from __future__ import annotations

from typing import Type

from trivox_conductor.common.registry.endpoint_registry import EndpointRegistry

from .base_observer import BaseObserver


class ObserverRegistry(EndpointRegistry[BaseObserver]):
    """
    Registry for observer implementations (ManifestObserver, NotificationObserver, etc.).
    """

    endpoint_base: type = BaseObserver


def register_observer(name: str, cls: Type[BaseObserver]) -> None:
    """
    Small helper if you prefer function-style registration.
    """
    ObserverRegistry.register(name, cls)
