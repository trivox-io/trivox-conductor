
from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
from trivox_conductor.common.base_processor import TrivoxCaptureCommandProcessor
from trivox_conductor.core.registry.watcher_registry import WatcherRegistry

from .services import ReplayWatcherService


class ReplayCommandProcessor(TrivoxCaptureCommandProcessor):
    """
    Command processor for Replay module commands.
    """
    
    def __init__(self, **kwargs):
        self._action: str = kwargs.get("action", "")
        self._session_id: str = kwargs.get("session_id", None)
    
    def run(self):
        # Implement the command processing logic here
        logger.debug("Running ReplayCommandProcessor")

        svc = ReplayWatcherService(WatcherRegistry, settings)

        ops = {
            "start": lambda: svc.start(self._session_id),
            "stop": svc.stop,
            "on_raw_detect": svc.on_raw_detect,
        }
        try:
            fn = ops[self._action]
        except KeyError as e:
            raise ValueError(f"Unknown action: {self._action}") from e

        result = fn()
        logger.info(f"replay.action - {self._action} - {self._session_id}")
        return result
