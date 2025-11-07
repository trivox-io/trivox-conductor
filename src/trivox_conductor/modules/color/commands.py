from trivox_conductor.common.base_command import TrivoxConductorCommand
from trivox_conductor.common.commands.argument_type import ArgumentType
from trivox_conductor.common.commands.base_command import register_command
from trivox_conductor.common.logger import logger

from .processors import ColorCommandProcessor


@register_command()
class ColorCommand(TrivoxConductorCommand):
    """
    Command for Color module.
    """

    name = "color"
    args = [
        ArgumentType(
            "action", str, "Action", choices=("color_pass"), required=True
        ),
    ]

    __doc__ = """
    Color command for managing color operations.
    Usage:
        color --action color_pass --src_path <src_path>
    
    Description:
        This command allows you to perform color operations
        using the Color module.
    
    Arguments:
        --action (str): The action to perform. Choices are 'color_pass'.
    """

    def _execute(self, **kwargs):
        # Implement the command execution logic here
        logger.debug(f"Executing ColorCommand with kwargs: {kwargs}")
        self.set_processor(ColorCommandProcessor)
        self._run(**kwargs)
