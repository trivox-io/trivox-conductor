"""
Logger utility module.
This module is responsible for providing utility functions for the logger.
"""

from pathlib import Path
from typing import Any, Dict


class LoggerUtils:
    """
    Utility class for the logger.
    """

    @staticmethod
    def deep_merge(
        base: Dict[str, Any], override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Deep merge two dictionaries.

        :param base: The base dictionary.
        :type override: dict

        :param override: The dictionary to merge on top of the base.
        :type base: dict

        :return: The merged dictionary.
        :rtype: dict
        """
        out = dict(base)
        for k, v in override.items():
            if isinstance(v, dict) and isinstance(out.get(k), dict):
                out[k] = LoggerUtils.deep_merge(out[k], v)
            else:
                out[k] = v
        return out

    @staticmethod
    def ensure_handler_dirs(cfg: dict):
        """
        Ensure that directories for file handlers exist.

        :param cfg: The logging configuration dictionary.
        :type cfg: dict
        """
        # Walk through handlers, create parent directories for any filename params.
        for _, hcfg in (cfg.get("handlers") or {}).items():
            filename = hcfg.get("filename")
            if filename:
                try:
                    Path(filename).parent.mkdir(parents=True, exist_ok=True)
                # Justification: Broad except is required to avoid crashes in logging
                # pylint: disable=broad-exception-caught
                except Exception:
                    pass  # let dictConfig surface detailed error later
                # pylint: enable=broad-exception-caught
