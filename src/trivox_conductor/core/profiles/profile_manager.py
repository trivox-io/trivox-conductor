"""
Profile management for Trivox Conductor.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Dict, Mapping

import yaml

from trivox_conductor.common.logger import logger
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

    @staticmethod
    def _deep_merge(
        base: Dict[str, Any], override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recursive dict merge.

        - If both base[k] and override[k] are dicts -> merge them.
        - Otherwise override[k] wins.

        Returns a new dict, does not mutate inputs.
        """
        result: Dict[str, Any] = copy.deepcopy(base)
        for k, v in override.items():
            if (
                k in result
                and isinstance(result[k], dict)
                and isinstance(v, dict)
            ):
                result[k] = ProfileManager._deep_merge(result[k], v)
            else:
                result[k] = copy.deepcopy(v)
        return result

    @classmethod
    def from_mapping(cls, raw_profiles: Mapping[str, Any]) -> "ProfileManager":
        """
        Build a ProfileManager from an in-memory mapping of profiles.

        :param raw_profiles: Mapping of profile key -> raw dict config.
        """
        profiles: Dict[str, PipelineProfile] = {}

        for key, cfg in raw_profiles.items():
            adapters: Dict[str, Adapter] = {}
            for role, adapter_cfg in (cfg.get("adapters", {}) or {}).items():
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
                    overrides=adapter_cfg.get("overrides", {}) or {},
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

    @classmethod
    def from_base_and_dir(
        cls,
        base_path: str | Path,
        extra_dir: str | Path | None,
    ) -> "ProfileManager":
        """
        Load profiles from a base YAML file plus zero or more extra YAML files
        in a directory (user/local profiles).

        Extra profiles can declare:

            extends: <parent_profile_key>

        In that case, the child profile's config is deep-merged on top of the
        parent profile's raw dict.
        """
        base_data = (
            yaml.safe_load(Path(base_path).read_text(encoding="utf-8")) or {}
        )
        merged_raw: Dict[str, Any] = base_data.get("profiles", {}) or {}

        if extra_dir is not None:
            logger.debug(f"Loading extra profiles from: {extra_dir}")
            extra_dir_path = Path(extra_dir)
            logger.debug(f"Extra dir path is dir: { extra_dir_path.is_dir()}")
            if extra_dir_path.is_dir():
                logger.debug(f"Scanning extra profiles in: {extra_dir_path}")
                for path in extra_dir_path.iterdir():
                    if path.suffix.lower() not in (".yml", ".yaml"):
                        continue

                    local_data = (
                        yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                    )
                    logger.debug(f"Loaded local profiles from: {path}")
                    local_profiles = local_data.get("profiles", {}) or {}

                    for profile_key, cfg in local_profiles.items():
                        parent_name = cfg.get("extends")
                        if parent_name:
                            parent_cfg = merged_raw.get(parent_name)
                            if parent_cfg is None:
                                raise ValueError(
                                    f"Profile '{profile_key}' extends unknown "
                                    f"profile '{parent_name}' (in {path})"
                                )
                            # We don't keep `extends` in the final config
                            child_cfg = {
                                k: v for k, v in cfg.items() if k != "extends"
                            }
                            merged_raw[profile_key] = cls._deep_merge(
                                parent_cfg, child_cfg
                            )
                        else:
                            # New standalone profile, no inheritance
                            merged_raw[profile_key] = cfg

        logger.debug(f"Merged profile configs: {merged_raw}")
        return cls.from_mapping(merged_raw)

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
        logger.debug(
            f"Activating profile '{key}' with adapters: {profile.adapters}"
        )

        for role, adapter in profile.adapters.items():
            registry = ROLE_REGISTRIES.get(role)
            if not registry:
                continue
            registry.set_active(adapter.name)

        return profile
