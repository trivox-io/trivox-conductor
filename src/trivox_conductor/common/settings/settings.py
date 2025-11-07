"""
Settings management for the application.
Provides the Settings class for managing application settings.
"""

from typing import Any, Optional

import yaml

from trivox_conductor.common.settings.setting_manager import SettingsManager


class Settings(SettingsManager):
    """
    This class is used to manage the settings for the application.

    :cvar _instance: Optional[Settings]: Singleton instance of the Settings class.
    """

    _instance = None

    def __new__(cls) -> "Settings":
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def populate(self, from_scratch: bool = True):
        """
        Populate the settings with the initial data based on the registry.

        :param from_scratch: If True, the settings will be populated from scratch.
        :type from_scratch: bool
        """

        if not from_scratch:
            self.data = self._load_file(self.settings_file)
            return

        self._initialize_data()

    def get(
        self, key: Optional[str] = None, default: Optional[Any] = None
    ) -> dict:
        """
        Get the settings data.

        :param key: The key to get from the settings.
        :type key: Optional[str]

        :param default: The default value if the key is not found.
        :type default: Optional[Any]

        :return: The settings data.
        :rtype: dict
        """
        data = self.data
        if key is None:
            return data
        keys = key.split(".")
        for key_ in keys:
            data = data.get(key_, default)
            if data is None:
                return default
        return data

    def add(self, data: dict):
        """
        Add data to the settings.

        :param data: The data to add to the settings.
        :type data: dict
        """
        self.data.update(data)

    def save(self):
        """
        Save the settings data to the settings file.
        """
        with open(self.settings_file, "w", encoding="utf-8") as file:
            yaml.dump(self.data, file, default_flow_style=False)


settings = Settings()
