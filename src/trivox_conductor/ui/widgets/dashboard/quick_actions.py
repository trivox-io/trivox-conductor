from __future__ import annotations
from typing import Optional

from PySide6 import QtWidgets

from trivox_conductor.common.settings import settings
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
from trivox_conductor.core.trivox_context import trivox_context
from trivox_conductor.modules.capture.services import CaptureService


class QuickActionsWidget(QtWidgets.QWidget):
    """
    Only Start/Stop recording for now. Pure UI; talks to services via context/registries.
    """

    def __init__(self, *, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self._svc = CaptureService(CaptureRegistry, settings)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = QtWidgets.QLabel("Quick Actions", self)
        title.setObjectName("dashCardTitle")
        layout.addWidget(title)

        btns = QtWidgets.QHBoxLayout()
        self.btn_start = QtWidgets.QPushButton("Start Recording", self)
        self.btn_stop = QtWidgets.QPushButton("Stop Recording", self)
        self.btn_start.setMinimumHeight(32)
        self.btn_stop.setMinimumHeight(32)
        btns.addWidget(self.btn_start)
        btns.addWidget(self.btn_stop)
        layout.addLayout(btns)

        self.btn_start.clicked.connect(self._on_start)
        self.btn_stop.clicked.connect(self._on_stop)

    def _on_start(self):
        # SessionManager may be a class or instance in your codebase—both patterns are used in your snippets.
        session = trivox_context.session
        self._svc.start(
            session_id=session.id,
            pipeline_profile=trivox_context.profile,
            overrides=trivox_context.overrides,
        )

    def _on_stop(self):
        self._svc.stop()
