"""
Console color formatter module.
"""

import logging


class ConsoleColorFormatter(logging.Formatter):
    """
    A custom console formatter for the logger.

    This formatter allows log messages to be formatted with ANSI escape codes for colors
    based on the log level.
    """

    COLORS = {
        logging.ERROR: "\033[91m",  # Red
        logging.DEBUG: "\033[96m",  # Cyan
        logging.INFO: "\033[97m",  # White
        logging.WARNING: "\033[93m",  # Yellow
        logging.CRITICAL: "\033[95m",  # Magenta
        "RESET": "\033[0m",  # Reset color
    }

    def __init__(self, fmt=None, datefmt=None, style="%"):
        """
        :param fmt: The format string for the log message.
        :type fmt: str, optional

        :param datefmt: The format string for the date.
        :type datefmt: str, optional

        :param style: The style for the format string.
        :type style: str, optional
        """
        super().__init__(fmt, datefmt, style)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record with ANSI escape codes.

        This method formats the log record using ANSI escape codes for colors
        based on the log level.

        :param record: The log record to be formatted.
        :type record: logging.LogRecord

        :return: The formatted log message as a string with ANSI escape codes.
        :rtype: str
        """

        color = ConsoleColorFormatter.COLORS.get(
            record.levelno, ConsoleColorFormatter.COLORS["RESET"]
        )
        formatted_record = super().format(record)
        return (
            f"{color}{formatted_record}{ConsoleColorFormatter.COLORS['RESET']}"
        )
