# SPDX-FileCopyrightText: 2024 German Aerospace Center <fame@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0


class InputError(Exception):
    """An error that occurred while parsing any kind of input"""

    pass


class SchemaError(InputError):
    """An error that occurred while parsing a Schema"""

    pass


class ScenarioError(InputError):
    """An error that occurred while parsing a Scenario"""

    pass


class YamlLoaderError(InputError):
    """An error that occurred while parsing a YAML file"""

    pass
