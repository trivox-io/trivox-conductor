from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Iterable, Iterator

import trivox_conductor.constants as trivox_constants
from trivox_conductor.common.dynamic_loader import (
    BaseLoader,
    Candidate,
    LoaderContext,
)
from trivox_conductor.common.dynamic_loader.utils import (
    has_any_files,
    iter_subpackages,
)
from trivox_conductor.common.logger import logger
from trivox_conductor.common.registry.endpoint_registry import EndpointRegistry
from trivox_conductor.core.registry import ROLE_REGISTRIES
from trivox_conductor.core.registry.base_loader import (
    import_adapter_from_descriptor,
    load_descriptors,
)


class ModulesLoader(BaseLoader):
    NAME = "modules"

    def __init__(self) -> None:
        # Just a handle into AppConstants, so later you can move this class
        self._cfg = (
            trivox_constants.MODULES_LOADER
        )  # e.g. modules_package, required_files

    def discover(self, ctx: LoaderContext) -> Iterable[Candidate]:
        for mod_name, mod_path in iter_subpackages(self._cfg.modules_package):
            yield Candidate(name=mod_name, path=mod_path)

    def condition(self, cand: Candidate) -> bool:
        return (
            has_any_files(cand.path, self._cfg.required_files)
            if cand.path
            else False
        )

    def on_load(self, cand: Candidate, ctx: LoaderContext) -> None:
        importlib.import_module(cand.name)
        logger.debug("modules: imported %s", cand.name)


class PluginsLoader(BaseLoader):
    NAME = "plugins"

    def __init__(self) -> None:
        self._cfg = trivox_constants.PLUGINS_LOADER

    def discover(self, ctx: LoaderContext) -> Iterable[Candidate]:
        # Single candidate: the plugins root package
        pkg = importlib.import_module(self._cfg.plugins_package_root)
        root = Path(pkg.__path__[0])
        yield Candidate(name=self._cfg.plugins_package_root, path=root)

    def on_load(self, cand: Candidate, ctx: LoaderContext) -> None:
        # Clear previous role registries (same behavior as before)
        for reg in ROLE_REGISTRIES.values():
            logger.debug(f"Clearing registry for role: {reg}")
            reg.clear()

        descriptors = load_descriptors(str(cand.path))
        logger.debug("plugins: descriptors loaded: %s", descriptors)

        for d in descriptors:
            clazz = import_adapter_from_descriptor(
                d, pkg_root="trivox_conductor"
            )
            name = clazz.__name__.lower()
            reg: EndpointRegistry = ROLE_REGISTRIES.get(d.role)
            if not reg:
                logger.warning("plugins: unknown role '%s' for %s", d.role, d)
                continue
            reg.register(name, clazz)

        logger.debug("plugins: registered %d adapter(s)", len(descriptors))


class ObserversLoader(BaseLoader):
    NAME = "observers"

    def __init__(self) -> None:
        self._cfg = trivox_constants.OBSERVERS_LOADER
        # expects .packages: list[str], .module_name_suffixes: tuple[str, ...]

    def _iter_modules(self, package_name: str) -> Iterator[tuple[str, Path]]:
        pkg = importlib.import_module(package_name)
        base = Path(pkg.__path__[0])
        for _finder, name, is_pkg in pkgutil.iter_modules(pkg.__path__):
            # we want modules, not subpackages, but you can tweak this
            full = f"{pkg.__name__}.{name}"
            yield full, base / name

    def discover(self, ctx: LoaderContext) -> Iterable[Candidate]:
        for pkg_name in self._cfg.packages:
            for mod_name, mod_path in self._iter_modules(pkg_name):
                yield Candidate(name=mod_name, path=mod_path)

    def condition(self, cand: Candidate) -> bool:
        return any(
            cand.name.endswith(sfx) for sfx in self._cfg.module_name_suffixes
        )

    def on_load(self, cand: Candidate, ctx: LoaderContext) -> None:
        importlib.import_module(cand.name)
        logger.debug("observers: imported %s", cand.name)
