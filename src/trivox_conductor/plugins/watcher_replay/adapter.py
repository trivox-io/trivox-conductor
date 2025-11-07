from __future__ import annotations

import threading
from pathlib import Path
from typing import Dict, Optional, Set, Tuple

from trivox_conductor.common.logger import logger
from trivox_conductor.core.contracts.base_contract import AdapterMeta
from trivox_conductor.core.contracts.watcher import WatcherAdapter
from trivox_conductor.core.events import topics
from trivox_conductor.core.events.bus import BUS


class ReplayWatcherAdapter(WatcherAdapter):
    """
    Simple replay-file watcher.

    - Watches a directory (watch_path) for new files.
    - Uses a polling loop in a background thread (no external deps).
    - Emits REPLAY_RENDER_DETECTED when a new file looks "stable"
      (file size not changing between polls).

    Config keys (from settings/overrides):

        watcher:
          watch_path: "C:/Users/USUARIO/Videos"
          poll_interval_sec: 2.0
          patterns: ["*.mp4", "*.mov"]   # optional

    The ProfileManager will typically inject `watch_path` via profile overrides.
    """

    meta: AdapterMeta = {
        "name": "watcher_replay",
        "role": "watcher",
        "version": "0.1.0",
        "requires_api": ">=1.0,<2.0",
        "capabilities": ["stable_detection", "session_correlation"],
        "source": "local",
    }

    def __init__(self) -> None:
        self._cfg: Dict = {}
        self._sec: Dict = {}
        self._path: Optional[Path] = None

        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # path -> (last_size, stable_count)
        self._seen: Dict[Path, Tuple[int, int]] = {}

    def configure(self, settings: Dict, secrets: Dict) -> None:
        self._cfg, self._sec = settings or {}, secrets or {}
        if not self._path:
            # allow config to define the path if set_watch_path wasn't called yet
            watch_path = self._cfg.get("watch_path")
            if watch_path:
                self.set_watch_path(watch_path)

    def set_watch_path(self, path: Optional[str] = None) -> None:
        if not path:
            logger.debug(
                "ReplayWatcherAdapter.set_watch_path: no path provided"
            )
            return
        p = Path(path)
        self._path = p
        logger.debug("ReplayWatcherAdapter.watch_path set to %s", p)

    def start(self) -> None:
        """
        Start the background polling thread.
        """
        if self._thread and self._thread.is_alive():
            logger.debug("ReplayWatcherAdapter.start: already running")
            return

        if not self._path:
            raise RuntimeError(
                "ReplayWatcherAdapter: watch_path not configured"
            )

        if not self._path.exists() or not self._path.is_dir():
            raise RuntimeError(
                f"ReplayWatcherAdapter: watch_path '{self._path}' does not exist or is not a directory"
            )

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run_loop, name="ReplayWatcherAdapter", daemon=True
        )
        self._thread.start()
        logger.info("ReplayWatcherAdapter started watching %s", self._path)

    def stop(self) -> None:
        """
        Stop the background polling thread.
        """
        if not self._thread:
            return
        self._stop_event.set()
        self._thread.join(timeout=5.0)
        if self._thread.is_alive():
            logger.warning(
                "ReplayWatcherAdapter.stop: thread did not terminate cleanly"
            )
        else:
            logger.info("ReplayWatcherAdapter stopped")
        self._thread = None

    def _run_loop(self) -> None:
        poll_interval = float(self._cfg.get("poll_interval_sec", 2.0))
        patterns = self._cfg.get("patterns") or ["*.*"]

        logger.debug(
            "ReplayWatcherAdapter loop starting: path=%s, interval=%.1fs, patterns=%s",
            self._path,
            poll_interval,
            patterns,
        )

        while not self._stop_event.is_set():
            try:
                self._scan_once(patterns)
            except Exception as e:
                logger.exception("ReplayWatcherAdapter.scan_error: %s", e)
            # use wait so stop() can interrupt sleep
            self._stop_event.wait(poll_interval)

    def _scan_once(self, patterns) -> None:
        if not self._path:
            return

        # discover candidate files
        paths: Set[Path] = set()
        for pattern in patterns:
            for p in self._path.glob(pattern):
                if p.is_file():
                    paths.add(p)

        # track size & stability
        current_seen: Dict[Path, Tuple[int, int]] = {}

        for p in paths:
            try:
                size = p.stat().st_size
            except OSError:
                # transient issues (file deleted/moved between listing and stat)
                continue

            last_size, stable_count = self._seen.get(p, (None, 0))

            if last_size is None:
                # first time we see this file
                current_seen[p] = (size, 0)
            else:
                if size == last_size:
                    stable_count += 1
                else:
                    stable_count = 0
                current_seen[p] = (size, stable_count)

            # emit only when we've seen the same size at least twice
            if stable_count == 1:
                self._on_stable_file(p)

        # update the tracking map
        self._seen = current_seen

    def _on_stable_file(self, path: Path) -> None:
        """
        Called when a file appears to have finished writing (size stable
        across two polls). Here you can parse filename to infer length/fps, etc.
        For now we emit with placeholder length/fps and let SessionCorrelator
        do the session work at the service layer.
        """
        # TODO: parse filename or use ffprobe to get real length/fps
        length_sec = 0.0
        fps = 0

        logger.info("ReplayWatcherAdapter detected new replay: %s", path)
        self._emit_detected(str(path), length_sec, fps)

    # ----- Event emission -------------------------------------------------

    def _emit_detected(self, path: str, length: float, fps: int) -> None:
        """
        Emit a raw detection event.

        NOTE: right now this publishes REPLAY_RENDER_DETECTED directly, which
        means the adapter is already sending the "final" event. If/when you
        want to run it through WatcherService.on_raw_detect for correlation/
        extra rules, change this to publish a RAW_* topic instead and have
        the service subscribe & re-emit the normalized event.
        """
        payload = {
            "path": path,
            "length": length,
            "fps": fps,
            # no session_id here; WatcherService.on_raw_detect will inject it
        }
        BUS.publish(topics.REPLAY_RENDER_DETECTED, payload)
