"""
Setting merger for application settings.
"""

from typing import Tuple


class SettingMerger:
    """
    Setting merger class.
    """

    @staticmethod
    def merge_settings(
        defaults: dict, user_settings: dict
    ) -> Tuple[dict, bool]:
        """
        Merge user settings over defaults.

        :param defaults: Default settings.
        :type defaults: dict

        :param user_settings: User settings, which override defaults.
        :type user_settings: dict

        :return: (merged_settings, changes_detected)
        :rtype: Tuple[dict, bool]
        """

        remove_missing_keys = True

        merged = defaults.copy()
        changes_detected = False

        # Detect changes and merge user settings
        for key, value in user_settings.items():
            if (
                isinstance(value, dict)
                and key in merged
                and isinstance(merged[key], dict)
            ):
                merged[key], sub_changes = SettingMerger.merge_settings(
                    merged[key], value
                )
                changes_detected = changes_detected or sub_changes
            elif key in defaults and merged[key] != value:
                merged[key] = value
                changes_detected = True
            elif (
                key not in defaults
            ):  # User-added key, keep it unless cleanup is enabled
                if not remove_missing_keys:
                    merged[key] = value
                else:
                    changes_detected = True

        # Add new keys from defaults
        for key, value in defaults.items():
            if key not in user_settings:
                merged[key] = value
                changes_detected = True

        return merged, changes_detected

    @staticmethod
    def merge_final(defaults: dict, user_settings: dict) -> dict:
        """
        Merge defaults and user settings without detecting changes,
        for final runtime use.

        :param defaults: Default settings.
        :type defaults: dict

        :param user_settings: User settings, which override defaults.
        :type user_settings: dict

        :return: merged settings.
        :rtype: dict
        """

        merged = defaults.copy()
        merged.update(user_settings)
        return merged
