"""
OBSAdapter
==========

An implementation of :class:`~trivox_conductor.core.contracts.capture.CaptureAdapter`
that integrates with OBS Studio through `obsws-python` (WebSocket v5).

Design Notes
------------
- **DIP / SRP**: Keeps only OBS-specific I/O here; orchestration lives in the module
  service layer (e.g., selection, preflight, state persistence).
- **Defensive parsing**: OBS/SDK responses vary across versions; parsing accepts both
  dataclass-like attributes and plain dict payloads.
- **Idempotent-ish stop**: `stop_capture()` is safe to call even if OBS is already
  stopped; the service also probes `is_recording()` when needed.
- **Events**: Emits CAPTURE_STARTED / CAPTURE_STOPPED / CAPTURE_ERROR with the current
  `session_id` when available.

Configuration keys consumed via ``configure(settings, secrets)``::
    {
        "host": "127.0.0.1",
        "port": 4455,
        "password": "...",
        "request_timeout_sec": 3.0,
        "session_id": "20251029_1050_s0_e0_test"
    }

Public API
----------
- :meth:`list_scenes`
- :meth:`list_profiles`
- :meth:`select_scene`
- :meth:`select_profile`
- :meth:`start_capture`
- :meth:`stop_capture`
- :meth:`is_recording`
- :meth:`health`

Exceptions
----------
Most OBS SDK exceptions are wrapped as :class:`RuntimeError` with a helpful message
so that callers do not need to import SDK-specific error types.
"""

from __future__ import annotations

import logging
from contextlib import suppress
from typing import Dict, List, Optional

import obsws_python as obsws
from obsws_python import error as obs_err

from trivox_conductor.core.contracts.base_contract import AdapterMeta
from trivox_conductor.core.contracts.capture import CaptureAdapter
from trivox_conductor.core.events import topics
from trivox_conductor.core.events.bus import BUS

logger = logging.getLogger(__name__)


