# modules/mux/offset_math.py
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class OffsetInputs:
    t_obs0_ms: int        # OBS recording start (ms)
    t_rep0_ms: int        # Replay export timeline start (ms, relative to game session)
    clip_s_ms: int        # Clip start within replay
    clip_e_ms: int        # Clip end within replay

@dataclass
class OffsetResult:
    offset_ms: int
    duration_ms: int

class OffsetCalculator:
    """
    Computes audio slice offset relative to the OBS recording timeline.
    Keep this pure (deterministic, unit-testable).
    """
    def calculate(self, i: OffsetInputs) -> OffsetResult:
        # Simplified: align replay clip start to OBS origin
        offset = (i.t_rep0_ms + i.clip_s_ms) - i.t_obs0_ms
        duration = max(0, i.clip_e_ms - i.clip_s_ms)
        return OffsetResult(offset_ms=max(0, offset), duration_ms=duration)
