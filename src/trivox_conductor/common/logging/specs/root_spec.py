"""
Specification for the root logger.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class RootSpec:
    """
    Specification for the root logger.

    :cvar level: The logging level for the root logger.
    :type level: str

    :cvar handlers: List of handler scopes for the root logger.
    :type handlers: List[str]
    """

    level: str = "INFO"
    handlers: List[str] = field(default_factory=list)
