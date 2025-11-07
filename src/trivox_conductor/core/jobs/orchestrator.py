from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict

from trivox_conductor.core.events.bus import BUS

from .pipelines import Pipeline
from .types import JobKind, JobState


@dataclass
class Job:
    id: str
    kind: JobKind
    payload: Dict[str, Any]
    state: JobState = JobState.QUEUED


class JobOrchestrator:
    """
    Minimal orchestrator skeleton. Modules enqueue jobs and subscribe to BUS to mark done/failed.
    You can expand this with concurrency limits, retries, persistence, etc.
    """

    def __init__(self) -> None:
        self._jobs: Dict[str, Job] = {}
        self._handlers: Dict[JobKind, Callable[[Job], None]] = {}

    def register_handler(
        self, kind: JobKind, handler: Callable[[Job], None]
    ) -> None:
        self._handlers[kind] = handler

    def enqueue(self, job: Job) -> None:
        self._jobs[job.id] = job
        self._run(job)

    def _run(self, job: Job) -> None:
        job.state = JobState.RUNNING
        handler = self._handlers.get(job.kind)
        if not handler:
            job.state = JobState.FAILED
            return
        try:
            handler(job)  # handler should publish progress/done to BUS
        except Exception:
            job.state = JobState.FAILED

    def mark_done(self, job_id: str) -> None:
        if job_id in self._jobs:
            self._jobs[job_id].state = JobState.DONE

    def mark_failed(self, job_id: str) -> None:
        if job_id in self._jobs:
            self._jobs[job_id].state = JobState.FAILED
