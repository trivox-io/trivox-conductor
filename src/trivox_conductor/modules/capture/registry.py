from __future__ import annotations

from typing import Optional, Type

from trivox_conductor.common.registry.implementation_registry import (
    ImplementationRegistry,
)
from trivox_conductor.core.registry.role_registries import (
    register_role_registry,
)

from .contracts import CaptureAdapter


class CaptureRegistry(ImplementationRegistry[CaptureAdapter]):
    """
    Registry for CaptureAdapter implementations.

    :cvar implementation_base (type): Base class for registered endpoints.
    :cvar _active_adapter (Optional[str]): Name of the currently active adapter.
    :cvar _active_instance (Optional[CaptureAdapter]): Cached instance of the active adapter.
    """

    implementation_base: type = CaptureAdapter
    _active_adapter: Optional[str] = None
    _active_instance: Optional[CaptureAdapter] = None  # cached instance

    @classmethod
    def set_active(cls, name: str):
        """
        Set the active capture adapter by name.

        :param name: Name of the adapter to set as active.
        :type name: str

        :raises KeyError: If the adapter name is not registered.
        """
        if name not in cls._registry:
            raise KeyError(f"Capture adapter '{name}' not registered.")
        cls._active_adapter = name
        cls._active_instance = None  # reset instance on change

    @classmethod
    def get_active_class(cls) -> Optional[Type[CaptureAdapter]]:
        """
        Get the class of the currently active capture adapter.

        :return: Active adapter class or None if not set.
        :rtype: Optional[Type[CaptureAdapter]]
        """
        if cls._active_adapter is None:
            return None
        return cls._registry.get(cls._active_adapter)

    @classmethod
    def get_active(cls) -> Optional[CaptureAdapter]:
        """
        Get the singleton instance of the currently active capture adapter.

        :return: Active adapter instance or None if not set.
        :rtype: Optional[CaptureAdapter]
        """
        if cls._active_adapter is None:
            return None
        if cls._active_instance is None:
            cls._active_instance = cls.instantiate(
                cls._active_adapter
            )  # from ImplementationRegistry
        return cls._active_instance


register_role_registry("capture", CaptureRegistry)
