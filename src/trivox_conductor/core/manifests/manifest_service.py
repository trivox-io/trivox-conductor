from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from trivox_conductor.common.logger import logger


@dataclass
class ManifestEvent:
    timestamp: float
    kind: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionManifest:
    session_id: str
    profile_key: Optional[str]
    created_at: float
    events: List[ManifestEvent] = field(default_factory=list)


class ManifestService:
    """
    Very small manifest store: one JSON file per session.

    Default root: ~/.trivox/manifests (can later be wired to settings).
    """

    def __init__(self, root: Optional[Path] = None) -> None:
        if root is None:
            base = __file__.replace(
                r"src\trivox_conductor\core\manifests\manifest_service.py", ""
            )
            logger.debug(f"ManifestService base path: {base}")
            root = Path(base) / ".trivox_conductor" / "manifests"
        self._root = root
        logger.debug(f"ManifestService root: {self._root}")
        self._root.mkdir(parents=True, exist_ok=True)

        # in-memory cache for the current process
        self._cache: Dict[str, SessionManifest] = {}

    def _path_for(self, session_id: str) -> Path:
        return self._root / f"{session_id}.json"

    def start_session(
        self, session_id: str, profile_key: Optional[str]
    ) -> None:
        if session_id in self._cache:
            # already started
            return
        manifest = SessionManifest(
            session_id=session_id,
            profile_key=profile_key,
            created_at=time.time(),
        )
        self._cache[session_id] = manifest
        self._save(manifest)
        logger.debug(
            "manifest.start - sid=%s profile=%s", session_id, profile_key
        )

    def append_event(
        self, session_id: str, kind: str, payload: Dict[str, Any]
    ) -> None:
        manifest = self._cache.get(session_id)
        if not manifest:
            # lazy start if someone forgot to call start_session
            manifest = SessionManifest(
                session_id=session_id,
                profile_key=payload.get("profile_key"),
                created_at=time.time(),
            )
            self._cache[session_id] = manifest

        manifest.events.append(
            ManifestEvent(
                timestamp=time.time(), kind=kind, payload=dict(payload)
            )
        )
        self._save(manifest)
        logger.debug("manifest.append - sid=%s kind=%s", session_id, kind)

    def close_session(self, session_id: str) -> None:
        # nothing special yet, but we could mark as closed
        logger.debug("manifest.close - sid=%s", session_id)
        manifest = self._cache.get(session_id)
        if manifest:
            self._save(manifest)

    def _save(self, manifest: SessionManifest) -> None:
        path = self._path_for(manifest.session_id)
        payload = asdict(manifest)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
