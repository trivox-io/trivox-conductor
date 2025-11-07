from PySide6 import QtWidgets

from trivox_conductor.common.logger import logger
from trivox_conductor.ui.common.base_window_view import BaseWindowView
from trivox_conductor.ui.qt.compiled.main_window import Ui_MainWindow


class MainWindowView(BaseWindowView, Ui_MainWindow):
    """
    Main window view

    :extends BaseWindowView
    :extends Ui_MainWindow
    """

    def __init__(self, parent: QtWidgets.QWidget = None):
        """
        :param parent: The parent widget
        :type parent: QtWidgets.QWidget
        """
        super().__init__(parent)
