from trivox_conductor.common.base_command import TrivoxConductorCommand
from trivox_conductor.common.commands.argument_type import ArgumentType
from trivox_conductor.common.commands.base_command import register_command
from trivox_conductor.common.logger import logger

from .processors import AIBrainCommandProcessor


@register_command()
class AICommand(TrivoxConductorCommand):
    """
    Command for AI module.
    """

    name = "ai"
    args = [
        ArgumentType(
            "action",
            str,
            "Action",
            choices=("generate", "markers"),
            required=True,
        ),
    ]

    __doc__ = """
    AI command for managing ai operations.
    Usage:
        ai --action generate
        ai --action markers
    
    Description:
        This command allows you to generate ai content or create beat markers
        using the AI module.
    
    Arguments:
        --action (str): The action to perform. Choices are 'generate', 'markers'.
        --session_id (str): The session ID for the ai operation.
    """

    def _execute(self, **kwargs):
        # Implement the command execution logic here
        logger.debug(f"Executing AICommand with kwargs: {kwargs}")
        self.set_processor(AIBrainCommandProcessor)
        self._run(**kwargs)
