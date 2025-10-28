"""
Exceptions module for command errors.
"""


class CommandException(Exception):
    """
    Exception for command errors.
    """

    def __init__(self, message: str, exit_code: int = 2):
        super().__init__(message)
        self.exit_code = exit_code
