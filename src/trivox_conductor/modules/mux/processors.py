from trivox_conductor.common.base_processor import (
    TrivoxCaptureCommandProcessor,
)
from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
from trivox_conductor.core.registry.mux_registry import MuxRegistry

from .services import MuxService


class MuxCommandProcessor(TrivoxCaptureCommandProcessor):
    """
    Command processor for Mux module commands.
    """

    def __init__(self, **kwargs):
        self._action: str = kwargs.get("action", "")
        self._session_id: str = kwargs.get("session_id", None)

    def run(self):
        # Implement the command processing logic here
        logger.debug("Running CaptureCommandProcessor")

        svc = MuxService(MuxRegistry, settings)

        ops = {
            "mux_clip": lambda: svc.mux_clip("", {}, None, self._session_id),
        }
        try:
            fn = ops[self._action]
        except KeyError as e:
            raise ValueError(f"Unknown action: {self._action}") from e

        result = fn()
        logger.info(f"mux.action - {self._action} - {self._session_id}")
        return result
