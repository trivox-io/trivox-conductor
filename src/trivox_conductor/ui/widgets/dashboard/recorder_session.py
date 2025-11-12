from __future__ import annotations
from PySide6 import QtWidgets
from trivox_conductor.core.events.bus import (
    BUS,
)  # uses your existing event bus
from trivox_conductor.core.events.topics import (
    CAPTURE_STARTED,
    CAPTURE_STOPPED,
)  # adjust if names differ


class RecorderSessionWidget(QtWidgets.QWidget):
    """
    Shows session id + current status (idle/recording). Listens to BUS for updates.
    """

    def __init__(
        self, *, context: dict, parent: QtWidgets.QWidget | None = None
    ):
        super().__init__(parent)
        self._ctx = context
        self._session_mgr = context["session_manager"]

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = QtWidgets.QLabel("Recorder & Session", self)
        title.setObjectName("dashCardTitle")
        layout.addWidget(title)

        self._status = QtWidgets.QLabel("Idle", self)
        self._status.setObjectName("badgeIdle")

        self._session_id = QtWidgets.QLabel("-", self)
        self._session_id.setTextInteractionFlags(
            self._session_id.textInteractionFlags()
        )

        form = QtWidgets.QFormLayout()
        form.addRow("Status:", self._status)
        form.addRow("Session ID:", self._session_id)
        layout.addLayout(form)
        layout.addStretch(1)

        # Subscribe to events (weakly coupled; UI doesn’t call services here)
        BUS.subscribe(CAPTURE_STARTED, self._on_started)
        BUS.subscribe(CAPTURE_STOPPED, self._on_stopped)

        # Initialize from current session if your SessionManager exposes it
        try:
            current = self._session_mgr.current_session()
            if current:
                self._session_id.setText(current.id)
        except Exception:
            pass

    # --- event handlers
    def _on_started(self, payload: dict):
        sid = payload.get("session_id")
        self._status.setText("Recording")
        self._status.setObjectName("badgeRecording")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        if sid:
            self._session_id.setText(sid)

    def _on_stopped(self, payload: dict):
        self._status.setText("Idle")
        self._status.setObjectName("badgeIdle")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
