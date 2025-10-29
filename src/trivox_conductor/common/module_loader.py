
import importlib
import os
import pkgutil
from typing import List, Optional


def load_specific_modules(package: object, required_files: List[str]):
    """
    Load all modules from the given package that contain any of the required files.

    :param package: Package to load modules from
    :type package: object (e.g., a module or package)

    :param required_files: List of files that the module must contain
    :type required_files: List[str]
    """

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package.__name__}.{module_name}"
        module_path = os.path.join(package.__path__[0], module_name)

        if os.path.isdir(module_path):
            # Check if required files exist in the module's directory
            if any(
                os.path.isfile(os.path.join(module_path, file))
                for file in required_files
            ):
                # Import the module if it contains any of the required files
                importlib.import_module(full_module_name)


def try_import(module_name: str) -> Optional[object]:
    """
    Try to import a module and return it if successful.

    :param module_name: Name of the module to import
    :type module_name: str

    :return: The imported module or None if the import failed
    :rtype: Optional[object]
    """

    try:
        module = __import__(module_name, fromlist=[""])
        return module
    except ImportError as e:
        print(f"Failed to import {module_name}: {e}")
        return None


def load_all_modules():
    """
    Load all the modules required by the system.
    - commands.py will add all the commands to the CLI
    - strategies.py will add all the strategies to the system and \
        make them available for the GUI
    - settings.py will add all the settings to the system and make \
        them available in the application
    """

    # Define required files for dynamic loading
    required_files = ["commands.py", "strategies.py", "settings.py"]

    # List of module names to import
    module_names = [
        "trivox_conductor.modules",
    ]

    # Import and load relevant modules dynamically with try-catch
    for module_name in module_names:
        module = try_import(module_name)
        if module:
            load_specific_modules(module, required_files)
