"""
HTML Formatter for the ICTools logger.
"""

import logging


class HTMLFormatter(logging.Formatter):
    """
    A custom HTML formatter for the logger.

    This formatter allows log messages to be formatted with HTML, including custom colors
    based on the log level. It supports dynamic formatting using specified format keys.
    """

    COLORS = {
        logging.ERROR: "#FF6B68",  # ~ Red
        logging.DEBUG: "#299999",  # ~ Cyan
        logging.INFO: "#D1CDCD",  # ~ Grey
        logging.WARNING: "#C07223",  # ~ Ginger
        logging.CRITICAL: "#FF00FF",  # ~ Magenta
    }

    def __init__(self, *_args, fmt_keys: dict[str, str] = None):
        """
        :param args: Additional arguments for the base Formatter class.

        :param fmt_keys: A dictionary containing format keys for customizing the log message format.
        :type fmt_keys: dict[str, str], optional
        """
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    # Justification: Accessing protected member _style of class Formatter is necessary here
    # pylint: disable=protected-access
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record as HTML.

        This method formats the log record using HTML, applying custom colors based on the log level
        and using the specified format keys.

        :param record: The log record to be formatted.
        :type record: logging.LogRecord

        :return: The formatted log message as an HTML string.
        :rtype: str
        """
        last_fmt = self._style._fmt

        color = HTMLFormatter.COLORS.get(record.levelno)
        if color:
            font = self.fmt_keys.get("font")
            fmt = self.fmt_keys.get("format")
            self._style._fmt = font.format(color, fmt)

        res = logging.Formatter.format(self, record)
        self._style._fmt = last_fmt
        return res

    # pylint: enable=protected-access
