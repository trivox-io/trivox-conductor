"""
Specification for logging formatters.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class FormatterSpec:
    """
    Specification for a logging formatter.

    :cvar class_name: The class name of the formatter.
    :type class_name: Optional[str]

    :cvar scope: The scope of the formatter.
    :type scope: Optional[str]

    :cvar params: Additional parameters for the formatter.
    :type params: Dict[str, Any]
    """

    class_name: Optional[str] = None
    scope: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)
