from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from trivox_conductor.common.settings import settings
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
from trivox_conductor.core.ui.nav_registry import ViewDescriptor, ViewRegistry

from .services import CaptureService


class CaptureMainView(QWidget):
    def __init__(self, *, context: dict):
        super().__init__()
        self._svc = CaptureService(CaptureRegistry, settings)
        self._context = context  # contains session/profile info, etc.

        layout = QVBoxLayout(self)
        self._status = QLabel("Capture idle", self)
        btn_start = QPushButton("Start capture", self)
        btn_stop = QPushButton("Stop capture", self)

        btn_start.clicked.connect(self._on_start)
        btn_stop.clicked.connect(self._on_stop)

        layout.addWidget(self._status)
        layout.addWidget(btn_start)
        layout.addWidget(btn_stop)

    def _on_start(self):
        session = self._context["session_manager"].ensure_session(
            label="capture"
        )
        self._svc.start(
            session_id=session.id,
            pipeline_profile=self._context.get("pipeline_profile"),
        )
        self._status.setText(f"Recording ({session.id[:8]})")

    def _on_stop(self):
        self._svc.stop()
        self._status.setText("Capture stopped")


ViewRegistry.register(
    "capture_main",
    ViewDescriptor(
        id="capture_main",
        title="Capture",
        area="main",
        order=10,
        factory=lambda context: CaptureMainView(context=context),
    ),
)
