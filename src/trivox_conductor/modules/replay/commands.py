
from trivox_conductor.common.logger import logger
from trivox_conductor.common.base_command import TrivoxConductorCommand
from trivox_conductor.common.commands.base_command import register_command
from trivox_conductor.common.commands.argument_type import ArgumentType

from .processors import ReplayCommandProcessor


@register_command()
class ReplayCommand(TrivoxConductorCommand):
    """
    Command for Replay module.
    """
    
    name = "replay"
    args = [
        ArgumentType("action", str, "Action", choices=("start","stop","on_raw_detect",), required=True),
    ]
    
    __doc__ = """
    Replay command for managing replay operations.
    Usage:
        replay --action start
    
    Description:
        This command allows you to start or stop replay operations
        using the Replay module.
    
    Arguments:
        --action (str): The action to perform. Choices are 'start', 'stop', 'on_raw_detect'.
    """

    def _execute(self, **kwargs):
        # Implement the command execution logic here
        logger.debug(f"Executing ReplayCommand with kwargs: {kwargs}")
        self.set_processor(ReplayCommandProcessor)
        self._run(**kwargs)
