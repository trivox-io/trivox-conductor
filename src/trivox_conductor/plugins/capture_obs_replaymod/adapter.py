
from __future__ import annotations

import logging

from obsws_python import error as obs_err

from trivox_conductor.core.contracts.base_contract import AdapterMeta
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.events import topics

from trivox_conductor.plugins.capture_obs.adapter import OBSAdapter

logger = logging.getLogger(__name__)


class OBSReplaymodAdapter(OBSAdapter):
    """
    Capture adapter for OBS (Open Broadcaster Software).
    Implements the CaptureAdapter contract.
    
    :cvar meta (AdapterMeta): Metadata describing the adapter.
    """

    meta: AdapterMeta = {
        "name": "capture_obs_replaymod",
        "role": "capture",
        "version": "0.1.0",
        "requires_api": ">=1.0,<2.0",
        "capabilities": ["scenes:list", "profiles:list"],
        "source": "local",
    }

    def health(self):
        parent_result = super().health()
        if not parent_result.get("ok", False):
            return parent_result
        # TODO: Add ReplayMod-specific health checks here if needed
        return {"ok": True, "details": "OBS ReplayMod adapter is healthy."}

    def start_capture(self):
        c = self._ensure_client()
        try:
            c.start_record()  # StartRecord
            # TODO: Add ReplayMod-specific start logic here if needed
        except obs_err.OBSSDKTimeoutError as e:
            BUS.publish(topics.CAPTURE_ERROR, {"session_id": self._session_id, "error": str(e)})
            raise RuntimeError(f"StartRecord failed: {e}") from e

        BUS.publish(topics.CAPTURE_STARTED, {"session_id": self._session_id})

    def stop_capture(self):
        c = self._ensure_client()
        try:
            # StopRecord returns outputPath in response; emit it if present.
            res = c.stop_record()  # StopRecord
            output_path = getattr(res, "output_path", None)
            # TODO: Add ReplayMod-specific stop logic here if needed
        except obs_err.OBSSDKTimeoutError as e:
            BUS.publish(topics.CAPTURE_ERROR, {"session_id": self._session_id, "error": str(e)})
            raise RuntimeError(f"StopRecord failed: {e}") from e

        payload = {"session_id": self._session_id}
        if output_path:
            payload["output_path"] = output_path
        BUS.publish(topics.CAPTURE_STOPPED, payload)
