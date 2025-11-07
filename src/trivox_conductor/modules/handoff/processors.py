from trivox_conductor.common.base_processor import (
    TrivoxCaptureCommandProcessor,
)
from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
from trivox_conductor.core.registry.notifier_registry import NotifierRegistry
from trivox_conductor.core.registry.uploader_registry import UploaderRegistry

from .services import NotifierService, UploaderService


class HandoffCommandProcessor(TrivoxCaptureCommandProcessor):
    """
    Command processor for Handoff module commands.
    """

    def __init__(self, **kwargs):
        self._action: str = kwargs.get("action", "")

    def run(self):
        # Implement the command processing logic here
        logger.debug("Running HandoffCommandProcessor")

        if self._action == "upload_clip":
            svc = UploaderService(UploaderRegistry, settings)
        elif self._action == "notify_upload_done":
            svc = NotifierService(NotifierRegistry, settings)

        ops = {
            "upload_clip": lambda: svc.upload_clip("", ""),
            "notify_upload_done": lambda: svc.notify_upload_done("", ""),
        }
        try:
            fn = ops[self._action]
        except KeyError as e:
            raise ValueError(f"Unknown action: {self._action}") from e

        result = fn()
        logger.info(f"handoff.action - {self._action}")
        return result
