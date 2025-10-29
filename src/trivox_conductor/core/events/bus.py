from __future__ import annotations
from typing import Callable, Dict, List, Any
import threading
from collections import defaultdict

Subscriber = Callable[[str, Dict[str, Any]], None]

class EventBus:
    """Tiny, thread-safe pub/sub. Fire-and-forget to avoid UI stalls."""
    def __init__(self) -> None:
        self._subs: Dict[str, List[Subscriber]] = defaultdict(list)
        self._lock = threading.RLock()

    def subscribe(self, topic: str, fn: Subscriber) -> None:
        with self._lock: self._subs[topic].append(fn)

    def publish(self, topic: str, payload: Dict[str, Any]) -> None:
        with self._lock: subs = list(self._subs.get(topic, ()))
        for fn in subs:
            try: fn(topic, payload)
            except Exception: pass  # log in real impl

BUS = EventBus()
