from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional, Protocol


class ViewFactory(Protocol):
    def __call__(self, *, context: dict) -> object: ...

    # PySide widgets will satisfy this but core doesn’t know they’re widgets


ViewCondition = Callable[[dict], bool]


@dataclass
class ViewDescriptor:
    id: str
    title: str
    area: str  # "main", "settings", "tray", etc.
    factory: ViewFactory
    order: int = 0
    icon_name: Optional[str] = None
    visible_if: Optional[ViewCondition] = None


class ViewRegistry:
    """
    Simple in-memory registry for ViewDescriptor instances.

    This is intentionally *not* an EndpointRegistry because we are storing
    data objects (descriptors), not endpoint classes.
    """

    _views: Dict[str, ViewDescriptor] = {}

    @classmethod
    def register(
        cls, name: str, desc: ViewDescriptor, *, replace: bool = False
    ):
        if not isinstance(desc, ViewDescriptor):
            raise TypeError(
                f"ViewRegistry.register() expects a ViewDescriptor, got {type(desc)!r}"
            )
        if not replace and name in cls._views:
            raise KeyError(f"View '{name}' already registered")
        cls._views[name] = desc

    @classmethod
    def get(cls, name: str) -> ViewDescriptor:
        try:
            return cls._views[name]
        except KeyError as e:
            raise KeyError(f"Unknown view '{name}'") from e

    @classmethod
    def all(cls) -> Dict[str, ViewDescriptor]:
        return dict(cls._views)

    @classmethod
    def names(cls) -> list[str]:
        return list(cls._views.keys())

    @classmethod
    def clear(cls) -> None:
        cls._views.clear()
