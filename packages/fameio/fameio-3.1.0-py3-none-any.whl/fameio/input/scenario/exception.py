# SPDX-FileCopyrightText: 2024 German Aerospace Center <fame@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

from typing import NoReturn, Any, Union

from fameio.input import ScenarioError
from fameio.logs import log_error_and_raise, log

_DEFAULT_USED = "Using default value '{}' for missing key '{}'"


def log_and_raise(message: str) -> NoReturn:
    """Raises ScenarioError with given `message`"""
    log_error_and_raise(ScenarioError(message))


def get_or_raise(dictionary: dict, key: str, message: str) -> Union[Any, NoReturn]:
    """Returns value associated with `key` in given `dictionary`, or raises ScenarioException if key is missing"""
    if key not in dictionary or dictionary[key] is None:
        log_error_and_raise(ScenarioError(message.format(key)))
    else:
        return dictionary[key]


def assert_or_raise(assertion: bool, msg: str) -> None:
    """Raises new ScenarioError with given `msg` if `assertion` is False"""
    if not assertion:
        log_error_and_raise(ScenarioError(msg))


def get_or_default(dictionary: dict, key: str, default_value) -> Any:
    """Returns value associated with `key` in given `dictionary`, or the given `default_value` if key is missing"""
    if key in dictionary and dictionary[key] is not None:
        return dictionary[key]
    else:
        log().debug(_DEFAULT_USED.format(default_value, key))
        return default_value
