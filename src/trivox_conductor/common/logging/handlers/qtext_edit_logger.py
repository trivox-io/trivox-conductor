"""
Logger module for redirecting log messages to a QTextEdit widget.
"""

import logging
import sys
from typing import Callable

from trivox_conductor.common.logging.log_subscriber import log_subscriber


class ConsoleStream:
    """
    ConsoleStream class.

    This class redirects stdout and stderr to callback functions, allowing log messages
    to be displayed in various UIs or even handled programmatically.
    """

    _stdout = None
    _stderr = None

    def __init__(self, write_callback: Callable[[str], None] = None):
        """
        :param write_callback: A function to handle writing the log messages.
        :type write_callback: Callable[[str], None]
        """
        self.write_callback = write_callback

    def write(self, message: str):
        """
        Write a message to the stream.

        :param message: The message to write.
        :type message: str
        """
        if self.write_callback:
            self.write_callback(message)

    @staticmethod
    def stdout(
        write_callback: Callable[[str], None] = None,
    ) -> "ConsoleStream":
        """
        Get the singleton instance for stdout redirection.

        :param write_callback: A function to handle writing the log messages.
        :type write_callback: Callable[[str], None]

        :return: The singleton instance for stdout redirection.
        :rtype: ConsoleStream
        """
        if not ConsoleStream._stdout:
            ConsoleStream._stdout = ConsoleStream(write_callback)
            sys.stdout = ConsoleStream._stdout
        return ConsoleStream._stdout

    @staticmethod
    def stderr(
        write_callback: Callable[[str], None] = None,
    ) -> "ConsoleStream":
        """
        Get the singleton instance for stderr redirection.

        :param write_callback: A function to handle writing the log messages.
        :type write_callback: Callable[[str], None]

        :return: The singleton instance for stderr redirection.
        :rtype: ConsoleStream
        """
        if not ConsoleStream._stderr:
            ConsoleStream._stderr = ConsoleStream(write_callback)
            sys.stderr = ConsoleStream._stderr
        return ConsoleStream._stderr

    def flush(self):
        """
        Flush the stream.

        This method is a no-op, provided for compatibility with file-like objects.
        """


class QtLogger(logging.Handler):
    """
    QtLogger class.

    This custom logging handler emits log records to the ConsoleStream, allowing
    log messages to be displayed in a QTextEdit widget.
    """

    def __init__(self):
        super().__init__()

    def emit(self, record: logging.LogRecord):
        """
        Emit a log record.

        :param record: The log record to emit.
        :type record: logging.LogRecord
        """
        log_entry = self.format(record)
        log_subscriber.notify(log_entry)
