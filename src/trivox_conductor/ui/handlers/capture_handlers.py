from trivox_conductor.common.logger import logger
from trivox_conductor.common.strategies import StrategyRegistry
from trivox_conductor.ui.common.base_handler import BaseHandler


class StartCaptureHandler(BaseHandler):
    """
    Start Capture Handler
    """

    def result_callback(self, result: dict):
        """
        Result callback

        :param result: The result
        :type result: dict
        """
        logger.info("Capture result received.")

    def progress_callback(self, progress: int):
        """
        Progress callback

        :param progress: The progress
        :type progress: int
        """
        logger.info(f"Capture progress: {progress}%")

    def pre_process_callback(self):
        """
        Pre process callback
        """
        logger.info("Preparing to start capture...")

    def handle(self):
        """
        Handle the request
        """
        strategy_cls = StrategyRegistry.get("capture-strategy")
        if not strategy_cls:
            logger.warning("Capture strategy not found")
            raise ValueError("Capture strategy not found")

        strategy = strategy_cls(self.window_controller)
        strategy.execution_finished.connect(self.result_callback)
        strategy.execution_finished.connect(
            lambda result: logger.info("Capture started.")
        )
        self.pre_process_callback()
        strategy.execute(action="start")


class StopCaptureHandler(BaseHandler):
    """
    Stop Capture Handler
    """

    def result_callback(self, result: dict):
        """
        Result callback

        :param result: The result
        :type result: dict
        """
        logger.info("Capture result received.")

    def progress_callback(self, progress: int):
        """
        Progress callback

        :param progress: The progress
        :type progress: int
        """
        logger.info(f"Capture progress: {progress}%")

    def pre_process_callback(self):
        """
        Pre process callback
        """
        logger.info("Preparing to stop capture...")

    def handle(self):
        """
        Handle the request
        """
        strategy_cls = StrategyRegistry.get("capture-strategy")
        if not strategy_cls:
            logger.warning("Capture strategy not found")
            raise ValueError("Capture strategy not found")

        strategy = strategy_cls(self.window_controller)
        strategy.execution_finished.connect(
            lambda result: logger.info("Capture stopped.")
        )
        strategy.execute(action="stop")
