from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from .dynamic_loader import Candidate, LoaderContext, LoaderSpec


class BaseLoader(ABC):
    """
    Base class for domain loaders.
    Subclasses implement discover/condition/on_load and optionally after_all.
    """

    NAME: str = "base"

    def build_spec(self) -> LoaderSpec:
        return LoaderSpec(
            name=self.NAME,
            discover=self.discover,
            condition=self.condition,
            on_load=self.on_load,
            after_all=self.after_all,
        )

    @abstractmethod
    def discover(self, ctx: LoaderContext) -> Iterable[Candidate]: ...

    def condition(self, cand: Candidate) -> bool:
        """Default: always load."""
        return True

    @abstractmethod
    def on_load(self, cand: Candidate, ctx: LoaderContext) -> None: ...

    def after_all(self, ctx: LoaderContext) -> None:
        """Optional hook."""
        return None
