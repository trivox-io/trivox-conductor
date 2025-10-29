
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
