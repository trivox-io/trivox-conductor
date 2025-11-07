"""
Package for base settings classes.
Provides the BaseSettings class for application settings.
"""

from __future__ import annotations

from abc import ABC
from typing import ClassVar, Optional, Union

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

    def get(
        self, key: str, default: Optional[JSONScalar] = None
    ) -> Optional[JSONScalar]:
        """
        Get a setting value by key.

        :param key: The setting key.
        :type key: str

        :param default: The default value if the key is not found.
        :type default: Optional[JSONScalar]

        :return: The setting value or default.
        :rtype: Optional[JSONScalar]
        """
        return self.data.get(key, default)

    def set(self, key: str, value: JSONScalar):
        """
        Set a setting value by key.

        :param key: The setting key.
        :type key: str

        :param value: The setting value.
        :type value: JSONScalar
        """
        self.data[key] = value
