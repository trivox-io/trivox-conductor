"""
Specification for a logger.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class LoggerSpec:
    """
    Specification for a logger.

    :cvar level: The logging level for the logger.
    :type level: str

    :cvar propagate: Whether the logger propagates messages to ancestor loggers.
    :type propagate: bool

    :cvar handlers: List of handler scopes for the logger.
    :type handlers: List[str]
    """

    level: str = "INFO"
    propagate: bool = True
    handlers: List[str] = field(default_factory=list)
