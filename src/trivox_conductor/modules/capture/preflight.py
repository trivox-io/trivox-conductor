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

from __future__ import annotations
from typing import Tuple

from trivox_conductor.core.contracts.capture import CaptureAdapter


class CapturePreflight:
    """
    Stateless checks before starting capture. Keeps I/O minimal for testability.
    """

    def check_disk_space(self, path: str, min_gb: float = 5.0) -> Tuple[bool, str]:
        """
        Check if there is sufficient disk space at the given path.
        
        :param path: Filesystem path to check.
        :type path: str
        
        :param min_gb: Minimum required free space in gigabytes.
        :type min_gb: float
        
        :return: Tuple of (is_ok, message).
        :rtype: Tuple[bool, str]
        """
        # TODO: os.statvfs on POSIX / shutil.disk_usage on Windows
        return True, "disk-ok"

    def check_obs_health(self, adapter: CaptureAdapter) -> Tuple[bool, str]:
        """
        Check if the OBS adapter is healthy and reachable.
        
        :return: Tuple of (is_ok, message).
        :rtype: Tuple[bool, str]
        """
        res = adapter.health()
        return bool(res.get("ok")), str(res.get("message", ""))

    def check_minecraft_foreground(self) -> Tuple[bool, str]:
        """
        Check if Minecraft is running in the foreground.
        
        :return: Tuple of (is_ok, message).
        :rtype: Tuple[bool, str]
        """
        # TODO: implement actual check
        return True, "mc-foreground-ok"
