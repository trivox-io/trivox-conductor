import sys

from PySide6 import QtWidgets

from trivox_conductor.common.logger import logger
from trivox_conductor.ui.common.base_window_controller import (
    BaseWindowController,
)
from trivox_conductor.ui.common.controllers_mediator import ControllersMediator
from trivox_conductor.ui.controllers.main_window_controller import (
    MainWindowController,
)


class TrivoxInspectorApp(ControllersMediator):

    _main_window_controller: BaseWindowController

    def __init__(self, **kwargs):
        """
        :param test: Run the application in test mode.
        :type test: bool

        If test is True, the application will run in test mode (Will show the test window).
        """
        logger.debug("Initializing TrivoxInspectorApp with kwargs: %s", kwargs)
        # Reuse an existing instance if one already exists (pytest-qt, other tests)
        instance = QtWidgets.QApplication.instance()
        self._app = instance or QtWidgets.QApplication(sys.argv)

        pipeline_profile_key = kwargs.pop("pipeline_profile", None)
        self._main_window_controller = MainWindowController(
            self, pipeline_profile_key=pipeline_profile_key
        )

    def run(self):
        logger.info("Initializing the application...")
        self._main_window_controller.show()
        self._app.exec_()
