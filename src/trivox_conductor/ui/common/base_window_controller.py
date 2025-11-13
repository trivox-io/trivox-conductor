from asyncio.log import logger
from typing import Any, Optional

from trivox_conductor.core.trivox_context import (
    ContextBuilder,
    ContextBuilderData,
)
from trivox_conductor.ui.common.controllers_mediator import ControllersMediator


class BaseWindowController(ControllersMediator):
    """
    Base window controller

    :extends: ControllersMediator
    """

    _pipeline_profile_key: Optional[str] = None

    def __init__(self, mediator: ControllersMediator):
        """
        :param mediator: The controllers mediator
        :type mediator: ControllersMediator
        """
        self.mediator = mediator

    def set_role_context(self, overrides: Optional[dict[str, Any]] = None):
        """Set connection overrides for the processor."""
        data = ContextBuilderData(
            pipeline_profile_key=self._pipeline_profile_key
            or "default_profile",
            overrides=overrides or {},
        )
        ContextBuilder.build_context(data)

    def show(self):
        """
        Show method
        """
        raise NotImplementedError(
            "show method must be implemented in derived class"
        )
