

from abc import ABC


class ControllersMediator(ABC):
    """
    Base class for all controllers that act as a mediator between
    the UI and the application
    """

    def run(self):
        """
        Run the controller.
        """
        raise NotImplementedError
