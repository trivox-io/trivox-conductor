from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import trivox_conductor.constants as trivox_constants
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
            base = trivox_constants.ROOT_DIR
            logger.debug(f"ManifestService base path: {base}")
            root = Path(base) / ".trivox" / "manifests"
        self._root = root
        logger.debug(f"ManifestService root: {self._root}")
        self._root.mkdir(parents=True, exist_ok=True)

        # in-memory cache for the current process
        self._cache: Dict[str, SessionManifest] = {}

    def _path_for(self, session_id: str) -> Path:
        return self._root / f"{session_id}.json"

    def _load_manifest(self, session_id: str) -> Optional[SessionManifest]:
        """
        Load manifest from cache or disk if it exists.
        """
        if session_id in self._cache:
            return self._cache[session_id]

        path = self._path_for(session_id)
        if not path.exists():
            return None

        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(
                "manifest.load_failed - sid=%s path=%s error=%s",
                session_id,
                path,
                e,
            )
            return None

        events_data = raw.get("events", []) or []
        events = [
            ManifestEvent(
                timestamp=e.get("timestamp", time.time()),
                kind=e.get("kind", ""),
                payload=e.get("payload") or {},
            )
            for e in events_data
        ]

        manifest = SessionManifest(
            session_id=raw.get("session_id", session_id),
            profile_key=raw.get("profile_key"),
            created_at=raw.get("created_at", time.time()),
            events=events,
        )
        self._cache[session_id] = manifest
        return manifest

    def start_session(self, session_id: str, profile_key: Optional[str]):
        manifest = self._load_manifest(session_id)

        if manifest:
            # Already exists (e.g. process restart). You may want to
            # backfill profile_key if it was missing:
            if profile_key and not manifest.profile_key:
                manifest.profile_key = profile_key
                self._save(manifest)
            logger.debug(
                "manifest.start_skip - sid=%s already exists (profile=%s)",
                session_id,
                manifest.profile_key,
            )
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
    ):
        manifest = self._load_manifest(session_id)
        logger.debug(
            "manifest.append - sid=%s loaded=%s", session_id, bool(manifest)
        )

        if not manifest:
            # lazily create if nothing exists on disk
            manifest = SessionManifest(
                session_id=session_id,
                profile_key=payload.get("profile_key"),
                created_at=time.time(),
            )
            self._cache[session_id] = manifest
            logger.debug(
                "manifest.auto_create - sid=%s (no existing manifest)",
                session_id,
            )

        manifest.events.append(
            ManifestEvent(
                timestamp=time.time(), kind=kind, payload=dict(payload)
            )
        )
        self._save(manifest)
        logger.debug("manifest.append_done - sid=%s kind=%s", session_id, kind)

    def close_session(self, session_id: str):
        logger.debug("manifest.close - sid=%s", session_id)
        manifest = self._load_manifest(session_id)
        if not manifest:
            logger.debug(
                "manifest.close_skip - sid=%s no manifest on disk", session_id
            )
            return

        # Later you might add manifest.closed_at etc. For now, just save.
        self._save(manifest)
        logger.debug("manifest.close_done - sid=%s", session_id)

    def _save(self, manifest: SessionManifest) -> None:
        path = self._path_for(manifest.session_id)
        payload = asdict(manifest)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
