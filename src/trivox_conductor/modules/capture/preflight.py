
from __future__ import annotations
from typing import Tuple

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

    def check_obs_health(self) -> Tuple[bool, str]:
        """
        Check if the OBS adapter is healthy and reachable.
        
        :return: Tuple of (is_ok, message).
        :rtype: Tuple[bool, str]
        """
        # TODO: real impl might ping the adapter or health() call
        return True, "obs-ok"

    def check_minecraft_foreground(self) -> Tuple[bool, str]:
        """
        Check if Minecraft is running in the foreground.
        
        :return: Tuple of (is_ok, message).
        :rtype: Tuple[bool, str]
        """
        # TODO: implement actual check
        return True, "mc-foreground-ok"
