from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, Tuple

from trivox_conductor.common.module_meta import ModuleMeta

CaptureAction = Literal["start", "stop", "list_scenes", "list_profiles"]


@dataclass(frozen=True)
class CaptureActions:
    START: Final[CaptureAction] = "start"
    STOP: Final[CaptureAction] = "stop"
    LIST_SCENES: Final[CaptureAction] = "list_scenes"
    LIST_PROFILES: Final[CaptureAction] = "list_profiles"

    ALL: Final[Tuple[CaptureAction, ...]] = (
        START,
        STOP,
        LIST_SCENES,
        LIST_PROFILES,
    )


CAPTURE_MODULE: Final[ModuleMeta] = ModuleMeta(
    key="capture",
    actions=CaptureActions.ALL,
)
