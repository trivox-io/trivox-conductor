# trivox_conductor/core/preflight/engine.py
from __future__ import annotations
from typing import Mapping, Any, List, Optional

from .preflight_registry import PreflightRegistry
from .preflight_types import PreflightContext, PreflightFailure, Role
from trivox_conductor.core.profiles.profile_models import PipelineProfile, Adapter


def run_preflights(
    *,
    role: Role,
    profile: Optional[PipelineProfile],
    adapter: Any,
    base_settings: Mapping[str, Any],
    session_id: Optional[str] = None,
) -> List[PreflightFailure]:
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
