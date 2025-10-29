
from __future__ import annotations
from typing import List, Dict
from trivox_conductor.core.contracts.capture import CaptureAdapter
from trivox_conductor.core.contracts.base_contract import AdapterMeta
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.events import topics

class OBSAdapter(CaptureAdapter):
    """
    Capture adapter for OBS (Open Broadcaster Software).
    Implements the CaptureAdapter contract.
    
    :cvar meta (AdapterMeta): Metadata describing the adapter.
    """

    meta: AdapterMeta = {
        "name": "capture_obs",
        "role": "capture",
        "version": "0.1.0",
        "requires_api": ">=1.0,<2.0",
        "capabilities": ["scenes:list", "profiles:list"],
        "source": "local",
    }

    def __init__(self):
        self._settings: Dict = {}
        self._secrets: Dict = {}

    def configure(self, settings: Dict, secrets: Dict):
        self._settings, self._secrets = settings or {}, secrets or {}

    def list_scenes(self) -> List[str]:
        return []

    def list_profiles(self) -> List[str]:
        return []
    
    def select_scene(self, name: str):
        # TODO: Implement scene selection logic here
        pass
    
    def select_profile(self, name: str):
        # TODO: Implement profile selection logic here
        pass
    
    def start_capture(self):
        BUS.publish(topics.CAPTURE_STARTED, {"session_id": self._settings.get("session_id")})

    def stop_capture(self):
        BUS.publish(topics.CAPTURE_STOPPED, {"session_id": self._settings.get("session_id")})
