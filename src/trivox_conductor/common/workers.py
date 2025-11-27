"""
Worker classes for the IC Inspector application.
"""

import threading
from abc import ABC, abstractmethod
from typing import Optional

from PySide6 import QtCore


class BaseWorkerThread(QtCore.QThread):
    """
    Base class for all worker threads
    """

    return_signal = return_signal = QtCore.Signal(dict)

    _is_running = False

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setTerminationEnabled(True)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Run the worker thread
        """

        self._is_running = True
        result = self.perform_task(*self.args, **self.kwargs)
        self.return_signal.emit(result)

    def perform_task(self, *args, **kwargs):
        """
        Perform the task of the worker thread
        """

        raise NotImplementedError

    def stop(self):
        """
        Stop the worker thread
        """
        self._is_running = False
        try:
            self.quit()
            self.wait()
        except RuntimeError:
            pass

    def __del__(self):
        self.stop()


class BaseWorker(ABC):
    """
    Base class for all workers
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.worker: Optional[BaseWorkerThread] = None

    def _handle_worker_result(self, result: dict):
        """
        Handle the result of the worker thread

        :param result: The result of the worker thread
        :type result: dict
        """

        self.process_result_callback(result)

    def _check_worker_status(self, worker: BaseWorkerThread):
        """
        Check the status of the worker thread

        :param worker: The worker thread to check
        :type worker: BaseWorkerThread
        """

        if worker.isRunning():
            threading.Timer(0.1, self._check_worker_status, [worker]).start()

    @abstractmethod
    def process_result_callback(self, result: dict):
        """
        Process the result of the worker thread

        :param result: The result of the worker thread
        :type result: dict
        """

        raise NotImplementedError

    def execute(self):
        """
        Execute the worker
        """

        raise NotImplementedError
