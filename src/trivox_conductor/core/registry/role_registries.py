"""
Module for managing the mapping between implementation roles and their
corresponding registry classes.
"""

from __future__ import annotations

from typing import Dict, Type

from trivox_conductor.common.registry.implementation_registry import (
    ImplementationRegistry,
)

# type: role string -> concrete registry subclass (e.g. CaptureRegistry)
ROLE_REGISTRIES: Dict[str, Type["ImplementationRegistry"]] = {}


def register_role_registry(
    role: str, registry_cls: Type["ImplementationRegistry"]
):
    """
    Called by concrete registries (CaptureRegistry, WatcherRegistry, etc.)
    to declare: "I am the registry for role = <role>".
    """
    ROLE_REGISTRIES[role] = registry_cls
