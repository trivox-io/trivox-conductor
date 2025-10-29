from __future__ import annotations
from typing import Optional
from .base_contract import Adapter

class WatcherAdapter(Adapter):
    """Watches a folder and emits REPLAY_RENDER_DETECTED on the bus."""
    def set_watch_path(self, path: Optional[str] = None):
        """
        Set the path to watch for replay files.
        
        :param path: Path to watch.
        :type path: Optional[str]
        """
