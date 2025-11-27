from trivox_conductor.common.strategies import BaseStrategy, register_strategy

from .workers import CaptureWorker


@register_strategy
class CaptureStrategy(BaseStrategy):
    """
    Capture strategy
    """

    name = "capture-strategy"

    def execute(self, *args, **kwargs):
        """
        Execute the capture strategy
        """

        self.worker = CaptureWorker(
            process_result_callback=self.process_result_callback,
            *args,
            **kwargs,
        )
        self.worker.execute()
