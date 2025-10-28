from __future__ import annotations

from typing import Optional, Type, Mapping, MutableMapping, ClassVar

from trivox_conductor.common.registry import EndpointRegistry


class CommandRegistry(EndpointRegistry["BaseCommand"]):
    """
    Registry for command classes (stores classes, not instances).
    Adds alias resolution on top of EndpointRegistry.
    """

    # set by BaseCommand after class is defined to avoid import cycles
    endpoint_base: ClassVar[type]  # = BaseCommand  (assigned in base_command.py)

    _alias_map: ClassVar[MutableMapping[str, str]]  # alias -> primary name

    def __init_subclass__(cls, **kwargs):  # type: ignore[override]
        super().__init_subclass__(**kwargs)
        cls._alias_map = {}

    # --- overrides / helpers -------------------------------------------------

    @classmethod
    def register(
        cls,
        name: str,
        impl_class: Type["BaseCommand"],
        *,
        replace: bool = False,
        aliases: tuple[str, ...] = (),
        abstract: bool = False,
    ) -> None:
        """
        Register a command class under a primary `name` and optional `aliases`.
        Abstract commands are skipped.
        """
        if abstract:
            return

        # Delegate core checks and primary registration
        super().register(name, impl_class, replace=replace)

        # Record aliases -> primary name
        with cls._lock:
            for a in aliases:
                # prevent alias collisions unless replacing the same class name
                if not replace and a in cls._alias_map and cls._alias_map[a] != name:
                    raise KeyError(f"Alias '{a}' already mapped to '{cls._alias_map[a]}'")
                cls._alias_map[a] = name

    @classmethod
    def endpoint(
        cls,
        name: Optional[str] = None,
        *,
        replace: bool = False,
    ):
        """
        Decorator for registering commands. Pulls metadata from class attributes:
        - name (str) if not provided here, inferred from class name
        - aliases (tuple[str, ...])  optional
        - abstract (bool)           if True, not registered
        """
        def decorator(impl_class: Type["BaseCommand"]) -> Type["BaseCommand"]:
            resolved_name = (
                name
                or getattr(impl_class, "name", None)
                or cls._infer_name(impl_class)
            )
            aliases = tuple(getattr(impl_class, "aliases", ()))  # type: ignore[call-arg]
            abstract = bool(getattr(impl_class, "abstract", False))
            cls.register(
                resolved_name,
                impl_class,
                replace=replace,
                aliases=aliases,
                abstract=abstract,
            )
            return impl_class
        return decorator

    # Lookups that understand aliases
    @classmethod
    def _resolve_primary(cls, name_or_alias: str) -> str:
        if name_or_alias in cls._registry:
            return name_or_alias
        return cls._alias_map.get(name_or_alias, name_or_alias)

    @classmethod
    def get(cls, name_or_alias: str) -> Type["BaseCommand"]:
        primary = cls._resolve_primary(name_or_alias)
        return super().get(primary)

    @classmethod
    def try_get(cls, name_or_alias: str) -> Optional[Type["BaseCommand"]]:
        primary = cls._resolve_primary(name_or_alias)
        return super().try_get(primary)

    @classmethod
    def contains(cls, name_or_alias: str) -> bool:
        primary = cls._resolve_primary(name_or_alias)
        return super().contains(primary)

    @classmethod
    def names(cls) -> list[str]:
        """Primary command names only (aliases excluded)."""
        return super().names()

    @classmethod
    def all_with_aliases(cls) -> Mapping[str, Type["BaseCommand"]]:
        """Convenience: primary names plus alias keys."""
        # snapshot with aliases pointing to same class
        out: dict[str, Type["BaseCommand"]]= dict(cls._registry)
        for alias, primary in cls._alias_map.items():
            if primary in cls._registry:
                out[alias] = cls._registry[primary]
        return out

    @classmethod
    def unregister(cls, name_or_alias: str) -> None:
        """Unregister a command by primary name or alias (removes its aliases too)."""
        with cls._lock:
            primary = cls._resolve_primary(name_or_alias)
            # remove class
            cls._registry.pop(primary, None)
            # remove aliases mapped to this primary
            to_del = [a for a, p in cls._alias_map.items() if p == primary]
            for a in to_del:
                cls._alias_map.pop(a, None)

    @classmethod
    def clear(cls) -> None:
        with cls._lock:
            super().clear()
            cls._alias_map.clear()
