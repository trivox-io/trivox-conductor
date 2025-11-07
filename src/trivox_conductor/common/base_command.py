"""
Base ingest command Module
This module defines the TrivoxConductorCommand class, which serves as a base for all
ic_ingest commands.
"""

from __future__ import annotations

from typing import Any, Iterable, List, Optional

from trivox_conductor.common.commands.argument_type import ArgumentType
from trivox_conductor.common.commands.base_command import BaseCommand
from trivox_conductor.common.commands.base_command_processor import (
    BaseCommandProcessor,
)
from trivox_conductor.common.commands.exceptions import CommandException
from trivox_conductor.common.logger import logger


class ActionArgument(ArgumentType):
    """
    Standardized 'action' CLI argument.

    Usage:
        ActionArgument("start", "stop")
        ActionArgument(*MyCommand.ACTIONS)
        ActionArgument(("start", "stop"))  # tuple/list also works
    """

    def __init__(self, *choices: str | Iterable[str]):
        # Support either:
        #   ActionArgument("start", "stop")
        # or
        #   ActionArgument(("start", "stop"))
        if len(choices) == 1 and not isinstance(choices[0], str):
            # Single iterable passed in
            choices_iter = tuple(choices[0])  # type: ignore[arg-type]
        else:
            # Multiple strings
            choices_iter = tuple(choices)  # type: ignore[assignment]

        super().__init__(
            "action",
            str,
            "Action",
            choices=choices_iter,
            required=True,
        )


class SessionIDArgument(ArgumentType):
    """
    Standardized 'session_id' CLI argument.
    """

    def _generate_default_session_id(self) -> str:
        return "20251029_1050_s0_e0_test"

    def __init__(
        self,
    ):
        super().__init__(
            "session_id",
            str,
            "Session ID",
            default=self._generate_default_session_id(),
        )


class TrivoxConductorCommand(BaseCommand):
    """
    Base class for all TrivoxConductor commands.
    """

    processor: Optional[BaseCommandProcessor] = None

    _COMMON_ARGS: List[ArgumentType] = [
        ArgumentType(
            "config",
            str,
            "Path to the configuration file.",
            required=False,
        ),
        ArgumentType(
            "pipeline_profile",
            str,
            "Profile to select before start",
            default="minecraft_obs_replay",
        ),
    ]

    @classmethod
    def define_arguments(cls) -> List[ArgumentType]:
        """
        Merge command-specific args with common flags.
        Ensures no duplicate names if a command defines its own.
        """
        specific = list(cls.args or [])
        existing = {a.name for a in specific}
        merged = specific[:]
        for common in cls._COMMON_ARGS:
            if common.name not in existing:
                merged.append(common)
        return merged

    def set_verbose(self, verbose: bool):
        """
        Set the verbose mode for the command.

        :param verbose: Whether to enable verbose mode.
        :type verbose: bool
        """
        if verbose:
            logger.setLevel("DEBUG")
            logger.debug("Verbose mode enabled")
            logger.debug(f"Executing {self.name} in verbose mode: {verbose}")

    def set_processor(self, processor: BaseCommandProcessor):
        """
        Set the processor for the command.

        :param processor: The processor for the command.
        :type processor: BaseCommandProcessor
        """
        if not issubclass(processor, BaseCommandProcessor):
            raise CommandException(
                f"Processor {processor} is not a subclass of BaseCommandProcessor"
            )

        self.processor = processor

    def _run(self, **kwargs):
        """
        Run the command.
        """
        if not self.processor:
            logger.error("No processor set for the command")
            raise CommandException("Processor must be set")

        logger.debug(f"Initializing processor: {self.processor}")
        processor_instance: BaseCommandProcessor = self.processor(**kwargs)
        logger.debug(
            f"Running processor: {processor_instance.__class__.__name__}"
        )
        return processor_instance.run()

    def execute(self, **kwargs):
        """
        Execute the command.
        """
        verbose = kwargs.pop("verbose", False)
        self.set_verbose(verbose)
        return self._execute(**kwargs)
