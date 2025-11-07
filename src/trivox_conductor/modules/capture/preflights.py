from __future__ import annotations
import os
import shutil
import ctypes
from ctypes import wintypes
from typing import Optional

from trivox_conductor.common.logger import logger
from trivox_conductor.core.preflights.preflight_types import (
    PreflightContext,
    PreflightFailure,
    Role,
)
from trivox_conductor.core.preflights.preflight_registry import PreflightRegistry


class DiskSpaceCheck:
    id = "capture.disk_space"
    role: Role = "capture"
    default_required = True
    adapter_name: Optional[str] = None   # any capture adapter

    def __call__(self, ctx: PreflightContext) -> Optional[PreflightFailure]:
        settings = ctx.settings
        path_key = settings.get("disk_path_key", "record_dir")
        record_dir = settings.get(path_key)
        if not record_dir:
            logger.debug("capture.preflight_skip - disk: '%s' not set", path_key)
            return None

        min_gb = float(settings.get("min_record_free_gb", 5.0))

        try:
            total, used, free = shutil.disk_usage(record_dir)
        except FileNotFoundError:
            return PreflightFailure(
                id=self.id,
                message=f"record_dir '{record_dir}' does not exist",
                required=True,
            )

        free_gb = free / (1024**3)
        if free_gb < min_gb:
            return PreflightFailure(
                id=self.id,
                message=f"Only {free_gb:.1f}GB free; need >= {min_gb:.1f}GB",
                required=True,
            )
        logger.debug("capture.preflight_ok - disk: %.1fGB free", free_gb)
        return None


PreflightRegistry.register("capture", DiskSpaceCheck())


def _get_foreground_window_title() -> Optional[str]:
    """
    Best-effort foreground window title resolver.

    - On Windows: uses user32.GetForegroundWindow + GetWindowTextW.
    - On non-Windows: returns None (caller can treat as soft skip).
    """
    if os.name != "nt":  # Only implemented for Windows for now
        return None

    # user32.dll bindings
    user32 = ctypes.WinDLL("user32", use_last_error=True)

    GetForegroundWindow = user32.GetForegroundWindow
    GetForegroundWindow.restype = wintypes.HWND

    GetWindowTextLengthW = user32.GetWindowTextLengthW
    GetWindowTextLengthW.argtypes = [wintypes.HWND]
    GetWindowTextLengthW.restype = ctypes.c_int

    GetWindowTextW = user32.GetWindowTextW
    GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    GetWindowTextW.restype = ctypes.c_int

    hwnd = GetForegroundWindow()
    if not hwnd:
        return None

    length = GetWindowTextLengthW(hwnd)
    if length <= 0:
        return None

    buf = ctypes.create_unicode_buffer(length + 1)
    if not GetWindowTextW(hwnd, buf, length + 1):
        return None

    title = buf.value.strip()
    return title or None


class WindowForegroundCheck:
    id = "capture.window_foreground"
    role: Role = "capture"
    default_required = False
    adapter_name: Optional[str] = None  # applies to any capture adapter

    def __call__(self, ctx: PreflightContext) -> Optional[PreflightFailure]:
        settings = ctx.settings
        pattern = settings.get("window_title_contains")
        if not pattern:
            logger.debug("capture.preflight_skip - window_foreground: no pattern set")
            return None

        title = _get_foreground_window_title()
        if title is None:
            # Can't determine foreground window → treat as soft issue,
            # profile can flip `required: true` if they want to block in this case.
            msg = "Could not determine foreground window title on this platform"
            logger.debug("capture.preflight_skip - window_foreground: %s", msg)
            return None

        # Case-insensitive substring match
        if pattern.lower() not in title.lower():
            msg = f"Foreground window '{title}' does not contain '{pattern}'"
            return PreflightFailure(
                id=self.id,
                message=msg,
                required=self.default_required,  # may be overridden by profile
            )

        logger.debug(
            "capture.preflight_ok - window_foreground: '%s' matches '%s'",
            title,
            pattern,
        )
        return None


PreflightRegistry.register("capture", WindowForegroundCheck())
