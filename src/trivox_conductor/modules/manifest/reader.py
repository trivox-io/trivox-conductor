
from __future__ import annotations
from typing import Dict, Any, Union
import json
from pathlib import Path

class ManifestReader:
    """Pure I/O helpers for reading traveling manifests."""

    def read(self, json_path: Union[str, Path]) -> Dict[str, Any]:
        p = Path(json_path)
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
