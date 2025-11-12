"""
CLI application for Trivox Conductor.
"""

from __future__ import annotations

import argparse
import sys
from typing import Callable, Optional

import trivox_conductor.constants as trivox_constants
from trivox_conductor.app import initialize
from trivox_conductor.common.commands import (
    BaseCLIApp,
    CLIConfig,
    GlobalParserBuilder,
)
from trivox_conductor.ui import run_gui


class TrivoxCLI(BaseCLIApp):
    """
    CLI application for Trivox Conductor.
    """

    def __init__(
        self,
        config: CLIConfig,
        gui_callback: Optional[Callable[[], None]] = None,
    ):
        """
        :param gui_callback: The callback function to run the GUI application.
        :type gui_callback: Optional[Callable[[], None]]
        """
        self.gui_callback = gui_callback

        super().__init__(config)
        self.build_commands()
        self._add_run_command(self.subparsers)

    def _add_run_command(self, subparsers: argparse._SubParsersAction):
        subparsers.add_parser(
            "run",
            help="Run the Trivox Conductor GUI application.",
            description="Launch the Trivox Conductor GUI application.",
        )

    def run_command(self, args: argparse.Namespace):
        """
        Run the command based on the parsed arguments.

        :param args: The parsed arguments.
        :type args: argparse.Namespace

        :param run_callback: The callback function to run the command.
        :type run_callback: callable
        """
        if not getattr(args, "command", None):
            self.parser.print_help()
            return 1

        if args.command == "run":
            if not self.gui_callback:
                print(
                    "Error: GUI callback is not configured.", file=sys.stderr
                )
                return 2
            kw = vars(args).copy()
            kw.pop("command", None)
            # Let GUI callback raise; map to exit code 1 on failure
            try:
                self.gui_callback(**kw)
                return 0
            # Justification: Broad exception caught to handle any error from the GUI launch
            # pylint: disable=broad-exception-caught
            except Exception as e:
                print(f"Error launching GUI: {e}", file=sys.stderr)
                return 1
            # pylint: enable=broad-exception-caught

        # For all other commands, defer to base logic (registry-driven)
        return super().run_command(args)


def main(argv: Optional[list[str]] = None):
    """
    Main entry point for the CLI application.

    - Load all modules to register commands, settings, and strategies.
    - Populate settings and setup the logger.
    - Parse the command line arguments.
    - Run the specified command.
    """
    if argv is None:
        argv = sys.argv[1:]

    global_parser = GlobalParserBuilder.build_global_parser(
        trivox_constants.APP.version
    )
    global_args, remaining_argv = global_parser.parse_known_args(argv)

    # Load all modules to register commands, settings, and strategies.
    initialize(global_args.verbose)

    # Parse the command line arguments
    cli_app = TrivoxCLI(
        config=CLIConfig(
            app_name=trivox_constants.CLI.executable_name,
            description=trivox_constants.CLI.description,
            usage=trivox_constants.CLI.usage,
        ),
        gui_callback=run_gui,
    )
    args = cli_app.parse_args(remaining_argv)
    exit_code = cli_app.run_command(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
