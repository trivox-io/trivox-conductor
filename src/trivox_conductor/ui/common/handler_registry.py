"""
Handler registry
"""

from typing import Dict, Type

from trivox_conductor.ui.common.base_handler import BaseHandler


class HandlerRegistry:
    """
    Handler registry
    """

    _handlers: Dict[str, BaseHandler] = {}

    @classmethod
    def register(
        cls, name: str, handler_cls: Type[BaseHandler], *args, **kwargs
    ):
        """
        :param name: The handler name
        :type name: str

        :param handler_cls: The handler class
        :type handler_cls: BaseHandler
        """

        cls._handlers[name] = handler_cls(*args, **kwargs)

    @classmethod
    def get(cls, name: str) -> BaseHandler:
        """
        :param name: The handler name
        :type name: str

        :return: The handler class
        :rtype: BaseHandler
        """

        handler_cls = cls._handlers.get(name)
        if handler_cls:
            return handler_cls
        raise ValueError(f"Handler '{name}' not found")

    @classmethod
    def list(cls) -> list:
        """
        :return: The list of handler names
        :rtype: list
        """

        return list(cls._handlers.keys())
