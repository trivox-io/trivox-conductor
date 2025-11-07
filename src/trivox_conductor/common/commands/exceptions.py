"""
Exceptions module for command errors.
"""

from __future__ import annotations


class CommandException(Exception):
    """
    Exception for command errors.
    """

    def __init__(self, message: str, exit_code: int = 2):
        """
        :param message: The error message.
        :type message: str

        :param exit_code: The exit code for the exception.
        :type exit_code: int
        """
        super().__init__(message)
        self.exit_code = exit_code
