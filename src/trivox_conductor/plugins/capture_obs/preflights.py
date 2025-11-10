from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Optional

from trivox_conductor.common.logger import logger
from trivox_conductor.core.preflights.preflight_registry import (
    PreflightRegistry,
)
from trivox_conductor.core.preflights.preflight_types import (
    PreflightContext,
    PreflightFailure,
    Role,
)


class ObsHealthCheck:
    id = "capture.obs_health"
    role: Role = "capture"
    default_required = True
    adapter_name: Optional[str] = (
        "capture_obs"  # must match OBSAdapter.meta["name"]
    )

    def __call__(self, ctx: PreflightContext) -> Optional[PreflightFailure]:
        adapter = ctx.adapter
        # Only run if this is actually the obs adapter
        if getattr(adapter, "meta", {}).get("name") != self.adapter_name:
            return None

        try:
            health = adapter.health()
        except Exception as e:
            return PreflightFailure(
                id=self.id,
                message=f"OBS health call failed: {e}",
                required=True,
            )

        if not health.get("ok", False):
            return PreflightFailure(
                id=self.id,
                message=health.get("message", "obs-not-ok"),
                required=True,
            )

        logger.debug("capture.preflight_ok - obs: %s", health.get("message"))
        return None


PreflightRegistry.register("capture", ObsHealthCheck())


def _auto_find_obs_exe() -> Optional[Path]:
    """
    Best-effort OBS executable locator.

    For now:
      - Windows only (os.name == 'nt')
      - Looks in common install locations under Program Files / Program Files (x86)

    Returns:
      Path to obs64.exe / obs32.exe if found, otherwise None.
    """
    if os.name != "nt":
        logger.debug("obs_launch: auto-find skipped (non-Windows platform)")
        return None

    candidates: list[Path] = []

    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    pfx86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

    roots = {pf, pfx86}
    for root in roots:
        root_path = Path(root)
        candidates.extend(
            [
                root_path / "obs-studio" / "bin" / "64bit" / "obs64.exe",
                root_path / "obs-studio" / "bin" / "32bit" / "obs32.exe",
            ]
        )

    for p in candidates:
        if p.exists():
            logger.debug("obs_launch: auto-found OBS at %s", p)
            return p

    logger.debug("obs_launch: could not auto-find OBS in standard locations")
    return None


class ObsLaunchCheck:
    """
    Preflight that optionally launches OBS if it's not reachable.

    Expected settings/params (via ctx.settings):

      auto_launch: bool (default False)
      exe_path: str  (path to obs executable)
      launch_wait_sec: float (default 5.0)

    This is OBS-specific, so we only run it if adapter.meta["name"] == "capture_obs".
    """

    id = "capture.obs_launch"
    role: Role = "capture"
    default_required = True
    adapter_name: Optional[str] = (
        "capture_obs"  # must match OBSAdapter.meta["name"]
    )

    def __call__(self, ctx: PreflightContext) -> Optional[PreflightFailure]:
        adapter = ctx.adapter
        settings = ctx.settings

        # Only run when the active adapter is the OBS one
        if getattr(adapter, "meta", {}).get("name") != self.adapter_name:
            logger.warning("Skipping preflight, adapter is not OBS")
            return None

        auto_launch = bool(settings.get("auto_launch_obs", False))
        wait_sec = float(settings.get("obs_launch_wait_sec", 5.0))

        # 1) If OBS is already reachable, we're done.
        logger.debug("Checking initial OBS health")
        try:
            health = adapter.health()
            if health.get("ok", False):
                logger.debug(
                    "capture.preflight_ok - obs_launch: OBS already reachable"
                )
                return None
        except Exception as e:
            logger.warning("obs_launch.initial_health_failed: %s", e)

        # 2) Not reachable at this point.
        logger.info("OBS not reachable via health check")
        if not auto_launch:
            # Let capture.obs_health complain later – this check is a no-op.
            logger.debug(
                "capture.preflight_skip - obs_launch: auto_launch_obs=False"
            )
            return None

        # 3) Resolve an executable path:
        #    - explicit obs_exe_path if provided & exists
        #    - otherwise try auto-detect
        logger.debug("obs_launch: attempting to locate OBS executable")
        exe_path_str = settings.get("obs_exe_path")
        exe_path: Optional[Path] = None

        if exe_path_str:
            p = Path(exe_path_str)
            if p.exists():
                exe_path = p
            else:
                logger.debug(
                    "obs_launch: configured obs_exe_path '%s' does not exist, "
                    "falling back to auto-detect",
                    p,
                )

        if exe_path is None:
            exe_path = _auto_find_obs_exe()

        if exe_path is None:
            return PreflightFailure(
                id=self.id,
                message=(
                    "auto_launch_obs=True but OBS executable could not be found. "
                    "Configure 'obs_exe_path' in profile overrides."
                ),
                required=self.default_required,
            )

        # 4) Try to launch OBS
        logger.info("Launching OBS via %s", exe_path)
        try:
            logger.info("capture.obs_launch: starting OBS from %s", exe_path)

            # Prefer launching with the executable's directory as the working dir
            launch_cwd = exe_path.parent

            creationflags = 0
            # Optional: detach on Windows so we don't tie OBS to our console
            if os.name == "nt":
                creationflags = getattr(
                    subprocess, "DETACHED_PROCESS", 0
                ) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

            subprocess.Popen(
                [str(exe_path)],
                shell=False,
                cwd=str(launch_cwd),
                close_fds=True,
                creationflags=creationflags,
            )
        except Exception as e:
            return PreflightFailure(
                id=self.id,
                message=f"Failed to launch OBS: {e}",
                required=self.default_required,
            )

        # 5) Give OBS a bit of time to start up before health check
        logger.debug(
            "capture.obs_launch: waiting %.1fs for OBS to come up", wait_sec
        )
        time.sleep(wait_sec)

        # 6) Retry health
        logger.debug("obs_launch: checking OBS health after launch")
        try:
            health = adapter.health()
        except Exception as e:
            return PreflightFailure(
                id=self.id,
                message=f"OBS health after launch failed: {e}",
                required=self.default_required,
            )

        if not health.get("ok", False):
            return PreflightFailure(
                id=self.id,
                message="OBS started but health check is still not OK: "
                + health.get("message", "unknown"),
                required=self.default_required,
            )

        logger.debug(
            "capture.preflight_ok - obs_launch: OBS started and reachable"
        )
        return None


PreflightRegistry.register("capture", ObsLaunchCheck())
