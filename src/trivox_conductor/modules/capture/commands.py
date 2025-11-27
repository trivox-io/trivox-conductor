"""
Capture CLI Command
===================

Declares the ``capture`` subcommand and its arguments, wiring them to the
:class:`~trivox_conductor.modules.capture.processors.CaptureCommandProcessor`.

What it does
------------
- Registers a ``capture`` command with actions:
  ``start``, ``stop``, ``list_scenes``, ``list_profiles``.
- Exposes optional **connection overrides** (``host``, ``port``, ``password``,
  ``request_timeout_sec``) and **selection hints** (``scene``, ``profile``).
- Delegates execution to the command processor.

Typical usage
-------------
  - ``capture --action start --session_id <id> [--scene <name>] [--profile <name>]``
  - ``capture --action stop``
  - ``capture --action list_scenes``
  - ``capture --action list_profiles``

Notes
-----
This module defines CLI shape only; business logic and I/O are handled by the
processor and service layers.
"""

from trivox_conductor.common.base_command import (
    ActionArgument,
    OptionsArgument,
    TrivoxConductorCommand,
)
from trivox_conductor.common.commands.base_command import register_command
from trivox_conductor.common.logger import logger

from .constants import CAPTURE_MODULE
from .processors import CaptureCommandProcessor


@register_command()
class CaptureCommand(TrivoxConductorCommand):
    """
    Command for Capture module.
    """

    name = CAPTURE_MODULE.command_name
    args = [
        ActionArgument(*CAPTURE_MODULE.actions),
        OptionsArgument(),
    ]

    __doc__ = """
    Capture command for managing capture operations.
    Usage:
      capture --action start --session_id <id> [--options host=127.0.0.1,port=4455,scene=MyScene]
      capture --action stop [--options ...]
      capture --action list_scenes [--options ...]
      capture --action list_profiles [--options ...]
    
    Description:
        This command allows you to start or stop capture operations
        using the Capture module.
    """

    def _execute(self, **kwargs):
        # Implement the command execution logic here
        logger.debug(f"Executing CaptureCommand with kwargs: {kwargs}")
        self.set_processor(CaptureCommandProcessor)
        return self._run(**kwargs)
