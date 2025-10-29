"""
Capture Role Contract
=====================

Defines the minimal interface for **capture** adapters (e.g., OBS, in-game,
or virtual recorders). Implementations are responsible for *I/O* and system
integration; higher-level orchestration lives in services.

Required Capabilities
---------------------
- **Discovery**: ``list_scenes()``, ``list_profiles()``
- **Selection**: ``select_scene(name)``, ``select_profile(name)``
- **Lifecycle**: ``start_capture()``, ``stop_capture()``
- **Status**: ``is_recording() -> bool``

Notes
-----
- Implementations should be **idempotent** where practical (e.g., stopping when
  already stopped).
- Prefer raising ``RuntimeError`` with actionable messages rather than leaking
  SDK-specific exceptions.
- Keep network/process I/O inside the adapter; do not load global settings here—use
  ``configure(settings, secrets)`` invoked by the calling service.
"""

from __future__ import annotations
from typing import List
from .base_contract import Adapter


class CaptureAdapter(Adapter):
    """
    Contract for capture adapters (OBS, Minecraft, etc).
    e.g., OBS: connect/auth, start/stop, list scenes/profiles.
    """

    def list_scenes(self) -> List[str]:
        """
        List available capture scenes.
        
        :return: List of scene names.
        :rtype: List[str]
        """

    def list_profiles(self) -> List[str]:
        """
        List available capture profiles.
        
        :return: List of profile names.
        :rtype: List[str]
        """

    def select_scene(self, name: str):
        """
        Select a capture scene by name.
        
        :param name: Name of the scene to select.
        :type name: str
        """
        
    def select_profile(self, name: str):
        """
        Select a capture profile by name.
        
        :param name: Name of the profile to select.
        :type name: str
        """
        
    def start_capture(self):
        """
        Start the capture process.
        """
        
    def stop_capture(self):
        """
        Stop the capture process.
        """
    
    def is_recording(self) -> bool:
        """
        Check if capture is currently active.
        
        :return: True if recording, False otherwise.
        :rtype: bool
        """
