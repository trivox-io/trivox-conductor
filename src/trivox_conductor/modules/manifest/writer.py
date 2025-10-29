
from __future__ import annotations
from typing import Dict, Any, Union
import json
from pathlib import Path

class ManifestWriter:
    """
    Owns writes and versioning rules. Keeps this small and explicit.
    """

    def write_v1(self, dst_json: Union[str, Path], base: Dict[str, Any]) -> None:
        p = Path(dst_json)
        base = dict(base)
        base.setdefault("version", 1)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            json.dump(base, f, indent=2, ensure_ascii=False)

    def upgrade_to_v2(self, src_json: Union[str, Path], dst_json: Union[str, Path], v2_extra: Dict[str, Any]) -> None:
        from .reader import ManifestReader
        data = ManifestReader().read(src_json)
        data.update(v2_extra)
        data["version"] = 2
        self.write_v1(dst_json, data)
