from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class PreflightConfig:
    id: str
    required: Optional[bool] = None     # None => use check’s default
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Adapter:
    name: str
    role: str
    overrides: Dict[str, Any] = field(default_factory=dict)
    preflights: List[PreflightConfig] = field(default_factory=list)


@dataclass
class PipelineProfile:
    key: str
    label: str
    adapters: Dict[str, Adapter] = field(default_factory=dict)
