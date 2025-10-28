
from __future__ import annotations

from typing import Optional, Union, ClassVar
from abc import ABC

JSONScalar = Union[str, int, float, bool]


class BaseSettings(ABC):
    """
    Base class for all settings.

    Subclasses can set a class-level `name`. If omitted, the registry infers it
    from the class name (lowercased).
    """
    name: ClassVar[Optional[str]] = None

    def __init__(self, data: Optional[dict[str, JSONScalar]] = None) -> None:
        # Avoid mutable-class-attribute pitfalls
        self.data: dict[str, JSONScalar] = dict(data or {})

    def get(self, key: str, default: Optional[JSONScalar] = None) -> Optional[JSONScalar]:
        return self.data.get(key, default)

    def set(self, key: str, value: JSONScalar) -> None:
        self.data[key] = value