class OBSAdapter(CaptureAdapter):
    """
    Capture adapter for OBS (Open Broadcaster Software).
    Implements the CaptureAdapter contract.

    :cvar meta (AdapterMeta): Metadata describing the adapter.
    """

    meta: AdapterMeta = {
        "name": "capture_obs",
        "role": "capture",
        "version": "0.1.0",
        "requires_api": ">=1.0,<2.0",
        "capabilities": ["scenes:list", "profiles:list"],
        "source": "local",
    }

    def __init__(self):
        self._settings: Dict = {}
        self._secrets: Dict = {}
        self._client: Optional[obsws.ReqClient] = None
        self._session_id: Optional[str] = None

    def configure(self, settings: Dict, secrets: Dict):
        self._settings = settings or {}
        self._secrets = secrets or {}
        self._session_id = self._settings.get("session_id")

    def _ensure_client(self) -> obsws.ReqClient:
        if self._client is not None:
            return self._client

        logger.debug(f"Setting up OBS client with settings: {self._settings}")
        host = self._settings.get("host", "127.0.0.1")
        port = int(self._settings.get("port", 4455))
        password = self._settings.get("password", "")
        timeout = float(self._settings.get("request_timeout_sec", 3.0))

        try:
            self._client = obsws.ReqClient(
                host=host, port=port, password=password, timeout=timeout
            )
        except Exception as e:
            self._client = None
            logger.error(f"OBS connect failed: {e}")
            raise RuntimeError(f"OBS connect failed: {e}") from e

        return self._client

    def _extract_scene_name(self, item) -> Optional[str]:
        """Accept both dataclass-style attrs and dict payloads."""
        if isinstance(item, dict):
            return (
                item.get("sceneName")
                or item.get("scene_name")
                or item.get("name")
            )
        return (
            getattr(item, "scene_name", None)
            or getattr(item, "sceneName", None)
            or getattr(item, "name", None)
        )

    def health(self):
        try:
            c = self._ensure_client()
            # simple ping via GetVersion
            _ = c.get_version()
            return {"ok": True, "message": "ok"}
        except Exception as e:
            return {"ok": False, "message": f"obs-unreachable: {e}"}

    def list_scenes(self) -> List[str]:
        c = self._ensure_client()
        try:
            c = self._ensure_client()
            res = c.get_scene_list()
            items = getattr(res, "scenes", []) or []
            names = [self._extract_scene_name(it) for it in items]
            names = [n for n in names if n]  # drop Nones
            logger.debug("OBS scenes resolved: %s", names)
            return names
        except obs_err.OBSSDKTimeoutError as e:
            raise RuntimeError(f"GetSceneList failed: {e}") from e

    def list_profiles(self) -> List[str]:
        c = self._ensure_client()
        # Try the modern call first
        try:
            res = c.get_profile_list()
            items = getattr(res, "profiles", []) or []
        except Exception:
            # Some builds expose different structure or none at all
            return []
        # profiles can be list[str] or list[dict]
        out = []
        for it in items:
            if isinstance(it, str):
                out.append(it)
            elif isinstance(it, dict):
                out.append(it.get("profileName") or it.get("name"))
            else:
                out.append(
                    getattr(it, "profile_name", None)
                    or getattr(it, "profileName", None)
                )
        result = [p for p in out if p]
        logger.debug("OBS profiles resolved: %s", result)
        return result

    def select_scene(self, name: str):
        if not name:
            return
        c = self._ensure_client()
        try:
            c.set_current_program_scene(name)  # SetCurrentProgramScene
        except obs_err.OBSSDKTimeoutError as e:
            raise RuntimeError(
                f"SetCurrentProgramScene('{name}') failed: {e}"
            ) from e

    def select_profile(self, name: str):
        if not name:
            return
        c = self._ensure_client()
        with suppress(obs_err.OBSSDKTimeoutError, AttributeError):
            c.set_current_profile(name)  # SetCurrentProfile
            return
        # if not supported, ignore gracefully
        # (You can log a warning from your central logger here)

    def start_capture(self):
        c = self._ensure_client()
        try:
            # Apply mixer settings *before* we start recording
            self._apply_mixer(c)
            c.start_record()  # StartRecord
        except obs_err.OBSSDKTimeoutError as e:
            BUS.publish(
                topics.CAPTURE_ERROR,
                {"session_id": self._session_id, "error": str(e)},
            )
            raise RuntimeError(f"StartRecord failed: {e}") from e

        BUS.publish(topics.CAPTURE_STARTED, {"session_id": self._session_id})

    def stop_capture(self):
        c = self._ensure_client()
        try:
            # StopRecord returns outputPath in response; emit it if present.
            res = c.stop_record()  # StopRecord
            output_path = getattr(res, "output_path", None)
        except obs_err.OBSSDKTimeoutError as e:
            BUS.publish(
                topics.CAPTURE_ERROR,
                {"session_id": self._session_id, "error": str(e)},
            )
            raise RuntimeError(f"StopRecord failed: {e}") from e

        payload = {"session_id": self._session_id}
        if output_path:
            payload["output_path"] = output_path
        BUS.publish(topics.CAPTURE_STOPPED, payload)

    def is_recording(self) -> bool:
        c = self._ensure_client()
        res = c.get_record_status()  # returns { "outputActive": bool, ... }
        # SDK may map to attributes or dict; keep it defensive:
        active = getattr(res, "output_active", None)
        if active is None and isinstance(getattr(res, "attrs", None), dict):
            active = res.attrs.get("outputActive")
        if active is None:
            # last fallback if response was returned as plain dict somewhere upstream
            active = getattr(res, "outputActive", False)
        return bool(active)

    def _apply_mixer(self, c: obsws.ReqClient) -> None:
        """
        Apply simple mixer config based on settings:

          - desktop_source_name: str
          - mic_source_name: str
          - capture_desktop_audio: bool (default True)
          - capture_mic_audio: bool (default False)

        We implement this as mute/unmute on the corresponding inputs.
        """
        desktop_name = self._settings.get("desktop_source_name")
        mic_name = self._settings.get("mic_source_name")

        desktop_on = bool(self._settings.get("capture_desktop_audio", True))
        mic_on = bool(self._settings.get("capture_mic_audio", False))

        # Desktop
        if desktop_name:
            try:
                # mute when we *don’t* want to capture
                c.set_input_mute(desktop_name, not desktop_on)
                logger.debug(
                    "obs.mixer.desktop: %s -> %s",
                    desktop_name,
                    "ON" if desktop_on else "MUTED",
                )
            except Exception as e:
                logger.warning(
                    "obs.mixer.desktop_failed - %s: %s", desktop_name, e
                )

        # Mic
        if mic_name:
            try:
                c.set_input_mute(mic_name, not mic_on)
                logger.debug(
                    "obs.mixer.mic: %s -> %s",
                    mic_name,
                    "ON" if mic_on else "MUTED",
                )
            except Exception as e:
                logger.warning("obs.mixer.mic_failed - %s: %s", mic_name, e)
