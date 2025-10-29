from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List
import importlib
import os
import yaml  # pip install pyyaml

@dataclass
class PluginDescriptor:
    name: str
    role: str
    module: str
    clazz: str
    version: str
    requires_api: str
    capabilities: list[str]
    source: str  # "local"

def iter_local_plugin_yamls(root: str) -> Iterable[str]:
    for dirpath, _dirnames, filenames in os.walk(root):
        if "plugin.yaml" in filenames:
            yield os.path.join(dirpath, "plugin.yaml")

def load_descriptors(plugins_root: str) -> List[PluginDescriptor]:
    descs: List[PluginDescriptor] = []
    for yaml_path in iter_local_plugin_yamls(plugins_root):
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        descs.append(PluginDescriptor(
            name=data.get("name", ""),
            role=data.get("role", ""),
            module=data.get("module", "adapter"),
            clazz=data.get("class", "Adapter"),
            version=data.get("version", "0.0.0"),
            requires_api=data.get("requires_api", ">=1.0,<2.0"),
            capabilities=data.get("capabilities", []),
            source="local",
        ))
    return descs

def import_adapter_from_descriptor(desc: PluginDescriptor, pkg_root: str):
    """
    Import adapter class given descriptor.
    Example: pkg_root='trivox_conductor' →
      trivox_conductor.plugins.capture_obs.adapter:OBSAdapter
    """
    mod_path = f"{pkg_root}.plugins.{desc.name}.{desc.module}".replace("-", "_")
    mod = importlib.import_module(mod_path)
    return getattr(mod, desc.clazz)
