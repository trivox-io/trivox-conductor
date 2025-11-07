from trivox_conductor.common.base_processor import (
    TrivoxCaptureCommandProcessor,
)
from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
from trivox_conductor.core.registry.watcher_registry import WatcherRegistry

from .services import WatcherService


class WatcherCommandProcessor(TrivoxCaptureCommandProcessor):
    """
    Command processor for Watcher module commands.
    """

    ROLE = "watcher"
    SERVICE_CLS = WatcherService
    ACTION_MAP = {
        "start": "start",
        "stop": "stop",
        "on_raw_detect": "on_raw_detect",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._session_id: str = kwargs.get("session_id", None)
        overrides = {}
        self.set_pipeline_profile(overrides)

    def build_service(self):
        return WatcherService(WatcherRegistry, settings)

    def build_call_kwargs(self, action: str) -> dict:
        if action == "start":
            return {
                "session_id": self._session_id,
                "overrides": self._overrides,
            }
        return {}

    def run(self):
        # Implement the command processing logic here
        logger.debug("Running ReplayCommandProcessor")
        return super().run()
