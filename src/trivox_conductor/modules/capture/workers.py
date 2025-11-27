from typing import Dict

from trivox_conductor.common.logger import logger
from trivox_conductor.common.settings import settings
from trivox_conductor.common.workers import BaseWorker, BaseWorkerThread
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
from trivox_conductor.core.trivox_context import trivox_context

from .services import CaptureService


class CaptureWorkerThread(BaseWorkerThread):
    """
    QThread that runs the CaptureService in the background.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        session = trivox_context.session
        self._service = CaptureService(
            CaptureRegistry,
            settings,
            session_id=session.id,
            pipeline_profile=trivox_context.profile,
            profile_overrides=trivox_context.overrides,
        )
        self.AVAILABLE_ACTIONS_MAP = {
            "start": self._service.start,
            "stop": self._service.stop,
        }

    def perform_task(self, *_args, **kwargs) -> Dict:
        logger.info("Starting Log Collector processor...")
        action = kwargs.get("action", None)
        logger.info(f"Performing action: {action}")
        if action is None or action not in self.AVAILABLE_ACTIONS_MAP:
            logger.error(f"Invalid action: {action}")
            return {"status": "error", "message": f"Invalid action: {action}"}
        self.AVAILABLE_ACTIONS_MAP[action]()
        return {
            "status": "success",
            "message": f"Action '{action}' completed successfully.",
        }


class CaptureWorker(BaseWorker):
    """
    Wrapper around CaptureWorkerThread for the BaseWorker API.
    """

    def __init__(self, process_result_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._process_result_callback = process_result_callback

    def process_result_callback(self, result: dict):
        logger.info(f"Log Collector result received: {result}")
        self._process_result_callback(result)

    def execute(self):
        """
        Start the worker thread.
        """
        self.worker = CaptureWorkerThread(*self.args, **self.kwargs)
        self.worker.return_signal.connect(self._handle_worker_result)
        self.worker.start()
        self._check_worker_status(self.worker)
