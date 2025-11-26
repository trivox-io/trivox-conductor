"""
Base command processor for Trivox Capture commands.
"""

from typing import Any, Mapping, Optional, Type

from trivox_conductor.common.commands.base_command_processor import (
    BaseCommandProcessor,
)
from trivox_conductor.common.logger import logger
from trivox_conductor.core.session.session_manager import SessionManager
from trivox_conductor.core.trivox_context import (
    ContextBuilder,
    ContextBuilderData,
    trivox_context,
)


class TrivoxCaptureCommandProcessor(BaseCommandProcessor):
    """
    Command processor for Trivox Capture commands.

    :cvar SERVICE_CLS (Type): The service class to instantiate.
    :cvar ACTION_MAP (Mapping[str, str]): Mapping of action names to service method names.
    """

    ROLE: str
    SERVICE_CLS: Type  # e.g. CaptureService
    ACTION_MAP: Mapping[str, str]  # e.g. {"start": "start", "stop": "stop"}
    _cli_session_id: Optional[str] = None
    _session_id: Optional[str] = None

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        # TODO: Get rid of redundant kwargs handling in CLI framework
        self._kwargs.pop("verbose", None)

        self._action = self._kwargs.pop("action", None)
        self._cli_session_id = self._kwargs.pop("session_id", None)
        self._pipeline_profile_key: Optional[str] = self._kwargs.pop(
            "pipeline_profile"
        )

        # TODO: Implement profile application logic
        self._config_file_path: Optional[str] = self._kwargs.pop("config")

        self._overrides = self._get_overrides()
        self._initialize_context()

    @staticmethod
    def _parse_options_string(raw: Optional[str]) -> dict[str, Any]:
        """
        Parse 'host=127.0.0.1,port=5050,scene=Foo' -> {'host': '127.0.0.1', ...}.

        Extremely simple on purpose; adapters can further coerce types if needed.
        """
        if not raw:
            return {}
        out: dict[str, Any] = {}
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        for part in parts:
            if "=" not in part:
                logger.warning(
                    f"Skipping invalid options part (no '='): '{part}'"
                )
                continue
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key:
                continue
            out[key] = value
        return out

    def _get_overrides(self) -> dict[str, Any]:
        """Extract connection overrides from kwargs."""
        raw_options = self._kwargs.pop("options", None)
        options_dict = self._parse_options_string(raw_options)

        overrides = dict(options_dict)

        logger.debug(f"Role overrides (from --options): {overrides}")
        return overrides

    def _initialize_context(self):
        """Set connection overrides for the processor."""
        # TODO: Sessions have a manager; use it to create/get session by ID
        # instead of fiddling with trivox_context directly
        # TODO: Profile overrides should be gotten by role, not globally
        data = ContextBuilderData(
            role=self.ROLE,
            pipeline_profile_key=self._pipeline_profile_key,
            overrides=self._overrides,
            session_id=self._cli_session_id,
        )
        logger.debug(f"Initializing context with data: {data}")
        ContextBuilder.build_context(data)
        logger.info(f"Resolved pipeline profile: {trivox_context.profile}")
        self._session_id = trivox_context.session.id
        logger.info(f"Using session ID: {self._session_id}")

    def build_service(self):
        """Subclasses build the service with proper registries/settings."""
        raise NotImplementedError

    def build_call_kwargs(self, action: str) -> dict[str, Any]:
        """Subclasses decide which kwargs go into each service call."""
        logger.debug(f"Building call kwargs for action: {action}")
        return {}

    def run(self):
        svc = self.build_service()
        if not self._action:
            raise ValueError("Action is required")

        try:
            method_name = self.ACTION_MAP[self._action]
        except KeyError as e:
            raise ValueError(f"Unknown action: {self._action}") from e

        method = getattr(svc, method_name)
        call_kwargs = self.build_call_kwargs(self._action)
        return method(**call_kwargs)
