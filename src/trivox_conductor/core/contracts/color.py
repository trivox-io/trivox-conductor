from __future__ import annotations
from .base_contract import Adapter

class ColorAdapter(Adapter):
    """Resolve Free: import IGReady, preset/LUT, render to IGColor."""
    def color_pass(self, src_path: str, preset: str, dst_dir: str) -> None: ...
