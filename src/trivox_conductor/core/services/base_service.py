
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Generic, TypeVar, Type, Mapping, Any, Optional, Protocol

TConf = TypeVar("TConf")
TAdapter = TypeVar("TAdapter")


class RegistryProto(Protocol[TAdapter]):
    def get_active(self) -> Optional[TAdapter]: ...
    def set_active(self, name: str) -> None: ...


class BaseService(Generic[TConf, TAdapter]):
    """
    Base class for services with typed configuration loading.
    
    :cvar SECTION (str): Configuration section name.
    :cvar MODEL (Type[TConf]): Configuration model class.
    """

    SECTION: str          # override in subclass, e.g. "capture"
    MODEL: Type[TConf]    # override in subclass, e.g. CaptureSettingsModel

    def __init__(self, registry: RegistryProto[TAdapter], settings: Mapping[str, Any]):
        self._registry = registry
        self._settings: TConf = self._load_config(settings)

    def _load_config(self, settings: Mapping[str, Any]) -> TConf:
        raw = settings.get(self.SECTION, {}) or {}
        if not isinstance(raw, Mapping):
            raise TypeError(f"Settings section '{self.SECTION}' must be a mapping")
        return self.MODEL(**dict(raw))
    
    def _require_adapter(self) -> TAdapter:
        adapter = self._registry.get_active()
        if not adapter:
            raise RuntimeError(f"No active adapter configured for '{self.SECTION}'.")
        return adapter

    def _settings_dict(self) -> Mapping[str, Any]:
        settings = self._settings
        return asdict(settings) if is_dataclass(settings) else dict(settings)  # supports dataclass or pydantic

    def _configure_adapter(self, adapter: TAdapter, *, overrides: Mapping[str, Any] = None, secrets: Mapping[str, Any] = None) -> Mapping[str, Any]:
        base = dict(self._settings_dict())
        if overrides: base.update(overrides)
        # adapter is assumed to implement .configure(settings, secrets)
        adapter.configure(base, secrets or {})
        return base
