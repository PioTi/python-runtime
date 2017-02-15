#!/usr/bin/env python3

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities for schema and command line validation"""

import argparse
import re


def get_field_value(container, field_name, field_type):
    """Fetch a field from a container with typechecking and default values.

    The field value is coerced to the desired type.  If the field is
    not present, a instance of `field_type` is constructed with no
    arguments and used as the default value.

    Args:
        container (dict): Object decoded from yaml
        field_name (str): Field that should be present in `container`
        field_type (type): Expected type for field value

    Returns:
        Any: Fetched or default value of field

    Raises:
        ValueError: if field value cannot be converted to the desired type
    """
    try:
        value = container[field_name]
        if value is None:
            return field_type()
    except (IndexError, KeyError):
        return field_type()

    msg = 'Expected "{}" field to be of type "{}", but found type "{}"'
    if not isinstance(value, field_type):
        # list('some string') is a successful type cast as far as Python
        # is concerned, but doesn't exactly produce the results we want.
        # We have a whitelist of conversions we will attempt.
        whitelist = (
            (float, str),
            (int, str),
            (str, float),
            (str, int),
            (int, float),
            )
        if (type(value), field_type) not in whitelist:
            raise ValueError(msg.format(field_name, field_type, type(value)))

    try:
        value = field_type(value)
    except ValueError as e:
        e.message = msg.format(field_name, field_type, type(value))
        raise
    return value


def validate_arg_regex(flag_value, flag_regex):
    """Check a named command line flag against a regular expression"""
    if not re.match(flag_regex, flag_value):
        raise argparse.ArgumentTypeError(
            'Value "{}" does not match pattern "{}"'.format(
                flag_value, flag_regex.pattern))
    return flag_value
