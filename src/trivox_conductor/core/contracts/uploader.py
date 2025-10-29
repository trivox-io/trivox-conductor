from __future__ import annotations
from .base_contract import Adapter

class UploaderAdapter(Adapter):
    """Upload local file to remote (e.g., Drive via rclone)."""
    def upload(self, local_path: str, remote: str, dest_path: str) -> None: ...
