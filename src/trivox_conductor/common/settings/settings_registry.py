
from __future__ import annotations

from typing import Optional, Union, ClassVar
from abc import ABC

from trivox_conductor.common.registry import EndpointRegistry
from .base_settings import BaseSettings

JSONScalar = Union[str, int, float, bool]

class SettingRegistry(EndpointRegistry[BaseSettings]):
    """Registry that stores *classes* derived from BaseSettings."""
    endpoint_base = BaseSettings

    @classmethod
    def endpoint(cls, name: Optional[str] = None, *, replace: bool = False):
        """
        Decorator specialized for settings classes.

        Name resolution:
        1) explicit `name` argument
        2) `impl_class.name` if set
        3) inferred from class name (lowercase)
        """
        def decorator(impl_class: type[BaseSettings]) -> type[BaseSettings]:
            resolved = name or getattr(impl_class, "name", None) or cls._infer_name(impl_class)
            cls.register(resolved, impl_class, replace=replace)
            return impl_class
        return decorator


def register_setting(name: Optional[str] = None, *, replace: bool = False):
    """
    Convenience decorator alias to mirror your previous helper.
    """
    return SettingRegistry.endpoint(name, replace=replace)
