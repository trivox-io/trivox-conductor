from trivox_conductor.common.base_processor import (
    TrivoxCaptureCommandProcessor,
)
from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
from trivox_conductor.core.registry.color_registry import ColorRegistry

from .services import ColorService


class ColorCommandProcessor(TrivoxCaptureCommandProcessor):
    """
    Command processor for Color module commands.
    """

    def __init__(self, **kwargs):
        self._action: str = kwargs.get("action", "")

    def run(self):
        # Implement the command processing logic here
        logger.debug("Running ColorCommandProcessor")

        svc = ColorService(ColorRegistry, settings)

        ops = {
            "color_pass": lambda: svc.color_pass(""),
        }
        try:
            fn = ops[self._action]
        except KeyError as e:
            raise ValueError(f"Unknown action: {self._action}") from e

        result = fn()
        logger.info(f"color.action - {self._action}")
        return result
