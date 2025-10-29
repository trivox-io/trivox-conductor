from __future__ import annotations
from typing import Dict, Optional
from trivox_conductor.core.contracts.watcher import WatcherAdapter
from trivox_conductor.core.contracts.base_contract import AdapterMeta
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.events import topics

class ReplayWatcherAdapter(WatcherAdapter):
    meta: AdapterMeta = {
        "name": "watcher_replay",
        "role": "watcher",
        "version": "0.1.0",
        "requires_api": ">=1.0,<2.0",
        "capabilities": ["stable_detection", "session_correlation"],
        "source": "local",
    }
    def __init__(self) -> None:
        self._cfg: Dict = {}
        self._sec: Dict = {}
        self._path: str = ""

    def configure(self, settings: Dict, secrets: Dict) -> None:
        self._cfg, self._sec = settings or {}, secrets or {}

    def set_watch_path(self, path: Optional[str] = None) -> None:
        self._path = path

    def start(self) -> None:
        # real impl: start filesystem watcher thread; emit REPLAY_RENDER_DETECTED
        pass

    def stop(self) -> None:
        pass

    # helper to simulate detection
    def _emit_detected(self, path: str, length: float, fps: int, session_id: str) -> None:
        BUS.publish(topics.REPLAY_RENDER_DETECTED, {
            "path": path, "length": length, "fps": fps, "session_id": session_id
        })
