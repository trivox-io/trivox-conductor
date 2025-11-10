"""
A tiny, thread-safe pub/sub event bus for inter-component communication.
"""

from __future__ import annotations

import threading
from collections import defaultdict
from typing import Any, Callable, Dict, List

from trivox_conductor.common.logger import logger

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
        logger.debug(
            "BUS.subscribe: topic=%r handler=%r (total=%d)",
            topic,
            fn,
            len(self._subs[topic]),
        )

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
        logger.debug(
            "BUS.publish: topic=%r handlers=%d payload=%s",
            topic,
            len(subs),
            payload,
        )
        for fn in subs:
            try:
                fn(payload)
            except Exception:
                logger.exception(
                    "Error in BUS subscriber for topic %r: %r", topic, fn
                )


BUS = EventBus()
