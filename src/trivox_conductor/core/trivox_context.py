# trivox_conductor/core/trivox_context.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional

from trivox_conductor.common.logger import logger

# from trivox_conductor.common.settings import settings
# from trivox_conductor.core.events.bus import BUS
from trivox_conductor.core.manifests.manifest_service import ManifestService

# from trivox_conductor.core.observers.observer_base import ObserverContext
from trivox_conductor.core.profiles.profile_injector import (
    ResolvedCaptureProfile,
    resolve_capture_profile,
)
from trivox_conductor.core.profiles.profile_models import PipelineProfile
from trivox_conductor.core.session.session_manager import (
    SessionInfo,
    SessionManager,
)

# from trivox_conductor.core.registry.capture_registry import CaptureRegistry
# from trivox_conductor.core.registry.watcher_registry import WatcherRegistry
# from trivox_conductor.core.session.session_manager import SessionManager
# from trivox_conductor.modules.capture.services import CaptureService
# from trivox_conductor.modules.watcher.services import WatcherService

# from trivox_conductor.core.observers.bootstrap import attach_all_observers


Role = Literal["capture", "watcher"]  # extend as modules grow


@dataclass
class RoleState:
    # What the CLI processor keeps
    profile_key: Optional[str] = None
    profile: Optional[ResolvedCaptureProfile] = None
    overrides: Dict[str, Any] = field(default_factory=dict)

    # “Runtime” bits
    observers_attached: bool = False


class TrivoxContext:
    """
    Centralized runtime context that mirrors what CLI processors do:
    - Resolve pipeline profiles (per role)
    - Manage overrides
    - Ensure session
    - Build services
    - Attach observers exactly once with a consistent ObserverContext
    """

    _instance: Optional["TrivoxContext"] = None

    _roles: Dict[Role, RoleState] = {}
    _manifest_service: Optional[ManifestService] = None
    # _watcher_service: Optional[WatcherService] = None
    _session_id: Optional[str] = None
    _resolved_profile: Optional[ResolvedCaptureProfile] = None
    session: Optional[SessionInfo] = None

    def __new__(cls) -> "TrivoxContext":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # initialize instance state
            cls._instance._roles.update(
                {
                    "capture": RoleState(),
                    "watcher": RoleState(),
                }
            )
            cls._instance._manifest_service = None
            cls._instance._watcher_service = None
            cls._instance._session_id = None
        return cls._instance

    @property
    def profile(self) -> Optional[PipelineProfile]:
        return self._resolved_profile.profile

    @property
    def overrides(self) -> Dict[str, Any]:
        return self._resolved_profile.overrides

    def set_pipeline_profile(
        self,
        *,
        role: Role,
        pipeline_profile_key: Optional[str],
        overrides: Optional[dict[str, Any]] = None,
    ):
        """
        Resolve and store pipeline profile + overrides for a given role.
        This matches the behavior in TrivoxCaptureCommandProcessor.set_pipeline_profile.
        """
        overrides = overrides or {}
        self._resolved_profile = resolve_capture_profile(
            role, pipeline_profile_key, overrides=overrides
        )

    def set_session(self, session_id: Optional[str]):
        self._session_id = session_id
        self.session = SessionManager.ensure_session(
            session_id=session_id,
            label="trivox_context",
        )


trivox_context = TrivoxContext()


@dataclass
class ContextBuilderData:
    role: Optional[Role] = None
    pipeline_profile_key: Optional[str] = None
    overrides: dict[str, Any] = field(default_factory=dict)
    session_id: Optional[str] = None


class ContextBuilder:
    """
    Helper to build context dicts for UI views, services, etc.
    """

    @staticmethod
    def build_context(
        data: ContextBuilderData,
    ) -> TrivoxContext:
        role: Optional[Role] = data.role
        pipeline_profile_key: Optional[str] = data.pipeline_profile_key
        overrides: dict[str, Any] = data.overrides
        session_id: Optional[str] = data.session_id
        trivox_context.set_pipeline_profile(
            role=role,
            pipeline_profile_key=pipeline_profile_key,
            overrides=overrides,
        )
        trivox_context.set_session(session_id)
        return trivox_context
