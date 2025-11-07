"""
Logger filter to ensure that 'classname' attribute is set in log records.
"""

import logging
import sys
from typing import Optional


def _classname_from_locals(locals_) -> Optional[str]:
    self_obj = locals_.get("self")
    if self_obj is not None:
        return type(self_obj).__name__
    cls_obj = locals_.get("cls")
    if isinstance(cls_obj, type):
        return cls_obj.__name__
    return None


class EnsureClassName(logging.Filter):
    """
    Populate record.classname by finding the *emitting* frame:
    we match by (pathname, funcName) and read self/cls from its locals.
    Falls back to "-" when not in a class context (module funcs/staticmethods).
    """

    # TODO: Refactor to reduce complexity
    # Justification: Accessing protected member _getframe of sys is necessary here
    # pylint: disable=protected-access
    def filter(self, record: logging.LogRecord) -> bool:
        # keep any explicitly-provided classname
        if getattr(record, "classname", None):
            return True

        target_path = record.pathname  # absolute path to the file
        target_func = record.funcName  # function name that logged

        # Walk current stack; stop when we match the record’s file+func.
        f = sys._getframe()
        for _ in range(200):  # safety cap
            if f is None:
                break
            code = f.f_code
            if code.co_filename == target_path and code.co_name == target_func:
                clsname = _classname_from_locals(f.f_locals)
                record.classname = clsname or "-"
                return True
            f = f.f_back

        # Fallback: we didn’t find the exact frame (wrappers, C calls, etc.)
        record.classname = "-"
        return True

    # pylint: enable=protected-access
