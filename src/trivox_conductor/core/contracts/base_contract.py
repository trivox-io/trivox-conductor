"""
Adapter Core Contracts
======================

Common primitives for all adapters, regardless of role (capture, watcher, mux,
uploader, etc.).

Contents
--------
- ``AdapterHealth``: TypedDict for health checks.
- ``AdapterMeta``: TypedDict describing identity and capabilities.
- ``Adapter`` (ABC): Minimal lifecycle every adapter should honor:
  ``configure(settings, secrets)``, optional ``start()/stop()``, and a
  standardized ``health()`` probe.

Guidelines
----------
- **Configuration**: Adapters are configured once via ``configure`` (inject all
  non-sensitive settings + secrets). Avoid reading global state directly.
- **Separation of concerns**: Keep external I/O within adapters; route selection
  and orchestration to services/registries.
- **Health**: ``health()`` should be inexpensive and never throw; return an
  ``AdapterHealth`` dict explaining status for logs/UX.

Extending
---------
Concrete roles (e.g., ``CaptureAdapter``) should subclass ``Adapter`` and define
their own role-specific methods while preserving this common lifecycle.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, TypedDict


class AdapterHealth(TypedDict, total=False):
    """
    Health check result for an adapter.
    
    :cvar ok (bool): Whether the adapter is healthy.
    :cvar message (str): Human-readable status message.
    :cvar details (Dict[str, str]): Optional detailed status information.
    """
    ok: bool
    message: str
    details: Dict[str, str]


class AdapterMeta(TypedDict, total=False):
    """
    Metadata describing an adapter's identity and capabilities.
    
    :cvar name (str): Unique adapter name.
    :cvar version (str): Adapter version string.
    :cvar requires_api (str): Compatible API version range.
    :cvar capabilities (List[str]): Supported features.
    :cvar role (str): Adapter role (e.g., capture, watcher).
    :cvar source (str): Adapter source type (e.g., local, entrypoint).
    """
    name: str
    version: str
    requires_api: str
    capabilities: List[str]
    role: str           # capture, watcher, mux, color, uploader, notifier, ai
    source: str         # "local", "entrypoint", "builtin"

class Adapter(ABC):
    """Minimal lifecycle for any adapter. Concrete roles extend this."""
    meta: AdapterMeta

    @abstractmethod
    def configure(self, settings: Dict, secrets: Dict):
        """
        Apply configuration settings and secrets to the adapter.
        Called once after instantiation, before start().
        
        :param settings: Non-sensitive configuration dictionary.
        :type settings: Dict
        
        :param secrets: Sensitive configuration dictionary.
        :type secrets: Dict
        """

    def start(self):  # watchers/servers
        """
        Start the adapter's main operation.
        """

    def stop(self):
        """
        Stop the adapter's main operation.
        """

    def health(self) -> AdapterHealth:
        """
        Perform a health check on the adapter.
        
        :return: Health status of the adapter.
        :rtype: AdapterHealth
        """
        raise NotImplementedError("health() not implemented for this adapter")
