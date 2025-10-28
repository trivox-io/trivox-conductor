"""
trivox_conductor/
|-- __init__.py
|-- cli.py # Application entry point
|-- app.py # Application initialization (cofigures logging, populate settings, registries, etc.)
|-- common/ # Share core functionality across modules
|   |-- __init__.py
|   |-- base_command.py # Application command base class (All commands in module inherit from this)
|   |-- logger.py # Instance of the application logger
|   |-- commands/ # Command implementations and related classes (Future standalone module)
|       |-- __init__.py
|       |-- argument_type.py # Command argument type definition
|       |-- base_command_processor.py # Base class for command processors
|       |-- base_command.py # Base class for commands
|       |-- cli_app.py # CLI application class (Load commands from registry and setup argparse)
|       |-- exceptions.py # Command-related exceptions
|       |-- registry.py # Command registry to manage available commands (Uses EndpointRegistry)
|   |-- logging/ # Logging configuration and utilities
|       |-- __init__.py
|       |-- configuration_validation.py # Logging configuration validation utilities
|       |-- log_subscriber.py # Allow subscribing to log events
|       |-- logger_utils.py # Logging utility functions
|       |-- filters/ # Logging filters
|           |-- __init__.py
|           |-- ensure_classname.py # Ensure log messages include the class name
|       |-- formatters/ # Logging formatters
|           |-- __init__.py
|           |-- console_color_formatter.py # Console formatter with color support
|           |-- html_formatter.py # HTML formatter for log messages (Used in GUI)
|       |-- handlers/ # Logging handlers
|           |-- __init__.py
|           |-- console_stream.py # Console stream handler
|           |-- qtext_edit_logger.py # QT text edit handler for GUI logging
|           |-- socket_handler.py # Socket handler for remote logging
|       |-- specs/ # Logging specification classes
|           |-- __init__.py
|           |-- formatter_spec.py # Specification for log message formatters
|           |-- handler_spec.py # Specifications for log handlers
|           |-- logger_spec.py # Specifications for loggers
|           |-- logging_spec.py # Overall logging configuration specification
|           |-- root_spec.py # Root logger specification
|           |-- spec_manager.py # Manages loading and validating logging specifications
|   |-- registry/ # General endpoint registry for managing plugins and extensions
|       |-- __init__.py
|       |-- endpoint_registry.py # Generic endpoint registry implementation
|   |-- settings/
|       |-- __init__.py
|       |-- base_settings.py # Base class for application settings (All settings in modules inherit from this)
|       |-- setting_manager.py # Manages application settings (load, save, validate, etc.)
|       |-- setting_merger.py # Merges multiple settings sources
|       |-- setting_registry.py # Registry for available settings classes
|       |-- settings.py # Application settings implementation
|-- ui/
|   |-- __init__.py
|   |-- app.py # Application main class (Initializes and runs the GUI)
|   |-- common/ # Shared GUI functionality
|       |-- __init__.py
|       |-- base_window_controller.py # Base class for window controllers
|       |-- base_window_view.py # Base class for window views
|       |-- controllers_mediator.py # Mediator for coordinating between controllers
|   |-- controllers/ # GUI controllers
|       |-- __init__.py
|       |-- main_window_controller.py # Main window controller
|   |-- handlers/ # GUI event handlers (Handle events that communicate with modules)
|       |-- __init__.py
|   |-- qt/ # QT related utilities and classes
|       |-- __init__.py
|       |-- compile.bat # Batch file to compile .ui files to .py
|       |-- compiled/ # Compiled .ui files to .py
|       |   |-- __init__.py
|       |   |-- main_window.py # Compiled main window UI
|       |-- source/ # Source .ui files
|           |-- main_window.ui # QT Designer main window UI file
|   |-- views/ # GUI views
|       |-- __init__.py
|       |-- main_window_view.py # Main window view implementation
"""
from trivox_conductor.cli import main


if __name__ == "__main__":
    main()