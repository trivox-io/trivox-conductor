
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
    ]
    
    __doc__ = """
    Capture command for managing capture operations.
    Usage:
        capture --action start --session_id <session_id>
        capture --action stop
    
    Description:
        This command allows you to start or stop capture operations
        using the Capture module.
    
    Arguments:
        --action (str): The action to perform. Choices are 'start', 'stop', 'list_scenes', 'list_profiles'.
        --session_id (str): The session ID for the capture operation.
    """

    def _execute(self, **kwargs):
        # Implement the command execution logic here
        logger.debug(f"Executing CaptureCommand with kwargs: {kwargs}")
        self.set_processor(CaptureCommandProcessor)
        self._run(**kwargs)
