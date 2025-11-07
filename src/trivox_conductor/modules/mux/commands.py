from trivox_conductor.common.base_command import TrivoxConductorCommand
from trivox_conductor.common.commands.argument_type import ArgumentType
from trivox_conductor.common.commands.base_command import register_command
from trivox_conductor.common.logger import logger

from .processors import MuxCommandProcessor


@register_command()
class MuxCommand(TrivoxConductorCommand):
    """
    Command for Mux module.
    """

    name = "mux"
    args = [
        ArgumentType(
            "action", str, "Action", choices=("mux_clip"), required=True
        ),
        ArgumentType(
            "session_id", str, "Session ID", default="20251029_1050_s0_e0_test"
        ),
    ]

    __doc__ = """
    Mux command for managing mux operations.
    Usage:
        mux --action mux_clip --session_id <session_id>
    
    Description:
        This command allows you to perform mux operations
        using the Mux module.
    
    Arguments:
        --action (str): The action to perform. Choices are 'mux_clip'.
        --session_id (str): The session ID for the mux operation.
    """

    def _execute(self, **kwargs):
        # Implement the command execution logic here
        logger.debug(f"Executing MuxCommand with kwargs: {kwargs}")
        self.set_processor(MuxCommandProcessor)
        self._run(**kwargs)
