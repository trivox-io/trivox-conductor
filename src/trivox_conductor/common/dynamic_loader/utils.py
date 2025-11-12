from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Iterator


def iter_subpackages(package_name: str) -> Iterator[tuple[str, Path]]:
    """Yield (full_module_name, filesystem_path) for each subpackage."""
    pkg = importlib.import_module(package_name)
    base_path = Path(pkg.__path__[0])
    for _finder, mod_name, is_pkg in pkgutil.iter_modules(pkg.__path__):
        if not is_pkg:
            continue
        full_name = f"{pkg.__name__}.{mod_name}"
        yield full_name, base_path / mod_name


def has_any_files(dir_path: Path, filenames: tuple[str, ...]) -> bool:
    return any((dir_path / f).is_file() for f in filenames)
