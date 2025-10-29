# modules/handoff/uploader_service.py
from __future__ import annotations
from typing import Dict
from trivox_conductor.core.contracts.uploader import UploaderAdapter
from trivox_conductor.core.contracts.notifier import NotifierAdapter
from trivox_conductor.core.registry.uploader_registry import UploaderRegistry
from trivox_conductor.core.registry.notifier_registry import NotifierRegistry
from trivox_conductor.core.services.base_service import BaseService
from .settings import HandoffSettingsModel


class UploaderService(BaseService[HandoffSettingsModel, UploaderAdapter]):
    """Owns upload behavior (idempotent paths, retries live in adapter)."""
    
    SECTION = "handoff"
    MODEL = HandoffSettingsModel

    def __init__(self, registry: UploaderRegistry, settings: Dict) -> None:
        super().__init__(registry, settings)

    def upload_clip(self, local_path: str, rel_path: str) -> None:
        adapter = self._require_adapter()
        dest = f"{self._settings.dest_root.rstrip('/')}/{rel_path.lstrip('/')}"
        adapter.upload(local_path, self._settings.rclone_remote, dest)


class NotifierService(BaseService[HandoffSettingsModel, NotifierAdapter]):
    """Builds consistent messages and calls NotifierAdapter once."""
    
    SECTION = "handoff"
    MODEL = HandoffSettingsModel

    def __init__(self, registry: NotifierRegistry, settings: Dict) -> None:
        super().__init__(registry, settings)

    def notify_upload_done(self, link: str, session_id: str) -> None:
        payload = {
            "title": "UPLOAD_DONE",
            "session_id": session_id,
            "link": link,
            "channels": {
                "slack": self._settings.slack_channel,
                "discord": self._settings.discord_channel,
            },
        }
        self._require_adapter().notify(payload)


