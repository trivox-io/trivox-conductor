"""
Strategy module for the IC Inspector application.
"""

from typing import Optional

from PySide6 import QtCore

from trivox_conductor.common.workers import BaseWorker
from trivox_conductor.ui.common.base_window_controller import (
    BaseWindowController,
)


class BaseStrategy(QtCore.QObject):
    """
    Base class for all strategies

    :extends QtCore.QObject: Base class for all Qt objects
    """

    name: Optional[str] = None
    execution_finished = QtCore.Signal(dict)
    worker: Optional[BaseWorker] = None

    def __init__(self, controller: BaseWindowController):
        """
        :param controller: The controller for the strategy
        :type controller: BaseWindowController
        """

        super().__init__()

        self.controller = controller

    def process_result_callback(self, result: dict):
        """
        Process the result of the strategy

        :param result: The result of the strategy
        :type result: dict
        """

        self.execution_finished.emit(result)

    def execute(self, *args, **kwargs):
        """
        Execute the strategy

        :param args: The arguments for the strategy
        :param kwargs: The keyword arguments for the strategy
        """

        raise NotImplementedError


class StrategyRegistry:
    """
    Registry for all strategies
    """

    _strategies: dict[str, type[BaseStrategy]] = {}

    @classmethod
    def register(cls, strategy_cls: type[BaseStrategy]) -> type[BaseStrategy]:
        """
        Register a strategy class

        :param strategy_cls: The strategy class to register
        :type strategy_cls: type[BaseStrategy]

        :return: The registered strategy class
        :rtype: type[BaseStrategy]
        """
        if not issubclass(strategy_cls, BaseStrategy):
            raise ValueError(
                "Strategy class must be a subclass of BaseStrategy"
            )

        strategy_name = strategy_cls.name or strategy_cls.__name__
        cls._strategies[strategy_name] = strategy_cls
        return strategy_cls

    @classmethod
    def get(cls, name: str) -> Optional[type[BaseStrategy]]:
        """
        Get a strategy class by name

        :param name: The name of the strategy
        :type name: str

        :return: The strategy class
        :rtype: Optional[type[BaseStrategy]]
        """
        return cls._strategies.get(name)

    @classmethod
    def all(cls) -> dict[str, type[BaseStrategy]]:
        """
        Get all registered strategies

        :return: A dictionary of all registered strategies
        :rtype: dict[str, type[BaseStrategy]]
        """
        return cls._strategies


def _register_cls(registry_cls: StrategyRegistry) -> type:
    """
    Decorator to register a class in a registry

    :param registry_cls: The registry class
    :type registry_cls: type

    :return: The decorator function
    :rtype: type
    """

    def decorator(cls: type) -> type:
        registry_cls.register(cls)
        return cls

    return decorator


def register_strategy(strategy_cls: BaseStrategy) -> BaseStrategy:
    """
    Register a strategy

    :param strategy_cls: The strategy class to register
    :type strategy_cls: BaseStrategy

    :return: The registered strategy
    :rtype: BaseStrategy
    """
    return _register_cls(StrategyRegistry)(strategy_cls)
