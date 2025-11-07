from enum import Enum, auto


class JobKind(Enum):
    MUX = auto()
    COLOR = auto()
    UPLOAD = auto()
    NOTIFY = auto()
    AI_GENERATE = auto()


class JobState(Enum):
    QUEUED = auto()
    RUNNING = auto()
    DONE = auto()
    FAILED = auto()
