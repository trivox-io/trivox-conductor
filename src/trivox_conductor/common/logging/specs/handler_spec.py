"""
Specification for logging handlers.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class HandlerSpec:
    """
    Specification for a logging handler.

    :cvar class_name: The class name of the handler.
    :type class_name: Optional[str]

    :cvar scope: The scope of the handler.
    :type scope: Optional[str]

    :cvar level: The logging level for the handler.
    :type level: Optional[str]

    :cvar formatter: The formatter scope for the handler.
    :type formatter: Optional[str]

    :cvar filters: List of filter scopes for the handler.
    :type filters: List[str]

    :cvar params: Additional parameters for the handler.
    :type params: Dict[str, Any]
    """

    class_name: Optional[str] = None
    scope: Optional[str] = None
    level: Optional[str] = None
    formatter: Optional[str] = None
    filters: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)
