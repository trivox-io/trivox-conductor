
from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
from trivox_conductor.common.base_processor import TrivoxCaptureCommandProcessor
from trivox_conductor.core.registry.ai_registry import AIRegistry

from .services import AIBrainService, BeatMarkerService


class AIBrainCommandProcessor(TrivoxCaptureCommandProcessor):
    """
    Command processor for AI Brain module commands.
    """
    
    def __init__(self, **kwargs):
        self._action: str = kwargs.get("action", "")
    
    def run(self):
        # Implement the command processing logic here
        logger.debug("Running AIBrainCommandProcessor")

        if self._action == "generate":
            svc = AIBrainService(AIRegistry, settings)
        elif self._action == "markers":
            svc = BeatMarkerService(AIRegistry, settings)

        ops = {
            "generate": lambda: svc.generate({}),
            "markers": lambda: svc.markers_from_features({}),
        }
        try:
            fn = ops[self._action]
        except KeyError as e:
            raise ValueError(f"Unknown action: {self._action}") from e

        result = fn()
        logger.info(f"ai.action - {self._action} - {result}")
        return result
