"""
Base Handler
"""

from trivox_conductor.ui.common.base_window_controller import (
    BaseWindowController,
)


class BaseHandler:
    """
    Base handler
    """

    def __init__(self, window_controller: BaseWindowController):
        """
        :param window_controller: The window controller
        :type window_controller: BaseWindowController
        """

        self.window_controller = window_controller

    def result_callback(self, result: dict):
        """
        Result callback

        :param result: The result
        :type result: dict
        """

        raise NotImplementedError

    def progress_callback(self, progress: int):
        """
        Progress callback

        :param progress: The progress
        :type progress: int
        """

        raise NotImplementedError

    def pre_process_callback(self):
        """
        Pre process callback
        """

        raise NotImplementedError

    def handle(self):
        """
        Handle the request
        """

        raise NotImplementedError
