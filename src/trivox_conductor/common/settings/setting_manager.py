
import os
from abc import ABC, abstractmethod
from typing import Optional

import yaml

from trivox_conductor.common.settings.setting_merger import SettingMerger
from trivox_conductor.common.settings.settings_registry import SettingRegistry


class SettingsManager(ABC):
    """
    Manager for all settings.
    """

    data: dict = {}
    _defaults: Optional[dict] = None
    _user_settings: Optional[dict] = None

    _setting_path: Optional[str] = None
    _configuration_descriptor = (
        f"{os.getenv('TRIVOX_CONFIG_PATH', os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.trivox_conductor/settings'))}/"
    )

    def __init__(self):
        """
        - Try to create the IC Inspector path in the AppData folder if it does not exist.
        - Set the environment variable for the IC Inspector path if it does not exist.
        - Create the settings file if it does not exist.
        """
        self.__ensure_directory()
        self.default_file = self.__set_setting_file(
            self._configuration_descriptor, "default-settings.yml"
        )
        self.user_file = self.__set_setting_file(
            self._configuration_descriptor, "user-settings.yml"
        )

        self.settings_file = self.__set_setting_file(
            self._configuration_descriptor, "settings.yaml"
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

    def __ensure_directory(self):
        """
        Ensure that the directory exists.
        """
        os.makedirs(self._configuration_descriptor, exist_ok=True)

    def __set_setting_file(self, path: str, name: str) -> str:
        """
        Set the setting file path.

        :param path: The path to the settings file.
        :type path: str

        :param name: The name of the settings file.
        :type name: str

        :return: The path to the settings file.
        :rtype: str
        """
        file_path = os.path.join(path, name)
        file_path = file_path.replace("\\", "/")
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("")
        return file_path

    def _load_file(self, file_path: str) -> dict:
        """
        Load settings from a YAML file.

        :param file_path: The path to the settings file.
        :type file_path: str

        :return: The settings data.
        :rtype: dict
        """

        if not os.path.exists(file_path):
            return {}
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

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
