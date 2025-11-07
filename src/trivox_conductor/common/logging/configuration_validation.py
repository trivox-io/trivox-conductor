"""
Configuration validation for logging.
"""


class ConfigValidation:
    """
    Validate logging config dict for internal consistency:
    1) handlers reference existing formatter & filters
    2) root & loggers reference existing handlers
    """

    @staticmethod
    def _check_handler_list(where: str, names, hdl_names: set):
        for hn in names:
            if hn not in hdl_names:
                raise ValueError(f"{where} references missing handler '{hn}'")

    # TODO: Refactor to reduce complexity
    @staticmethod
    def validate(cfg: dict):
        """
        Validate logging config dict for internal consistency.

        :param cfg: Logging configuration dictionary.
        :type cfg: dict

        :raises ValueError: If any references are missing.
        """
        fmt_names = set((cfg.get("formatters") or {}).keys())
        filt_names = set((cfg.get("filters") or {}).keys())
        hdl = cfg.get("handlers") or {}
        hdl_names = set(hdl.keys())

        for name, h in hdl.items():
            f = h.get("formatter")
            if f and f not in fmt_names:
                raise ValueError(
                    f"Handler '{name}' references missing formatter '{f}'"
                )
            for flt in h.get("filters", []) or []:
                if flt not in filt_names:
                    raise ValueError(
                        f"Handler '{name}' references missing filter '{flt}'"
                    )

        ConfigValidation._check_handler_list(
            "root.handlers",
            (cfg.get("root") or {}).get("handlers", []),
            hdl_names,
        )
        for lname, lcfg in (cfg.get("loggers") or {}).items():
            ConfigValidation._check_handler_list(
                f"logger '{lname}'.handlers",
                lcfg.get("handlers", []),
                hdl_names,
            )
