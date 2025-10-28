"""
Console stream handler for logging.
Sends formatted log lines to LogSubscriber (not stdout redirection).
"""

import logging

from trivox_conductor.common.logging.log_subscriber import log_subscriber


class ConsoleStreamHandler(logging.Handler):
    """Send formatted log lines to LogSubscriber (not stdout redirection)."""

    def emit(self, record: logging.LogRecord):
        try:
            line = self.format(record)
            # Justification: Broad except is required to avoid crashes in logging
        # pylint: disable=broad-exception-caught
        except Exception:
            self.handleError(record)
            return
        # pylint: enable=broad-exception-caught
        log_subscriber.notify(line)
