"""
Specification manager for logging configurations.
This module provides the SpecManager class to manage logging specifications
and convert them to dictionary configurations suitable for logging.config.dictConfig.
"""

import os
from typing import Any, Dict

from .formatter_spec import FormatterSpec
from .handler_spec import HandlerSpec
from .logging_spec import LoggingSpec
from .root_spec import RootSpec

DEFAULT_FORMAT = (
    "%(asctime)s [%(levelname)-8.8s] [%(name)s] "
    "%(module)s.%(classname)s.%(funcName)s: "
    "%(message)s (%(filename)s:%(lineno)d)"
)


class SpecManager:
    """
    Manages logging specifications and provides methods to convert them to
    dictionary configurations suitable for logging.config.dictConfig.
    """

    def __init__(self):
        self._spec = self._default_spec()

    def _default_spec(self) -> LoggingSpec:
        """
        Create a default LoggingSpec with sensible defaults.

        :return: A LoggingSpec instance with default configuration.
        :rtype: LoggingSpec
        """
        spec = LoggingSpec()
        spec.filters["ensure_classname"] = {
            "()": "trivox_conductor.common.logging.filters.EnsureClassName"
        }
        spec.formatters["console_color"] = FormatterSpec(
            class_name="trivox_conductor.common.logging.formatters.ConsoleColorFormatter",
            scope="console_color",
            params={
                "fmt": DEFAULT_FORMAT,  # reuse your rich format
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        )
        spec.handlers["console_stream"] = HandlerSpec(
            class_name="logging.StreamHandler",
            level="DEBUG",
            formatter="console_color",
            filters=["ensure_classname"],
            params={"stream": "ext://sys.stdout"},
        )
        spec.handlers["file"] = HandlerSpec(
            class_name="logging.handlers.RotatingFileHandler",
            level="DEBUG",
            formatter="console_color",  # not "rich"
            filters=["ensure_classname"],
            params={
                # TODO: This path should be configurable
                "filename": ".trivox_conductor/logs/trivox_conductor.log",
                "maxBytes": 5_000_000,
                "backupCount": 3,
                "encoding": "utf-8",
                "delay": True,  # delay opening until first emit
            },
        )
        spec.handlers["socket"] = HandlerSpec(
            class_name="trivox_conductor.common.logging.handlers.RobustSocketLogger",
            scope="socket_handler",
            level="DEBUG",
            formatter="console_color",
            filters=["ensure_classname"],
            params={
                "host": "127.0.0.1",
                "port": 9999,
                "queue_maxsize": 5000,
                "fallback_file": (
                    os.path.join(
                        os.getenv("APPDATA", "C:\\Temp"),
                        "Trivox",
                        "logs",
                        "producer_fallback.log",
                    )
                ),
                "backoff_min": 0.25,
                "backoff_max": 8.0,
            },
        )
        spec.root = RootSpec(
            level="DEBUG", handlers=["console_stream", "file"]
        )
        self._spec = spec
        return spec

    def to_dict_config(self) -> Dict[str, Any]:
        """
        Convert a LoggingSpec dataclass to a dictionary suitable for logging.config.dictConfig.

        :param cfg: The LoggingSpec dataclass instance.
        :type cfg: LoggingSpec

        :return: A dictionary representation of the logging configuration.
        :rtype: dict
        """
        return {
            "version": 1,
            "disable_existing_loggers": self._spec.disable_existing_loggers,
            "filters": self._spec.filters,
            "formatters": {
                k: self._fmt_entry(v) for k, v in self._spec.formatters.items()
            },
            "handlers": {
                k: self._handler_entry(v)
                for k, v in self._spec.handlers.items()
            },
            "loggers": {
                k: {
                    "level": v.level,
                    "propagate": v.propagate,
                    "handlers": v.handlers,
                }
                for k, v in self._spec.loggers.items()
            },
            "root": {
                "level": self._spec.root.level,
                "handlers": self._spec.root.handlers,
            },
        }

    def _fmt_entry(self, spec: FormatterSpec) -> Dict[str, Any]:
        if spec.class_name:
            return {"()": spec.class_name, **spec.params}
        if spec.scope:
            return {
                "()": f"{__name__}.endpoint_formatter_factory",
                "scope": spec.scope,
                **spec.params,
            }
        raise ValueError("FormatterSpec needs 'class_name' or 'scope'")

    def _handler_entry(self, spec: HandlerSpec) -> Dict[str, Any]:
        if spec.class_name:
            d = {"class": spec.class_name}
        elif spec.scope:
            d = {
                "()": f"{__name__}.endpoint_handler_factory",
                "scope": spec.scope,
            }
        else:
            raise ValueError("HandlerSpec needs 'class_name' or 'scope'")
        if spec.level:
            d["level"] = spec.level
        if spec.formatter:
            d["formatter"] = spec.formatter
        if spec.filters:
            d["filters"] = spec.filters
        d.update(spec.params)
        return d
