# modules/mux/mux_service.py
from __future__ import annotations

from typing import Dict

from trivox_conductor.core.contracts.mux import MuxAdapter, MuxParams
from trivox_conductor.core.events import topics
from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.registry.mux_registry import MuxRegistry
from trivox_conductor.core.services.base_service import BaseService

from .offset_math import OffsetResult
from .settings import MuxSettingsModel


class MuxService(BaseService[MuxSettingsModel, MuxAdapter]):
    """
    Orchestrates mux jobs with validated parameters; emits progress via EventBus.
    SRP: business rules live here; adapter just executes.
    """

    SECTION = "mux"
    MODEL = MuxSettingsModel

    def __init__(self, registry: MuxRegistry, settings: Dict) -> None:
        super().__init__(registry, settings)

    def mux_clip(
        self,
        replay_path: str,
        audio_sources: Dict[str, str],
        calc: OffsetResult,
        session_id: str,
    ) -> None:
        adapter = self._require_adapter()
        params: MuxParams = MuxParams(
            {
                "replay_path": replay_path,
                "offset_ms": calc.offset_ms,
                "duration_ms": calc.duration_ms,
                "normalize": self._settings.normalize,
                "lufs": self._settings.loudness_target_lufs,
                "desktop_device": audio_sources.get("desktop"),
                "mic_device": audio_sources.get("mic"),
                "ffmpeg_path": self._settings.ffmpeg_path,
                "session_id": session_id,
            }
        )
        BUS.publish(topics.MUX_STARTED, {"session_id": session_id})
        adapter.mux(params)  # adapter should publish PROGRESS/DONE/FAILED
        # Optionally: add guard rails/retries here
