from trivox_conductor.common.base_command import (
    ActionArgument,
    SessionIDArgument,
    TrivoxConductorCommand,
)
from trivox_conductor.common.commands.argument_type import ArgumentType
from trivox_conductor.common.commands.base_command import register_command
from trivox_conductor.common.logger import logger

from .processors import WatcherCommandProcessor


@register_command()
class WatcherCommand(TrivoxConductorCommand):
    """
    Command for Replay module.
    """

    name = "watch"
    args = [
        ActionArgument("start", "stop", "on_raw_detect"),
        SessionIDArgument(),
    ]

    __doc__ = """
    Replay command for managing watch operations.
    Usage:
        watch --action start
    
    Description:
        This command allows you to start or stop watch operations
        using the Replay module.
    
    Arguments:
        --action (str): The action to perform. Choices are 'start', 'stop', 'on_raw_detect'.
    """

    def _execute(self, **kwargs):
        # Implement the command execution logic here
        logger.debug(f"Executing ReplayCommand with kwargs: {kwargs}")
        self.set_processor(WatcherCommandProcessor)
        self._run(**kwargs)
