from __future__ import annotations

from typing import Optional
from venv import logger

from PySide6 import QtWidgets

from trivox_conductor.common.settings import settings
from trivox_conductor.core.trivox_context import trivox_context
from trivox_conductor.modules.capture.registry import CaptureRegistry
from trivox_conductor.modules.capture.services import CaptureService
from trivox_conductor.ui.common.handler_registry import HandlerRegistry
from trivox_conductor.ui.widgets.base_widget import BaseWidget


class QuickActionsWidget(BaseWidget):
    """
    Only Start/Stop recording for now. Pure UI; talks to services via context/registries.
    """

    def __init__(self, *, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        session = trivox_context.session
        self._service = CaptureService(
            CaptureRegistry,
            settings,
            session_id=session.id,
            pipeline_profile=trivox_context.profile,
            profile_overrides=trivox_context.overrides,
        )

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
        self.btn_stop.setEnabled(False)
        btns.addWidget(self.btn_start)
        btns.addWidget(self.btn_stop)
        layout.addLayout(btns)

        self.btn_start.clicked.connect(self._on_start)
        self.btn_stop.clicked.connect(self._on_stop)

    def _on_start(self):
        # self._service.start()
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        try:
            handler_cls = HandlerRegistry.get("start_capture")
            logger.info("Using handler class: %s", handler_cls)
            handler_cls.handle()
        except ValueError as e:
            logger.error("Failed to start capture: %s", e)
            self.btn_start.setEnabled(True)
            self.btn_stop.setEnabled(False)

    def _on_stop(self):
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        try:
            handler_cls = HandlerRegistry.get("stop_capture")
            logger.info("Using handler class: %s", handler_cls)
            handler_cls.handle()
        except ValueError as e:
            logger.error("Failed to stop capture: %s", e)
            self.btn_start.setEnabled(False)
            self.btn_stop.setEnabled(True)
