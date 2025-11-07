from trivox_conductor.common.logger import logger
from trivox_conductor.ui.common.base_window_controller import (
    BaseWindowController,
)
from trivox_conductor.ui.common.controllers_mediator import ControllersMediator
from trivox_conductor.ui.views.main_window_view import MainWindowView


class MainWindowController(BaseWindowController):
    """
    Main window controller

    :extends: BaseWindowController
    """

    def __init__(self, mediator: ControllersMediator):
        """
        :param mediator: The controllers mediator
        :type mediator: ControllersMediator
        """
        super().__init__(mediator)
        self._window = MainWindowView()
        self.__connect_signals()

    def __connect_signals(self):
        """
        This function connects signals to slots.
        """

    def show(self):
        logger.info("Showing Main Window")
        self._window.show()
