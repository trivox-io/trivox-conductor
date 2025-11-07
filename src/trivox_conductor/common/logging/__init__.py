"""
Trivox Conductor Logger Package
"""

import logging
import logging.config
import queue as _q
from logging.handlers import QueueHandler, QueueListener
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml

from .configuration_validation import ConfigValidation
from .logger_utils import LoggerUtils
from .specs.spec_manager import SpecManager


def setup_logging(
    config: Optional[Dict[str, Any]] = None,
    *,
    config_path: Optional[Union[str, Path]] = None,
    overrides: Optional[Dict[str, Any]] = None,
    enable_queue: bool = False,
):
    """
    Set up logging configuration.
    Accepts:
      - dictConfig dict,
      - or YAML file via `config_path`,
      - or nothing → builds sane defaults.
    `overrides` can patch/merge on top of whatever is loaded.

    :param config: A dictionary representing the logging configuration.
    :type config: dict, optional

    :param config_path: Path to a YAML file containing the logging configuration.
    :type config_path: str or Path, optional

    :param overrides: A dictionary to override specific parts of the logging configuration.
    :type overrides: dict, optional

    :param enable_queue: Whether to enable queue-based logging.
    :type enable_queue: bool, optional
    """
    if config is None and config_path:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

    if not config:
        # Build from dataclasses for maintainability
        spec_manager = SpecManager()
        config = spec_manager.to_dict_config()

    if overrides:
        config = LoggerUtils.deep_merge(config, overrides)

    # optional: create directories for file handlers
    LoggerUtils.ensure_handler_dirs(config)

    # validate references before dictConfig
    ConfigValidation.validate(config)

    logging.config.dictConfig(config)

    if enable_queue:
        q = _q.Queue(-1)
        root = logging.getLogger()
        handlers = root.handlers[:]
        root.handlers.clear()
        root.addHandler(QueueHandler(q))
        listener = QueueListener(q, *handlers, respect_handler_level=True)
        listener.start()
