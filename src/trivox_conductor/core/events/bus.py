"""
A tiny, thread-safe pub/sub event bus for inter-component communication.
"""

from __future__ import annotations

import threading
from collections import defaultdict
from typing import Any, Callable, Dict, List

Subscriber = Callable[[str, Dict[str, Any]], None]


class EventBus:
    """Tiny, thread-safe pub/sub. Fire-and-forget to avoid UI stalls."""

    def __init__(self):
        self._subs: Dict[str, List[Subscriber]] = defaultdict(list)
        self._lock = threading.RLock()

    def subscribe(self, topic: str, fn: Subscriber):
        """
        Subscribe to a topic.

        :param topic: Topic name.
        :type topic: str

        :param fn: Callback function to invoke on event.
        :type fn: Subscriber
        """
        with self._lock:
            self._subs[topic].append(fn)

    def publish(self, topic: str, payload: Dict[str, Any]):
        """
        Publish an event to a topic.

        :param topic: Topic name.
        :type topic: str

        :param payload: Event payload.
        :type payload: Dict[str, Any]
        """
        with self._lock:
            subs = list(self._subs.get(topic, ()))
        for fn in subs:
            try:
                fn(topic, payload)
            except Exception:
                pass  # log in real impl


BUS = EventBus()
