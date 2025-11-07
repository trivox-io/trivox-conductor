"""
Types module for command arguments.
"""

# Justification: Disable pylint for too many instance attributes in ArgumentType
# because it is a data class and having multiple attributes is acceptable.
# pylint: disable=too-many-instance-attributes

import argparse
import json
from dataclasses import dataclass
from typing import List, Optional, Type, Union

JSON = object()


@dataclass
class ArgumentType:
    """
    Represents an argument for a command.

    :cvar name (str): The name of the argument.
    :cvar data_type (Type[Union[str, int, float, bool]]): The data type of the argument.
    :cvar help_text (str): The help text for the argument.
    :cvar required (bool): Whether the argument is required.
    :cvar default (Optional[Union[str, int, float, bool]]): The default value for the argument.
    :cvar choices (Optional[List[str]]): The choices for the argument.
    :cvar nargs (Optional[Union[int, str]]): The number of arguments.
    :cvar metavar (Optional[str]): The metavar for the argument.
    :cvar env (Optional[str]): The environment variable associated with the argument.
    """

    name: str
    data_type: Type[Union[str, int, float, bool]]
    help_text: str
    required: bool = False
    default: Optional[Union[str, int, float, bool]] = None
    choices: Optional[List[str]] = None
    nargs: Optional[Union[int, str]] = None
    metavar: Optional[str] = None
    env: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert the argument to a dictionary.

        :return: The argument as a dictionary.
        :rtype: dict
        """

        return dict(self.__dict__)


def coerce_type(t: Type[Union[str, int, float, bool]]) -> callable:
    """
    Coerce a type to a callable that converts a string to that type.

    :param t: The type to coerce.
    :type t: Type[Union[str, int, float, bool]]

    :return: A callable that converts a string to the specified type.
    :rtype: callable
    """

    def _coerce_json(s):
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            raise argparse.ArgumentTypeError(f"Invalid JSON: {e}")

    if t is JSON:
        return _coerce_json
    return t
