"""
Base command module
This module defines the BaseCommand class, which serves as a base for all
command implementations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Tuple, Type

from .argument_type import ArgumentType
from .registry import CommandRegistry  # safe: we don't register on import


class BaseCommand(ABC):
    """
    Base class for all commands.

    Registration is done via the endpoint decorator:

        @CommandRegistry.endpoint("build")
        class Build(BaseCommand): ...

    or:

        from .command_registry import register_command
        @register_command("build", aliases=("b",))
        class Build(BaseCommand): ...

    Subclasses should implement the execute(...) method as the main entrypoint.

    :cvar name: Optional[str]: Command name (for registry); defaults to class name lowercased.
    :cvar aliases: Tuple[str, ...]: Optional command aliases.
    :cvar summary: Optional[str]: Short description of the command.
    :cvar epilog: Optional[str]: Additional help text for the command.
    :cvar args: Optional[List[ArgumentType]]: List of command arguments.
    :cvar abstract: bool: If True, the command is not registered (base class
    """

    # Metadata read by CommandRegistry.endpoint(...)
    name: Optional[str] = None
    aliases: Tuple[str, ...] = ()
    summary: Optional[str] = None
    epilog: Optional[str] = None
    args: Optional[List[ArgumentType]] = None
    abstract: bool = False  # if True, decorator will skip registration

    # Keep __init_subclass__ empty to avoid import/registration cycles
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    @classmethod
    def define_arguments(cls) -> List[ArgumentType]:
        """
        Return the list of ArgumentType for this command.

        :return: List of ArgumentType instances.
        :rtype: List[ArgumentType]
        """
        return list(cls.args or [])

    def validate(self, **_kwargs):
        """Optional argument validation hook."""
        # override in subclasses
        return None

    @abstractmethod
    def _run(self, **kwargs):
        """Internal run (pre-exec)."""

    @abstractmethod
    def _execute(self, **kwargs):
        """Internal execution step (core logic)."""

    @abstractmethod
    def execute(self, **kwargs):
        """External command entrypoint."""
        # typical pattern: self.validate(...); self._run(...); return self._execute(...)
        raise NotImplementedError


# Bind the endpoint_base now that BaseCommand exists (avoids circular import issues)
CommandRegistry.endpoint_base = BaseCommand


# Optional: keep your old ergonomic helper
def register_command(
    name: Optional[str] = None,
    *,
    aliases: Tuple[str, ...] = (),
    replace: bool = False,
) -> Callable[[Type[BaseCommand]], Type[BaseCommand]]:
    """
    Convenience decorator for registering commands with metadata.
    Mirrors your previous pattern but uses the new registry.

    :param name: Optional command name; defaults to class name lowercased.
    :type name: Optional[str]

    :param aliases: Optional command aliases.
    :type aliases: Tuple[str, ...]

    :param replace: Whether to replace an existing command with the same name.
    :type replace: bool

    :return: Decorator function.
    :rtype: Callable[[Type[BaseCommand]], Type[BaseCommand]]
    """

    def deco(impl_cls: type[BaseCommand]) -> type[BaseCommand]:
        resolved = (
            name
            or getattr(impl_cls, "name", None)
            or impl_cls.__name__.lower()
        )
        # set attributes so CommandRegistry.endpoint can pick them up if desired
        if name is not None:
            impl_cls.name = resolved
        if aliases:
            impl_cls.aliases = aliases
        return CommandRegistry.endpoint(resolved, replace=replace)(impl_cls)

    return deco
