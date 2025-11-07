
from typing import Type, Mapping, Any, Optional

from trivox_conductor.common.logger import logger
from trivox_conductor.common.commands.base_command_processor import BaseCommandProcessor
from trivox_conductor.core.profiles.profile_injector import resolve_capture_profile, ResolvedCaptureProfile


class TrivoxCaptureCommandProcessor(BaseCommandProcessor):
    """
    Command processor for Trivox Capture commands.
    
    :cvar SERVICE_CLS (Type): The service class to instantiate.
    :cvar ACTION_MAP (Mapping[str, str]): Mapping of action names to service method names.
    """

    SERVICE_CLS: Type        # e.g. CaptureService
    ACTION_MAP: Mapping[str, str]  # e.g. {"start": "start", "stop": "stop"}
    _overrides: Optional[dict[str, Any]] = None
    _pipeline_profile: Optional[ResolvedCaptureProfile] = None

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._pipeline_profile_key: Optional[str] = self._kwargs.get("pipeline_profile")
        
        # TODO: Implement profile application logic
        self._config_file_path : Optional[str] = self._kwargs.get("config")
    
    def set_pipeline_profile(self, overrides: dict[str, Any]):
        """Set connection overrides for the processor."""
        resolved = resolve_capture_profile(
            self._pipeline_profile_key,
            overrides=overrides,
        )
        self._overrides = resolved.overrides
        self._pipeline_profile = resolved.profile

    def build_service(self):
        """Subclasses build the service with proper registries/settings."""
        raise NotImplementedError

    def build_call_kwargs(self, action: str) -> dict[str, Any]:
        """Subclasses decide which kwargs go into each service call."""
        logger.debug(f"Building call kwargs for action: {action}")
        return {}

    def run(self):
        svc = self.build_service()
        action = self._kwargs.get("action")
        if not action:
            raise ValueError("Action is required")

        try:
            method_name = self.ACTION_MAP[action]
        except KeyError as e:
            raise ValueError(f"Unknown action: {action}") from e

        method = getattr(svc, method_name)
        call_kwargs = self.build_call_kwargs(action)
        return method(**call_kwargs)