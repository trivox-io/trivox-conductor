"""
Module for managing the mapping between endpoint roles and their
corresponding registry classes.
"""

from __future__ import annotations

from typing import (
    Type,
    Dict,
)


from trivox_conductor.common.registry.endpoint_registry import EndpointRegistry


# type: role string -> concrete registry subclass (e.g. CaptureRegistry)
ROLE_REGISTRIES: Dict[str, Type["EndpointRegistry"]] = {}


def register_role_registry(role: str, registry_cls: Type["EndpointRegistry"]):
    """
    Called by concrete registries (CaptureRegistry, WatcherRegistry, etc.)
    to declare: "I am the registry for role = <role>".
    """
    ROLE_REGISTRIES[role] = registry_cls
