"""
Profile models for Trivox Conductor.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PreflightConfig:
    """
    Configuration for a preflight check within an adapter.

    :cvar id: The unique identifier of the preflight check.
    :cvar required: Whether this preflight is required.
    :cvar params: Additional parameters for the preflight check.
    """

    id: str
    required: Optional[bool] = None  # None => use check’s default
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Adapter:
    """
    Configuration for an adapter within a pipeline profile.

    :cvar name: The name of the adapter to use.
    :cvar role: The role of the adapter (e.g., 'capture', 'uploader').
    :cvar overrides: Specific overrides for this adapter.
    :cvar preflights: List of preflight check configurations for this adapter.
    """

    name: str
    role: str
    overrides: Dict[str, Any] = field(default_factory=dict)
    preflights: List[PreflightConfig] = field(default_factory=list)


@dataclass
class PipelineProfile:
    """
    Represents a pipeline profile configuration.

    :cvar key: The unique key of the profile.
    :cvar label: The human-readable label of the profile.
    :cvar adapters: A dictionary of adapter role to Adapter configuration.
    """

    key: str
    label: str
    adapters: Dict[str, Adapter] = field(default_factory=dict)
