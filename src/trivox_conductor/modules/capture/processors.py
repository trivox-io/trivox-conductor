
from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
from trivox_conductor.common.base_processor import TrivoxCaptureCommandProcessor
from trivox_conductor.core.registry.capture_registry import CaptureRegistry

from .services import CaptureService


class CaptureCommandProcessor(TrivoxCaptureCommandProcessor):
    """
    Command processor for Capture module commands.
    """
    
    def __init__(self, **kwargs):
        self._action: str = kwargs.get("action", "")
        self._session_id: str = kwargs.get("session_id", None)
    
    def run(self):
        # Implement the command processing logic here
        logger.debug("Running CaptureCommandProcessor")

        svc = CaptureService(CaptureRegistry, settings)

        ops = {
            "start": lambda: svc.start(self._session_id),
            "stop": svc.stop,
            "list_scenes": svc.list_scenes,
            "list_profiles": svc.list_profiles,
        }
        try:
            fn = ops[self._action]
        except KeyError as e:
            raise ValueError(f"Unknown action: {self._action}") from e

        result = fn()
        logger.info(f"capture.action - {self._action} - {self._session_id}")
        return result
