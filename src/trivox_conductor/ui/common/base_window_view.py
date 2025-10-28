
from typing import Callable
from PySide6 import QtCore, QtGui, QtWidgets

from trivox_conductor.common.logging.log_subscriber import log_subscriber


class BaseWindowView(QtWidgets.QMainWindow):
    """
    Base class for all windows

    :extends QtWidgets.QMainWindow: The base class for all windows
    """

    _title = "Trivox Conductor" # TODO: From settings
    output: QtWidgets.QPlainTextEdit
    setupUi: Callable[[QtWidgets.QMainWindow], None]

    def __init__(self, parent: QtWidgets.QWidget = None):
        """
        :param parent: The parent widget
        :type parent: QtWidgets.QWidget
        """

        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(self._title)

        log_subscriber.subscribe(self.__console_pipe)

    def __console_pipe(self, message: str):
        """
        Append log messages to the QTextEdit in a thread-safe manner.

        :param message: The message to append
        :type message: str
        """

        QtCore.QMetaObject.invokeMethod(
            self,
            "update_output",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, message),
        )

    @QtCore.Slot(str)
    def update_output(self, message: str):
        """
        Update the console safely in the main thread.

        :param message: The message to append
        :type message: str
        """

        self.output.appendHtml(message)
        self.output.moveCursor(QtGui.QTextCursor.MoveOperation.Down)
        self.output.moveCursor(QtGui.QTextCursor.MoveOperation.StartOfLine)
