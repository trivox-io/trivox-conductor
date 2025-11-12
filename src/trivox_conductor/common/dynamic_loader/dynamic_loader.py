from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Optional

import trivox_conductor.constants as trivox_constants
from trivox_conductor.common.logger import logger


@dataclass(frozen=True)
class Candidate:
    """A discovered thing we might load."""

    name: str  # module/package id, or path label
    path: Optional[Path] = None  # optional filesystem path
    extra: Optional[dict] = None  # anything else you want to pass to on_load


@dataclass
class LoaderContext:
    """Shared context you can pass around if needed."""

    constants = trivox_constants  # for convenience


@dataclass
class LoaderSpec:
    name: str
    discover: Callable[[LoaderContext], Iterable[Candidate]]
    condition: Callable[[Candidate], bool]
    on_load: Callable[[Candidate, LoaderContext], None]
    after_all: Optional[Callable[[LoaderContext], None]] = None


class DynamicLoader:
    def __init__(self) -> None:
        self._specs: list[LoaderSpec] = []

    def register(self, spec: LoaderSpec) -> None:
        self._specs.append(spec)

    def load_all(self) -> None:
        ctx = LoaderContext()
        for spec in self._specs:
            logger.debug("Loader[%s]: discovering...", spec.name)
            loaded_count = 0
            for cand in spec.discover(ctx):
                try:
                    if not spec.condition(cand):
                        continue
                    spec.on_load(cand, ctx)
                    loaded_count += 1
                except Exception as e:
                    logger.exception(
                        "Loader[%s]: candidate %s failed: %s",
                        spec.name,
                        cand.name,
                        e,
                    )
            if spec.after_all:
                try:
                    spec.after_all(ctx)
                except Exception as e:
                    logger.exception(
                        "Loader[%s].after_all failed: %s", spec.name, e
                    )
            logger.info(
                "Loader[%s]: processed %d candidate(s)",
                spec.name,
                loaded_count,
            )
