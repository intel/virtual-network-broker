#    Copyright (c) 2016 Intel Corporation.
#    All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Common util functions
"""

import ast
import json
import uuid


def generate_uuid():
    """ Generate a random UUID

        Version 4(v4) uuid
    """
    # Make a UUID and convert to a string of hex digits
    return str(uuid.uuid4())


def is_valid_uuid(uuid_to_test, version=4):
    """Check if uuid_to_test is a valid UUID.

    Note : version is defaulted to 4

    Args:
        uuid_to_test (str): uuid value in string format
        version (int): version no. of uuid {1, 2, 3, 4}

    Returns:
        `True` if uuid_to_test is a valid UUID, otherwise `False`.
    """
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def str_to_dict(value):
    """Converts a string expression to dict

    Args:
        value (str) :

    Returns:
        dict
    """
    return ast.literal_eval(value)


def unicode_to_ascii_dict(value):
    """Converts a unicode expression to ascii dict

    Args:
        value (str) :

    Returns:
        dict
    """
    return str_to_dict(json.dumps(value))


def get_sk_from_path(request):
    """extract secondary key from path

    Args:
       request : request context

    Returns:
        secondary key
    """
    return request._request.get_full_path().decode('unicode-escape').encode(
        'utf8').rsplit('/')[4]


def get_resource_from_path(request):
    """extract resource name from path

    Args:
       request : request context

    Returns:
        resource name
    """
    return request._request.get_full_path().decode('unicode-escape').encode(
        'utf8').rsplit('/')[3]
