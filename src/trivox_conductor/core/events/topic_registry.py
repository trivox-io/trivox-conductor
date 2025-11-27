from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class TopicNamespace:
    """Namespace for a group of related topics, e.g. capture, watcher, mux."""

    name: str  # e.g. "capture"
    topics: Dict[str, str]  # e.g. {"STARTED": "capture.started", ...}

    def __getattr__(self, item: str) -> str:
        try:
            return self.topics[item]
        except KeyError:
            raise AttributeError(
                f"No topic '{item}' in namespace '{self.name}'"
            )


class TopicRegistry:
    """Central registry for topic namespaces."""

    def __init__(self) -> None:
        self._namespaces: Dict[str, TopicNamespace] = {}

    def register_namespace(
        self,
        name: str,
        **topics: str,
    ) -> TopicNamespace:
        """
        Register a namespace:

            TOPIC_REGISTRY.register_namespace(
                "capture",
                STARTED="capture.started",
                STOPPED="capture.stopped",
                ERROR="capture.error",
            )
        """
        ns = TopicNamespace(name=name, topics=dict(topics))
        self._namespaces[name] = ns
        return ns

    def namespace(self, name: str) -> TopicNamespace:
        return self._namespaces[name]

    def all_namespaces(self) -> Dict[str, TopicNamespace]:
        return dict(self._namespaces)


TOPIC_REGISTRY = TopicRegistry()
