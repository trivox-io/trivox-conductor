# trivox_conductor/core/profiles/injector.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional, Mapping

from trivox_conductor.core.profiles import profile_manager
from trivox_conductor.core.profiles.profile_models import PipelineProfile


@dataclass
class ResolvedCaptureProfile:
    profile: Optional[PipelineProfile]
    overrides: Dict[str, Any]


def resolve_capture_profile(
    profile_key: Optional[str],
    overrides: Mapping[str, Any] | None = None,
) -> ResolvedCaptureProfile:
    """
    - If profile_key is given:
        * activates the profile (sets registries)
        * merges profile.capture_overrides + profile.preflight_flags + overrides
    - If profile_key is None:
        * does not touch registries
        * returns overrides as-is
    """
    incoming_overrides = dict(overrides or {})

    if not profile_key:
        return ResolvedCaptureProfile(profile=None, overrides=incoming_overrides)

    # Activates adapters as a side-effect
    profile = profile_manager.activate(profile_key)

    capture_adapter = profile.adapters.get("capture")
    base: Dict[str, Any] = {}
    if capture_adapter:
        base.update(capture_adapter.overrides)

    merged = {
        **base,
        **incoming_overrides,  # CLI/GUI wins on conflicts
    }
    return ResolvedCaptureProfile(profile=profile, overrides=merged)
