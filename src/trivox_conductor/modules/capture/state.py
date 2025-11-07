"""
Capture Runtime State
=====================

Simple dataclass capturing minimal, process-agnostic state for a capture session.
Used by the service together with :mod:`state_store` to persist across CLI runs.

Fields
------
- ``session_id`` : str | None
- ``scene`` : str | None
- ``profile`` : str | None
- ``is_recording`` : bool
- ``started_ts`` : float | None
- ``notes`` : List[str]

Usage
-----
- ``start(session_id)`` marks the beginning of a session and stamps ``started_ts``.
- ``stop()`` clears the recording flag; additional cleanup is handled by the service.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CaptureState:
    """
    Runtime state for capture sessions (SRP: state only).

    :cvar session_id (Optional[str]): Current capture session ID.
    :cvar scene (Optional[str]): Currently selected scene.
    :cvar profile (Optional[str]): Currently selected profile.
    :cvar is_recording (bool): Flag indicating if recording is in progress.
    :cvar started_ts (Optional[float]): Timestamp when recording started.
    :cvar notes (List[str]): List of notes or logs related to the capture session.
    """

    session_id: Optional[str] = None
    scene: Optional[str] = None
    profile: Optional[str] = None
    is_recording: bool = False
    started_ts: Optional[float] = None
    notes: List[str] = field(default_factory=list)

    def start(self, session_id: str):
        """
        Start a capture session with the given session ID.

        :param session_id: The session ID for the capture operation.
        :type session_id: str
        """
        self.session_id = session_id
        self.is_recording = True
        self.started_ts = time.time()

    def stop(self):
        """Stop the current capture session."""
        self.is_recording = False
