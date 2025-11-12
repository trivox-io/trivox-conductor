from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleLoaderInfo:
    modules_package: str
    required_files: tuple[str, ...]


@dataclass(frozen=True)
class PluginLoaderInfo:
    plugins_package_root: str  # e.g. "trivox_conductor.plugins"
    plugins_dir_name: str  # folder inside the app if you need FS access


@dataclass(frozen=True)
class ObserverLoaderInfo:
    packages: tuple[str, ...]  # packages to scan
    module_name_suffixes: tuple[str]  # e.g. ("_observer",)


@dataclass(frozen=True)
class LoaderConstants:
    modules = ModuleLoaderInfo(
        modules_package="trivox_conductor.modules",
        required_files=(
            "commands.py",
            "settings.py",
            "strategies.py",
            "ui.py",
        ),
    )
    plugins = PluginLoaderInfo(
        plugins_package_root="trivox_conductor.plugins",
        plugins_dir_name="plugins",
    )
    observers = ObserverLoaderInfo(
        packages=(
            "trivox_conductor.core.manifests",
            "trivox_conductor.core.observers",
        ),
        module_name_suffixes=("_observer",),
    )
