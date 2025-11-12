"""
Commands Module

This module provides the base classes and utilities for creating
command-line interface (CLI) applications. It includes the following components:

1. app: Contains the CLI application class and configuration.
2. base: Defines the base command class that all commands should inherit from.
3. exceptions: Custom exceptions for command errors.
4. registry: A registry for managing and retrieving command classes.
5. types: Defines argument types and utilities for argument parsing and validation.

## Usage:

```python
from ic_utils.ic_commands import CLIConfig, BaseCLIApp

config = CLIConfig(
    app_name="my_app",
    version="1.0.0",
    description="My CLI Application",
)

app = BaseCLIApp(config)
args = app.parse_args()
app.run_command(args)
```

This will create a CLI application with the specified configuration,
parse the command-line arguments, and execute the corresponding command.

### Adding new commands:

To add a new command, create a class that inherits from BaseCommand and implement
the execute method and define the command name and arguments.
Register the command in the CommandRegistry.

```python
from ic_utils.ic_commands.base import BaseCommand
from ic_utils.ic_commands.types import ArgumentType

class MyCommand(BaseCommand):
    name = "my_command"
    args = [
        ArgumentType("arg1", str, "Description of arg1", required=True),
        ArgumentType("arg2", int, "Description of arg2", required=False, default=0),
    ]

    def execute(self, **kwargs):
        arg1 = kwargs.get("arg1")
        arg2 = kwargs.get("arg2", 0)
        # Command logic here
        print(f"Executing my_command with arg1={arg1} and arg2={arg2}")
```

This will create a command "my_command" that can be executed from the
CLI and accessed from the registry as long as the module is imported before
running the CLI application.
"""

from .cli_app import BaseCLIApp, CLIConfig, GlobalParserBuilder
