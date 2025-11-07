from __future__ import annotations

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
