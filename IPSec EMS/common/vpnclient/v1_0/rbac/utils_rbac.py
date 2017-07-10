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

import argparse
import re

NAME_MAX_LEN = 50


def check_name_len(name):
    """Check name length of the resource

    Args:
        name (str): name of the resource

    Returns:
        name

    Raises:
        argparse.ArgumentTypeError: if name length is longer than
            NAME_MAX_LEN
    """
    if name is not None and len(name) > NAME_MAX_LEN:
        msg = _("name length can not be greater than ") + str(NAME_MAX_LEN)
        raise argparse.ArgumentTypeError(msg)
    else:
        return name


def check_email(email):
    """Check email address is valid or not

    Args:
        email (str): email

    Returns:
        email, if email is valid
    """
    check = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
        email)

    if check is None:
        msg = _("%s is an invalid email address" % email)
        raise argparse.ArgumentTypeError(msg)
    else:
        return email
