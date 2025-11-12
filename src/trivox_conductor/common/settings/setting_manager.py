"""
Manager for application settings.
Handles loading, saving, and merging of settings files.
"""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import yaml

from trivox_conductor.common.settings.setting_merger import SettingMerger
from trivox_conductor.common.settings.settings_registry import SettingRegistry
from trivox_conductor.common.utils.paths import ensure_dir, get_settings_dir


class SettingsManager(ABC):
    """
    Manager for all settings.
    """

    data: dict = {}
    _defaults: Optional[dict] = None
    _user_settings: Optional[dict] = None

    _setting_path: Optional[str] = None

    def __init__(self):
        """
        - Try to create the IC Inspector path in the AppData folder if it does not exist.
        - Set the environment variable for the IC Inspector path if it does not exist.
        - Create the settings file if it does not exist.
        """
        self._settings_dir = ensure_dir(get_settings_dir())
        self._configuration_descriptor = str(self._settings_dir) + os.sep

        # Your naming remains the same
        self.default_file = self.__set_setting_file(
            self._settings_dir, "default-settings.yml"
        )
        self.user_file = self.__set_setting_file(
            self._settings_dir, "user-settings.yml"
        )
        self.settings_file = self.__set_setting_file(
            self._settings_dir, "settings.yaml"
        )

        self._load_file(self.settings_file)

    @property
    def __get_default_settings(self) -> dict:
        """
        Load the initial data for the settings from the registry.

        :return: The initial data for the settings.
        :rtype: dict
        """

        return {
            module: SettingRegistry.get(module)().data
            for module in SettingRegistry.names()
        }

    @abstractmethod
    def save(self):
        """Save the settings data to the settings file."""

    def __set_setting_file(self, base: Path, filename: str) -> Path:
        """
        Set the setting file path.

        :param base: The base directory for the settings file.
        :type base: Path

        :param filename: The name of the settings file.
        :type filename: str

        :return: The path to the settings file.
        :rtype: Path
        """
        path = base / filename
        if not path.exists():
            path.write_text("", encoding="utf-8")  # or create default skeleton
        return path

    def _load_file(self, file_path: Path) -> dict:
        """
        Load settings from a YAML file.

        :param file_path: The path to the settings file.
        :type file_path: Path

        :return: The settings data.
        :rtype: dict
        """
        if not file_path.exists():
            return {}
        return yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}

    def _save_file(self, file_path: str, data: dict):
        """
        Save settings to a YAML file.

        :param file_path: The path to the settings file.
        :type file_path: str

        :param data: The settings data.
        :type data: dict
        """
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False)

    def _get_versions(self) -> tuple:
        """
        Get the version numbers for the default and user settings.

        :return: The version numbers for the default and user settings.
        :rtype: tuple
        """

        return (
            self._defaults.get("version", 0),
            self._user_settings.get("version", 0),
        )

    def _load_setting_files(self):
        """Load defaults and user settings from their respective files."""
        self._defaults = self._load_file(self.default_file)
        self._user_settings = self._load_file(self.user_file)

    def _ensure_settings_content(self):
        """
        Ensure that both default and user settings have a version number.
        Initializes the files if they are missing or incomplete.
        """

        self._defaults = self.__get_default_settings
        self._save_file(self.default_file, self._defaults)

        if not self._user_settings:
            self._user_settings = self._defaults.copy()
            self._save_file(self.user_file, self._user_settings)

    def _sync_files(self):
        """
        If the default version is newer than the user version, update user settings.
        """

        updated_user_settings, changes_detected = SettingMerger.merge_settings(
            self._defaults, self._user_settings
        )

        if changes_detected:
            self._save_file(self.user_file, updated_user_settings)
            self._user_settings = updated_user_settings
            self._save_file(self.default_file, self._defaults)

    def _finalize_settings(self):
        """Merge the final settings for application use and save them."""

        self.data = SettingMerger.merge_final(
            self._defaults, self._user_settings
        )

        self.save()

    def _initialize_data(self):
        """
        Initialize the settings data by merging defaults with file-based settings.
        New defaults will be added to the file without overriding user modifications.
        """

        self._load_setting_files()
        self._ensure_settings_content()
        self._sync_files()
        self._finalize_settings()
