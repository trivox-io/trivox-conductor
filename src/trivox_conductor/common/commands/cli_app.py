"""
Command line interface for the IC Inspector tool.
"""

import argparse
import os
import sys
from dataclasses import dataclass
from typing import List, Optional, Type

from .base_command import BaseCommand
from .exceptions import CommandException
from .registry import CommandRegistry
from .argument_type import coerce_type


@dataclass
class CLIConfig:
    """
    Configuration for the CLI application.
    """

    app_name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    usage: Optional[str] = None
    formatter_class: Optional[Type[argparse.HelpFormatter]] = (
        argparse.RawDescriptionHelpFormatter
    )


class BaseCLIApp:
    """
    Command line interface for the IC Inspector tool.

    - Create the main parser for the CLI application.
    - Add subparsers to the main parser to handle multiple commands.
    - Add custom commands to the parser.
    """

    def __init__(self, config: CLIConfig):
        """
        :param gui_callback: The callback function to run the GUI application.
        :type gui_callback: Optional[callable]
        """

        self.config = config

        self.parser = self._create_main_parser()
        self.subparsers = self._add_subparsers(self.parser)
        self._add_custom_commands(self.subparsers)

    def _create_main_parser(self) -> argparse.ArgumentParser:
        """
        Create the main parser for the CLI application.

        :return: The main parser for the CLI application.
        :rtype: argparse.ArgumentParser
        """
        p = argparse.ArgumentParser(
            prog=self.config.app_name,
            description=self.config.description,
            usage=self.config.usage,
            formatter_class=self.config.formatter_class,
        )
        if self.config.version:
            p.add_argument(
                "--version", action="version", version=self.config.version
            )
        p.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="Increase verbosity (-v, -vv)",
        )
        return p

    def _add_subparsers(
        self, parser: argparse.ArgumentParser
    ) -> argparse._SubParsersAction:
        """
        Add subparsers to the main parser to handle multiple commands.

        :param parser: The main parser for the CLI application.
        :type parser: argparse.ArgumentParser

        :return: The subparsers for the main parser.
        :rtype: argparse._SubParsersAction
        """
        return parser.add_subparsers(dest="command", help="Available commands")

    def _add_custom_commands(self, subparsers: argparse._SubParsersAction):
        """
        Add custom commands to the parser.

        :param subparsers: The subparsers for the main parser.
        :type subparsers: argparse._SubParsersAction
        """
        for command_name in CommandRegistry.names():
            command_cls = CommandRegistry.get(command_name)
            doc = (command_cls.__doc__ or "").strip()
            summary = command_cls.summary or (
                doc.splitlines()[0] if doc else None
            )
            command_parser = subparsers.add_parser(
                command_cls.name,
                help=summary,
                description=doc or summary,
                epilog=command_cls.epilog,
                aliases=getattr(command_cls, "aliases", ()),
                formatter_class=argparse.RawDescriptionHelpFormatter,
            )
            self.define_command_arguments(command_parser, command_cls)

    def define_command_arguments(
        self, command_parser: argparse.ArgumentParser, command_cls: BaseCommand
    ):
        """
        Define arguments for a command.

        :param command_parser: The parser for the command.
        :type command_parser: argparse.ArgumentParser

        :param command_cls: The class for the command.
        :type command_cls: BaseCommand
        """
        for arg in command_cls.define_arguments():
            if arg.data_type is bool and arg.required:
                raise ValueError(
                    f"Boolean flag --{arg.name} cannot be required"
                )
            default = arg.default
            if arg.env and default is None:
                default = os.getenv(arg.env)

            kwargs = {
                "help": arg.help_text,
                "required": arg.required,
                "default": default,
            }
            if arg.choices:
                kwargs["choices"] = arg.choices
            if arg.nargs is not None:
                kwargs["nargs"] = arg.nargs
            if arg.metavar:
                kwargs["metavar"] = arg.metavar

            ty = coerce_type(arg.data_type)
            if ty is bool:
                kwargs["action"] = "store_true"
            else:
                kwargs["type"] = ty

            command_parser.add_argument(f"--{arg.name}", **kwargs)

    def parse_args(
        self, argv: Optional[List[str]] = None
    ) -> argparse.Namespace:
        """
        Parse the command line arguments and return the parser and the parsed arguments.

        :return: The parser and the parsed arguments.
        :rtype: Tuple[argparse.ArgumentParser, argparse.Namespace]
        """
        return self.parser.parse_args(argv)

    def run(self, argv: Optional[List[str]] = None) -> int:
        """
        Run the CLI application.

        :param argv: The command line arguments to parse. If None, uses sys.argv.
        :type argv: Optional[List[str]]

        :return: The exit code of the application.
        :rtype: int
        """
        args = self.parse_args(argv)
        return self.run_command(args) or 0

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

        command_cls = CommandRegistry.get(args.command)
        if not command_cls:
            self.parser.print_help()
            return 1

        command_instance: BaseCommand = command_cls()
        cmd_args = vars(args).copy()
        cmd_args.pop("command", None)
        try:
            command_instance.validate(**cmd_args)
            return command_instance.execute(**cmd_args) or 0
        except CommandException as e:
            print(f"Error: {e}", file=sys.stderr)
            return e.exit_code
