from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class SessionInfo:
    id: str
    created_at: datetime
    label: str = ""


class SessionManager:
    _current: Optional[SessionInfo] = None
    _by_id: Dict[str, SessionInfo] = {}

    @classmethod
    def generate_id(cls) -> str:
        # your format if you want, or UUID
        return uuid.uuid4().hex

    @classmethod
    def start_session(
        cls, session_id: Optional[str] = None, label: str = ""
    ) -> SessionInfo:
        sid = session_id or cls.generate_id()
        info = SessionInfo(id=sid, created_at=datetime.utcnow(), label=label)
        cls._by_id[sid] = info
        cls._current = info
        return info

    @classmethod
    def ensure_session(
        cls, session_id: Optional[str] = None, label: str = ""
    ) -> SessionInfo:
        if session_id and session_id in cls._by_id:
            cls._current = cls._by_id[session_id]
            return cls._current
        if session_id:
            return cls.start_session(session_id, label=label)
        if cls._current:
            return cls._current
        return cls.start_session(label=label)

    @classmethod
    def current(cls) -> Optional[SessionInfo]:
        return cls._current
