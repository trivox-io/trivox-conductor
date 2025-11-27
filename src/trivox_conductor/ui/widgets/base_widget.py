from __future__ import annotations

from typing import Optional

from PySide6 import QtWidgets


class BaseWidget(QtWidgets.QWidget):

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
