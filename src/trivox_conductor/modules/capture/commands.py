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

from trivox_conductor.common.logger import logger
from trivox_conductor.common.base_command import TrivoxConductorCommand
from trivox_conductor.common.commands.base_command import register_command
from trivox_conductor.common.commands.argument_type import ArgumentType

from .processors import CaptureCommandProcessor


@register_command()
class CaptureCommand(TrivoxConductorCommand):
    """
    Command for Capture module.
    """
    
    name = "capture"
    args = [
        ArgumentType("action", str, "Action", choices=("start","stop","list_scenes","list_profiles"), required=True),
        ArgumentType("session_id", str, "Session ID", default="20251029_1050_s0_e0_test"),

        # --- connection overrides (optional) ---
        ArgumentType("host", str, "OBS host", default=None),
        ArgumentType("port", int, "OBS port", default=None),
        ArgumentType("password", str, "OBS password", default=None),
        ArgumentType("request_timeout_sec", float, "OBS request timeout (sec)", default=None),

        # --- selection (optional) ---
        ArgumentType("scene", str, "Scene to select before start", default=None),
        ArgumentType("profile", str, "Profile to select before start", default=None),
    ]
    
    __doc__ = """
    Capture command for managing capture operations.
    Usage:
      capture --action start --session_id <id> [--scene <name>] [--profile <name>]
              [--host 127.0.0.1] [--port 4455] [--password ******] [--request_timeout_sec 3.0]
      capture --action stop [conn-overrides]
      capture --action list_scenes [conn-overrides]
      capture --action list_profiles [conn-overrides]
    
    Description:
        This command allows you to start or stop capture operations
        using the Capture module.
    
    Arguments:
        --action (str): The action to perform. Choices are 'start', 'stop', 'list_scenes', 'list_profiles'.
        --session_id (str): The session ID for the capture operation.
        --host (str, optional): The OBS host address.
        --port (int, optional): The OBS port number.
        --password (str, optional): The OBS password.
        --request_timeout_sec (float, optional): The request timeout in seconds.
    """

    def _execute(self, **kwargs):
        # Implement the command execution logic here
        logger.debug(f"Executing CaptureCommand with kwargs: {kwargs}")
        self.set_processor(CaptureCommandProcessor)
        self._run(**kwargs)
