from trivox_conductor.common.base_command import TrivoxConductorCommand
from trivox_conductor.common.commands.argument_type import ArgumentType
from trivox_conductor.common.commands.base_command import register_command
from trivox_conductor.common.logger import logger

from .processors import HandoffCommandProcessor


@register_command()
class HandoffCommand(TrivoxConductorCommand):
    """
    Command for Handoff module.
    """

    name = "handoff"
    args = [
        ArgumentType(
            "action",
            str,
            "Action",
            choices=("upload_clip", "notify_upload_done"),
            required=True,
        ),
    ]

    __doc__ = """
    Handoff command for managing handoff operations.
    Usage:
        handoff --action upload_clip
        handoff --action notify_upload_done
    
    Description:
        This command allows you to upload clips using the Handoff module.
    
    Arguments:
        --action (str): The action to perform. Choices are 'upload_clip', 'notify_upload_done'.
    """

    def _execute(self, **kwargs):
        # Implement the command execution logic here
        logger.debug(f"Executing HandoffCommand with kwargs: {kwargs}")
        self.set_processor(HandoffCommandProcessor)
        self._run(**kwargs)
