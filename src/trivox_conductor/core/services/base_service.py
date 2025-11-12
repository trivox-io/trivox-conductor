"""
Base Service Abstraction
========================

Typed, registry-driven service base that loads a configuration model and
coordinates an *adapter* selected via a role-specific registry.

Key Ideas
---------
- **Typed config**: Subclasses set ``SECTION`` and ``MODEL`` (e.g., a dataclass)
  and get a strongly-typed ``self._settings`` loaded from the global settings
  mapping (``settings[SECTION]``).
- **Registry decoupling**: Services depend on a small ``RegistryProto`` interface
  (``get_active()`` / ``set_active()``), never on concrete adapter classes.
- **Adapter configuration**: ``_get_configured_adapter()`` merges base settings
  with optional ``overrides`` and passes them to the adapter's ``configure()``.
- **Defensive defaults**: Missing sections load as empty mappings; type safety is
  enforced with a helpful ``TypeError``.

Subclassing
-----------
Set:
    ``SECTION`` : str
        Name of the settings section (e.g., ``"capture"``).
    ``MODEL`` : Type[TConf]
        Dataclass/Pydantic model used to deserialize the section.

Typical Usage
-------------
    adapter = self._get_configured_adapter(overrides={"session_id": sid})
    adapter.start_capture()

Error Model
-----------
- Raises ``TypeError`` when the settings section is not a mapping.
- Raises ``RuntimeError`` when no active adapter is registered for the section.

This module defines no I/O; orchestration and policy live in concrete services.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Generic, Mapping, Optional, Protocol, Type, TypeVar

TConf = TypeVar("TConf")
TAdapter = TypeVar("TAdapter")


class RegistryProto(Protocol[TAdapter]):
    """
    Protocol for adapter registries used by BaseService.
    """

    def get_active(self) -> Optional[TAdapter]:
        """
        Get the currently active adapter instance, or None if not set.

        :return: Active adapter instance or None.
        :rtype: Optional[TAdapter]
        """

    def set_active(self, name: str):
        """
        Set the active adapter by name.

        :param name: Name of the adapter to set as active.
        :type name: str
        """


class BaseService(Generic[TConf, TAdapter]):
    """
    Base class for services with typed configuration loading.

    :cvar SECTION (str): Configuration section name.
    :cvar MODEL (Type[TConf]): Configuration model class.
    """

    SECTION: str  # override in subclass, e.g. "capture"
    MODEL: Type[TConf]  # override in subclass, e.g. CaptureSettingsModel

    def __init__(
        self, registry: RegistryProto[TAdapter], settings: Mapping[str, Any]
    ):
        """
        :param registry: Adapter registry for the service role.
        :type registry: RegistryProto[TAdapter]

        :param settings: Global settings mapping.
        :type settings: Mapping[str, Any]
        """
        self._registry = registry
        self._settings: TConf = self._load_config(settings)

    def _load_config(self, settings: Mapping[str, Any]) -> TConf:
        raw = settings.get(self.SECTION, {}) or {}
        if not isinstance(raw, Mapping):
            raise TypeError(
                f"Settings section '{self.SECTION}' must be a mapping"
            )
        return self.MODEL(**dict(raw))

    def _get_configured_adapter(
        self,
        *,
        overrides: Optional[Mapping[str, Any]] = None,
        secrets: Optional[Mapping[str, Any]] = None,
    ):
        adapter = self._require_adapter()
        self._configure_adapter(
            adapter, overrides=overrides or {}, secrets=secrets or {}
        )
        return adapter

    def _require_adapter(self) -> TAdapter:
        adapter = self._registry.get_active()
        if not adapter:
            raise RuntimeError(
                f"No active adapter configured for '{self.SECTION}'."
            )
        return adapter

    def _settings_dict(self) -> Mapping[str, Any]:
        settings = self._settings
        return (
            asdict(settings) if is_dataclass(settings) else dict(settings)
        )  # supports dataclass or pydantic

    def _configure_adapter(
        self,
        adapter: TAdapter,
        *,
        overrides: Mapping[str, Any] = None,
        secrets: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        base = dict(self._settings_dict())
        if overrides:
            base.update(overrides)
        # adapter is assumed to implement .configure(settings, secrets)
        adapter.configure(base, secrets or {})
        return base
