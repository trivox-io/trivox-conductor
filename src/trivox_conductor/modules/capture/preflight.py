"""
Capture Preflight Checks
========================

Stateless, testable health probes executed before starting a capture session.
Keeps side effects minimal and delegates device/SDK specifics to the adapter.

Checks
------
- ``check_obs_health(adapter)``: uses the adapter's ``health()`` to verify reachability.
- ``check_disk_space(path, min_gb)``: placeholder for storage capacity checks.
- ``check_minecraft_foreground()``: placeholder for UX gating (optional).

Design
------
- Return ``(ok: bool, message: str)`` for simple branching and log friendliness.
- Avoid raising; let the service aggregate results and decide on failure policy.
"""

# TODO: This is deprecated in favor of preflight checks in
# core/preflights/ and modules/capture/preflights.py
from __future__ import annotations

import os
import platform
import shutil
from typing import Iterable, Tuple

try:
    import psutil  # type: ignore
except ImportError:  # keep preflight import-safe if psutil is missing
    psutil = None  # type: ignore


from trivox_conductor.core.contracts.capture import CaptureAdapter


class CapturePreflight:
    """
    Stateless checks before starting capture. Keeps I/O minimal for testability.
    """

    def check_disk_space(
        self, path: str, min_gb: float = 5.0
    ) -> Tuple[bool, str]:
        """
        Check if there is sufficient disk space at the given path.

        :param path: Filesystem path to check.
        :type path: str

        :param min_gb: Minimum required free space in gigabytes.
        :type min_gb: float

        :return: Tuple of (is_ok, message).
        :rtype: Tuple[bool, str]
        """
        try:
            check_path = (
                path if os.path.exists(path) else os.path.dirname(path) or "."
            )
            _, _u, free = shutil.disk_usage(check_path)
            free_gb = free / (1024**3)
            if free_gb >= float(min_gb):
                return (
                    True,
                    f"disk-ok: {free_gb:.2f} GB free >= {min_gb:.2f} GB",
                )
            return False, f"disk-low: {free_gb:.2f} GB free < {min_gb:.2f} GB"
        except Exception as e:
            # Don’t hard fail; surface a readable message.
            return False, f"disk-check-error: {e}"

    def check_obs_health(self, adapter: CaptureAdapter) -> Tuple[bool, str]:
        """
        Check if the OBS adapter is healthy and reachable.

        :return: Tuple of (is_ok, message).
        :rtype: Tuple[bool, str]
        """
        res = adapter.health()
        return bool(res.get("ok")), str(res.get("message", ""))

    def check_minecraft_foreground(
        self,
        *,
        process_names: Iterable[str] = (
            "Minecraft.exe",
            "javaw.exe",
            "java.exe",
        ),
        title_hints: Iterable[str] = ("Minecraft",),
    ) -> Tuple[bool, str]:
        """
        Check whether Minecraft is in the foreground (Windows),
        or at least running (macOS/Linux fallback).

        Windows strategy (no pywin32 needed):
          - GetForegroundWindow() → PID (via GetWindowThreadProcessId)
          - Compare process name to known Minecraft/Java launchers
          - As a secondary hint, try to read the window title (best-effort)

        Non-Windows strategy:
          - If psutil available, check if any minecraft/java process is running.
          - Foreground detection is not robust cross-platform without extra libs,
            so we only claim “running”.

        :param process_names: Executable name candidates for Java/MC.
        :param title_hints: Substrings expected to appear in the window title.
        :return: (ok, message)
        """
        system = platform.system()

        # If psutil is missing, we can’t do much anywhere.
        if psutil is None:
            return True, "mc-foreground-unknown: psutil not installed"

        if system == "Windows":
            try:
                import ctypes
                from ctypes import wintypes

                # Win32 API calls
                user32 = ctypes.WinDLL("user32", use_last_error=True)
                GetForegroundWindow = user32.GetForegroundWindow
                GetWindowThreadProcessId = user32.GetWindowThreadProcessId
                GetForegroundWindow.restype = wintypes.HWND
                GetWindowThreadProcessId.argtypes = [
                    wintypes.HWND,
                    ctypes.POINTER(wintypes.DWORD),
                ]
                GetWindowTextW = user32.GetWindowTextW
                GetWindowTextLengthW = user32.GetWindowTextLengthW

                hwnd = GetForegroundWindow()
                if not hwnd:
                    return False, "mc-foreground-false: no-foreground-window"

                pid = wintypes.DWORD(0)
                _ = GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                pid = pid.value
                if not pid:
                    return False, "mc-foreground-false: no-foreground-pid"

                # Process name check
                name = ""
                try:
                    name = psutil.Process(pid).name()
                except Exception:
                    pass

                name_match = name.lower() in {p.lower() for p in process_names}

                # Title contains hint?
                title = ""
                try:
                    length = GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buf = ctypes.create_unicode_buffer(length + 1)
                        GetWindowTextW(hwnd, buf, length + 1)
                        title = buf.value or ""
                except Exception:
                    pass

                title_match = any(
                    h.lower() in (title or "").lower() for h in title_hints
                )

                if name_match or title_match:
                    return (
                        True,
                        f"mc-foreground-ok: pid={pid} name='{name}' title='{title}'",
                    )
                else:
                    # If Minecraft is running but not foreground, surface that
                    if self._any_mc_process_running(process_names):
                        return (
                            False,
                            f"mc-running-not-foreground: pid={pid} name='{name}' title='{title}'",
                        )
                    return (
                        False,
                        f"mc-not-running: foreground pid={pid} name='{name}' title='{title}'",
                    )

            except Exception as e:
                # Degrade to “is running” probe if Win32 calls fail
                if self._any_mc_process_running(process_names):
                    return True, f"mc-running-unknown-foreground: {e}"
                return False, f"mc-not-running: {e}"

        else:
            # macOS/Linux: foreground without extra deps is non-trivial.
            # Provide a helpful, non-fatal signal.
            if self._any_mc_process_running(process_names):
                return True, "mc-running (foreground not verified on this OS)"
            return False, "mc-not-running"

    # ----- helpers -----
    def _any_mc_process_running(self, process_names: Iterable[str]) -> bool:
        if psutil is None:
            return False
        names = {p.lower() for p in process_names}
        for proc in psutil.process_iter(attrs=["name"]):
            try:
                if (proc.info.get("name") or "").lower() in names:
                    return True
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
            ):  # pragma: no cover
                continue
        return False
