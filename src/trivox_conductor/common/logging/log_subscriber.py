"""
Log subscriber module.
This module provides a LogSubscriber class that allows different UI components
or non-UI components to subscribe to log messages.
"""

from typing import Callable, List


class LogSubscriber:
    """
    LogSubscriber class.
    This class allows different UI components or non-UI components to subscribe to log messages.
    """

    def __init__(self):
        self.subscribers: List[Callable[[str], None]] = []

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(LogSubscriber, cls).__new__(cls)
        return cls.instance

    def subscribe(self, callback: Callable[[str], None]):
        """
        Subscribe a new callback to receive log messages.

        :param callback: A function that handles log messages.
        :type callback: Callable[[str], None]
        """

        self.subscribers.append(callback)

    def notify(self, message: str):
        """
        Notify all subscribers with a new log message.

        :param message: The log message.
        :type message: str
        """
        for subscriber in self.subscribers:
            subscriber(message)


log_subscriber = LogSubscriber()
