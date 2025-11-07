from __future__ import annotations

import importlib
import os
from dataclasses import dataclass
from typing import Iterable, List

import yaml  # pip install pyyaml


@dataclass
class PluginDescriptor:
    """
    Descriptor for a plugin adapter.

    :cvar name (str): Name of the plugin.
    :cvar role (str): Role of the plugin (e.g., "capture", "watcher").
    :cvar module (str): Module name where the adapter class is located.
    :cvar clazz (str): Class name of the adapter.
    :cvar version (str): Version of the plugin.
    :cvar requires_api (str): Required API version specifier.
    :cvar capabilities (list[str]): List of capabilities provided by the plugin.
    :cvar source (str): Source of the plugin (e.g., "local").
    """

    name: str
    role: str
    module: str
    clazz: str
    version: str
    requires_api: str
    capabilities: list[str]
    source: str


def iter_local_plugin_yamls(root: str) -> Iterable[str]:
    """
    Iterate over local plugin YAML files under the given root directory.

    :param root: Root directory to search for plugins.
    :type root: str

    :return: Iterable of file paths to plugin YAML files.
    :rtype: Iterable[str]
    """
    for dirpath, _dirnames, filenames in os.walk(root):
        if "plugin.yaml" in filenames:
            yield os.path.join(dirpath, "plugin.yaml")


def load_descriptors(plugins_root: str) -> List[PluginDescriptor]:
    """
    Load plugin descriptors from local YAML files.

    :param plugins_root: Root directory to search for plugins.
    :type plugins_root: str

    :return: List of PluginDescriptor instances.
    :rtype: List[PluginDescriptor]
    """
    descriptors: List[PluginDescriptor] = []
    for yaml_path in iter_local_plugin_yamls(plugins_root):
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        descriptors.append(
            PluginDescriptor(
                name=data.get("name", ""),
                role=data.get("role", ""),
                module=data.get("module", "adapter"),
                clazz=data.get("class", "Adapter"),
                version=data.get("version", "0.0.0"),
                requires_api=data.get("requires_api", ">=1.0,<2.0"),
                capabilities=data.get("capabilities", []),
                source="local",
            )
        )
    return descriptors


def import_adapter_from_descriptor(
    descriptor: PluginDescriptor, pkg_root: str
):
    """
    Import adapter class given descriptor.
    Example: pkg_root='trivox_conductor' →
        trivox_conductor.plugins.capture_obs.adapter:OBSAdapter

    :param descriptor: Plugin descriptor.
    :type descriptor: PluginDescriptor

    :param pkg_root: Root package name for imports.
    :type pkg_root: str
    """
    mod_path = (
        f"{pkg_root}.plugins.{descriptor.name}.{descriptor.module}".replace(
            "-", "_"
        )
    )
    try:
        mod = importlib.import_module(mod_path)
        return getattr(mod, descriptor.clazz)
    except (ImportError, AttributeError) as e:
        raise ImportError(
            f"Failed to import {descriptor.clazz} from {mod_path}"
        ) from e
