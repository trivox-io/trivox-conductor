from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
from .types import JobKind

# A stage is a named step that expects an event to advance
@dataclass
class PipelineStage:
    name: str
    kind: JobKind
    waits_for_topic: Optional[str] = None  # advance trigger (e.g., MUX_DONE)
    next_stages: List[str] = field(default_factory=list)

@dataclass
class Pipeline:
    name: str
    stages: Dict[str, PipelineStage]
    entry: str

# Example named DAGs (wire actual topics at runtime/UI)
IGREADY = Pipeline(
    name="IGReady",
    stages={
        "mux": PipelineStage(name="mux", kind=JobKind.MUX, waits_for_topic=None, next_stages=[]),
    },
    entry="mux",
)

IGCOLOR = Pipeline(
    name="IGColor",
    stages={
        "color": PipelineStage(name="color", kind=JobKind.COLOR, waits_for_topic=None, next_stages=[]),
    },
    entry="color",
)

HANDOFF = Pipeline(
    name="Handoff",
    stages={
        "upload": PipelineStage(name="upload", kind=JobKind.UPLOAD, waits_for_topic=None, next_stages=["notify"]),
        "notify": PipelineStage(name="notify", kind=JobKind.NOTIFY, waits_for_topic=None, next_stages=[]),
    },
    entry="upload",
)
