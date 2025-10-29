from __future__ import annotations
from typing import Dict

class MuxParams(Dict[str, object]):
    """Parameters for muxing operation."""

from .base_contract import Adapter
class MuxAdapter(Adapter):
    """Input: replay path, offset_ms, duration_ms, audio sources; emits MUX_*."""
    def mux(self, params: MuxParams) -> None: ...
