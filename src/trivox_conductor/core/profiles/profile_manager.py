"""
Profile management for Trivox Conductor.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import yaml

from trivox_conductor.core.profiles.profile_models import (
    Adapter,
    PipelineProfile,
    PreflightConfig,
)
from trivox_conductor.core.registry import ROLE_REGISTRIES


class ProfileManager:
    """
    Manages pipeline profiles loaded from a YAML configuration.
    """

    def __init__(self, profiles: Dict[str, PipelineProfile]):
        """
        :param profiles: A dictionary of profile key to PipelineProfile.
        :type profiles: Dict[str, PipelineProfile]
        """
        self._profiles = profiles

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ProfileManager":
        """
        Load profiles from a YAML file.

        :param path: Path to the YAML file containing profiles.
        :type path: str | Path

        :return: An instance of ProfileManager with loaded profiles.
        :rtype: ProfileManager
        """
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
            profiles[key] = PipelineProfile(
                key=key,
                label=cfg["label"],
                adapters=adapters,
                pipelines=cfg.get("pipelines", {}) or {},
                hooks=cfg.get("hooks", {}) or {},
            )
        return cls(profiles)

    def list_profiles(self) -> Dict[str, PipelineProfile]:
        """
        List all available pipeline profiles.

        :return: A dictionary of profile key to PipelineProfile.
        :rtype: Dict[str, PipelineProfile]
        """
        return dict(self._profiles)

    def get(self, key: str) -> PipelineProfile:
        """
        Retrieve a pipeline profile by its key.

        :param key: The key of the profile to retrieve.
        :type key: str

        :return: The corresponding PipelineProfile.
        :rtype: PipelineProfile

        :raises KeyError: If the profile key does not exist.
        """
        try:
            return self._profiles[key]
        except KeyError as e:
            raise KeyError(f"Unknown profile '{key}'") from e

    def activate(self, key: str) -> PipelineProfile:
        """
        Apply adapter selection for this profile via registries.

        :param key: The key of the profile to activate.
        :type key: str

        :return: The activated PipelineProfile.
        :rtype: PipelineProfile

        :raises KeyError: If the profile key does not exist.
        """
        profile = self.get(key)

        for role, adapter in profile.adapters.items():
            registry = ROLE_REGISTRIES.get(role)
            if not registry:
                continue
            registry.set_active(adapter.name)

        return profile
