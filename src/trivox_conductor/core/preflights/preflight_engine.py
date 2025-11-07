"""
Preflight engine to run preflight checks for adapters.
"""

from __future__ import annotations

from typing import Any, List, Mapping, Optional

from trivox_conductor.core.profiles.profile_models import (
    Adapter,
    PipelineProfile,
)

from .preflight_registry import PreflightRegistry
from .preflight_types import PreflightContext, PreflightFailure, Role


def run_preflights(
    *,
    role: Role,
    profile: Optional[PipelineProfile],
    adapter: Any,
    base_settings: Mapping[str, Any],
    session_id: Optional[str] = None,
) -> List[PreflightFailure]:
    """
    Run preflight checks for a given adapter role and profile.

    :param role: The adapter role (e.g., 'capture', 'uploader').
    :type role: Role

    :param profile: The pipeline profile containing adapter configurations.
    :type profile: Optional[PipelineProfile]

    :param adapter: The adapter instance to run preflights against.
    :type adapter: Any

    :param base_settings: Base settings to use for preflight checks.
    :type base_settings: Mapping[str, Any]

    :param session_id: Optional session identifier for context.
    :type session_id: Optional[str]

    :return: List of preflight failures encountered.
    :rtype: List[PreflightFailure]
    """
    if profile is None:
        return []

    adapter_cfg: Optional[Adapter] = profile.adapters.get(role)
    if not adapter_cfg:
        return []

    failures: List[PreflightFailure] = []

    for pf_cfg in adapter_cfg.preflights:
        check = PreflightRegistry.get(role, pf_cfg.id)

        # merge base settings + per-preflight params
        effective_settings = dict(base_settings)
        effective_settings.update(pf_cfg.params or {})

        ctx = PreflightContext(
            role=role,
            settings=effective_settings,
            adapter=adapter,
            session_id=session_id,
            profile_key=profile.key,
        )
        result = check(ctx)
        if result is None:
            continue

        # Let the profile override required flag if it wants
        if pf_cfg.required is not None:
            result.required = pf_cfg.required
        else:
            result.required = getattr(check, "default_required", True)

        failures.append(result)

    return failures
