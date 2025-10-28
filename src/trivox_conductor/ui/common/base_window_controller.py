
from trivox_conductor.ui.common.controllers_mediator import ControllersMediator


class BaseWindowController(ControllersMediator):
    """
    Base window controller

    :extends: ControllersMediator
    """

    def __init__(self, mediator: ControllersMediator):
        """
        :param mediator: The controllers mediator
        :type mediator: ControllersMediator
        """
        self.mediator = mediator

    def show(self):
        """
        Show method
        """
        raise NotImplementedError(
            "show method must be implemented in derived class"
        )
