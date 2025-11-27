from typing import Any, Optional
from venv import logger

from trivox_conductor.core.session.session_manager import SessionManager
from trivox_conductor.core.trivox_context import (
    ContextBuilder,
    ContextBuilderData,
    TrivoxContext,
)
from trivox_conductor.ui.common.controllers_mediator import ControllersMediator


class BaseWindowController(ControllersMediator):
    """
    Base window controller

    :extends: ControllersMediator
    """

    _pipeline_profile_key: Optional[str] = None
    _context: Optional[TrivoxContext] = None

    def __init__(self, mediator: ControllersMediator):
        """
        :param mediator: The controllers mediator
        :type mediator: ControllersMediator
        """
        self.mediator = mediator
        self._session_manager = SessionManager()

    def initialize_context(self, overrides: Optional[dict[str, Any]] = None):
        """Set connection overrides for the processor."""
        data = ContextBuilderData(
            pipeline_profile_key=self._pipeline_profile_key
            # TODO: Bring default profile key from constants
            or "default_profile",
            overrides=overrides or {},
        )
        self._context = ContextBuilder.build_context(data)
        logger.debug(f"Profile: {self._context.profile}")
        logger.debug(f"Overrides: {self._context.overrides}")

    def show(self):
        """
        Show method
        """
        raise NotImplementedError(
            "show method must be implemented in derived class"
        )
