"""
Specification for logging configuration.
"""

from dataclasses import dataclass, field
from typing import Any, Dict

from .formatter_spec import FormatterSpec
from .handler_spec import HandlerSpec
from .logger_spec import LoggerSpec
from .root_spec import RootSpec


@dataclass
class LoggingSpec:
    """
    Specification for logging configuration.

    :cvar disable_existing_loggers: Whether to disable existing loggers.
    :type disable_existing_loggers: bool

    :cvar filters: Dictionary of filter specifications.
    :type filters: Dict[str, Dict[str, Any]]

    :cvar formatters: Dictionary of formatter specifications.
    :type formatters: Dict[str, FormatterSpec]

    :cvar handlers: Dictionary of handler specifications.
    :type handlers: Dict[str, HandlerSpec]

    :cvar loggers: Dictionary of logger specifications.
    :type loggers: Dict[str, LoggerSpec]

    :cvar root: Specification for the root logger.
    :type root: RootSpec
    """

    disable_existing_loggers: bool = False
    filters: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    formatters: Dict[str, FormatterSpec] = field(default_factory=dict)
    handlers: Dict[str, HandlerSpec] = field(default_factory=dict)
    loggers: Dict[str, LoggerSpec] = field(default_factory=dict)
    root: RootSpec = field(default_factory=RootSpec)
