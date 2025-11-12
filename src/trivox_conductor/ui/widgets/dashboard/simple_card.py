# ui/widgets/dashboard/simple_card.py
from __future__ import annotations
from PySide6 import QtWidgets


class SimpleCard(QtWidgets.QWidget):
    def __init__(
        self,
        *,
        title: str,
        body: str = "",
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        ttl = QtWidgets.QLabel(title, self)
        ttl.setObjectName("dashCardTitle")
        layout.addWidget(ttl)

        if body:
            lbl = QtWidgets.QLabel(body, self)
            lbl.setWordWrap(True)
            layout.addWidget(lbl)

        layout.addStretch(1)
