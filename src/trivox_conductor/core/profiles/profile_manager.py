from __future__ import annotations
from typing import Dict
from pathlib import Path
import yaml

from trivox_conductor.core.profiles.profile_models import PipelineProfile, Adapter, PreflightConfig
from trivox_conductor.core.registry.capture_registry import CaptureRegistry
# later: from .mux_registry import MuxRegistry, etc.

ROLE_REGISTRIES = {
    "capture": CaptureRegistry,
    # "watcher": WatcherRegistry,
    # "mux": MuxRegistry, ...
}

class ProfileManager:
    def __init__(self, profiles: Dict[str, PipelineProfile]):
        self._profiles = profiles

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ProfileManager":
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        raw_profiles = data.get("profiles", {}) or {}
        profiles: Dict[str, PipelineProfile] = {}
        for key, cfg in raw_profiles.items():
            adapters = {}
            for role, adapter_cfg in cfg.get("adapters", {}).items():
                preflights = []
                for pf in adapter_cfg.get("preflights", []) or []:
                    preflights.append(
                        PreflightConfig(
                            id=pf["id"],
                            required=pf.get("required"),
                            params=pf.get("params", {}) or {},
                        )
                    )
                adapters[role] = Adapter(
                    name=adapter_cfg["name"],
                    role=role,
                    overrides=adapter_cfg.get("overrides", {}),
                    preflights=preflights,
                )
            profiles[key] = PipelineProfile(key=key, label=cfg["label"], adapters=adapters)
        return cls(profiles)

    def list_profiles(self) -> Dict[str, PipelineProfile]:
        return dict(self._profiles)

    def get(self, key: str) -> PipelineProfile:
        try:
            return self._profiles[key]
        except KeyError as e:
            raise KeyError(f"Unknown profile '{key}'") from e

    def activate(self, key: str) -> PipelineProfile:
        """
        Apply adapter selection for this profile via registries.
        """
        profile = self.get(key)

        for role, adapter in profile.adapters.items():
            registry = ROLE_REGISTRIES.get(role)
            if not registry:
                continue
            registry.set_active(adapter.name)

        return profile
