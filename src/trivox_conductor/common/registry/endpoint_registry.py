"""
Typed, safe, and subclass-isolated endpoint registry.
"""
from __future__ import annotations

from typing import Generic, TypeVar, ClassVar, Mapping, MutableMapping, Iterator, Optional, Type
import threading
import re
from abc import ABC

T = TypeVar("T")  # endpoint implementation type (classes deriving from endpoint_base)


class EndpointRegistry(Generic[T]):
    """
    A registry of *classes* implementing a specific endpoint interface.

    Subclasses **must** set `endpoint_base` to the ABC (or base class) that all
    endpoint implementations derive from.
    """

    endpoint_base: ClassVar[type] = ABC  # override in subclasses
    _registry: ClassVar[MutableMapping[str, Type[T]]]
    _lock: ClassVar[threading.RLock]

    def __init_subclass__(cls, **kwargs):  # type: ignore[override]
        super().__init_subclass__(**kwargs)
        cls._registry = {}
        cls._lock = threading.RLock()

    @staticmethod
    def _infer_name(impl_class: type) -> str:
        return impl_class.__name__.lower()

    @classmethod
    def register(cls, name: str, impl_class: Type[T], *, replace: bool = False) -> None:
        if not issubclass(impl_class, cls.endpoint_base):
            raise TypeError(
                f"{impl_class.__qualname__} must subclass {cls.endpoint_base.__qualname__}"
            )
        with cls._lock:
            if not replace and name in cls._registry:
                raise KeyError(f"Endpoint '{name}' already registered")
            cls._registry[name] = impl_class

    @classmethod
    def unregister(cls, name: str) -> None:
        with cls._lock:
            cls._registry.pop(name, None)

    @classmethod
    def endpoint(cls, name: Optional[str] = None, *, replace: bool = False):
        """Decorator to register an endpoint implementation class."""
        def decorator(impl_class: Type[T]) -> Type[T]:
            cls.register(name or cls._infer_name(impl_class), impl_class, replace=replace)
            return impl_class
        return decorator

    @classmethod
    def get(cls, name: str) -> Type[T]:
        try:
            return cls._registry[name]
        except KeyError as e:
            raise KeyError(f"Unknown endpoint '{name}'") from e

    @classmethod
    def try_get(cls, name: str) -> Optional[Type[T]]:
        return cls._registry.get(name)

    @classmethod
    def contains(cls, name: str) -> bool:
        return name in cls._registry

    @classmethod
    def all(cls) -> Mapping[str, Type[T]]:
        return dict(cls._registry)

    @classmethod
    def names(cls) -> list[str]:
        return list(cls._registry.keys())

    @classmethod
    def find_contains(cls, needle: str) -> list[Type[T]]:
        n = needle.lower()
        return [impl for key, impl in cls._registry.items() if n in key.lower()]

    @classmethod
    def find_regex(cls, pattern: str) -> list[Type[T]]:
        rx = re.compile(pattern, re.IGNORECASE)
        return [impl for key, impl in cls._registry.items() if rx.search(key)]

    @classmethod
    def instantiate(cls, name: str, *args, **kwargs) -> T:
        impl = cls.get(name)
        return impl(*args, **kwargs)  # type: ignore[call-arg]

    @classmethod
    def clear(cls) -> None:
        with cls._lock:
            cls._registry.clear()

    @classmethod
    def __iter__(cls) -> Iterator[tuple[str, Type[T]]]:  # pragma: no cover
        return iter(cls._registry.items())

    @classmethod
    def __len__(cls) -> int:  # pragma: no cover
        return len(cls._registry)
