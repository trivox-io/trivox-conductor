"""
Capture State Store
===================

Tiny persistence layer for :class:`~trivox_conductor.modules.capture.state.CaptureState`.
Serializes state to a JSON file under the tool's appdata directory, enabling
stateless CLI executions to share current capture status.

Behavior
--------
- ``load()``: returns a valid ``CaptureState`` even if the file is missing/corrupt.
- ``save(state)``: atomic write using a ``.tmp`` file then ``os.replace``.
- ``clear()``: removes the state file if it exists.

Notes
-----
- The storage path is derived from the package location; adjust ``_appdata_dir()``
  if your deployment layout changes.
- This module performs no locking; single-writer (CLI) is assumed.
"""

from __future__ import annotations

import contextlib
import json
import os
from dataclasses import asdict

import trivox_conductor.constants as trivox_constants

from .state import CaptureState


def _appdata_dir() -> str:
    """
    Determine the application data directory for storing state files.

    :return: Path to the appdata storage directory.
    :rtype: str
    """
    base = os.path.join(trivox_constants.ROOT_DIR, ".trivox")
    path = os.path.join(base, "storage")
    os.makedirs(path, exist_ok=True)
    return path


class CaptureStateStore:
    """
    Persistence layer for CaptureState using JSON file storage.
    """

    def __init__(self, filename: str = "capture_state.json"):
        """
        :param filename: Name of the JSON file for storing state.
        :type filename: str
        """
        self._path = os.path.join(_appdata_dir(), filename)

    def load(self) -> CaptureState:
        """
        Load the persisted CaptureState from the JSON file.

        :return: Loaded CaptureState instance.
        :rtype: CaptureState
        """
        if not os.path.exists(self._path):
            return CaptureState()
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return CaptureState(**data)
        except Exception:
            # Corrupt or unexpected → start clean
            return CaptureState()

    def save(self, state: CaptureState):
        """
        Save the given CaptureState to the JSON file.

        :param state: CaptureState instance to persist.
        :type state: CaptureState
        """
        tmp = self._path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(asdict(state), f, ensure_ascii=False, indent=2)
        os.replace(tmp, self._path)

    def clear(self):
        """
        Remove the persisted CaptureState file if it exists.
        """
        with contextlib.suppress(FileNotFoundError):
            os.remove(self._path)
            os.remove(self._path)
