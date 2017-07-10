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

"""Util functions related to IPsecEnforcer"""

import ast
import random
import string


def generate_psk_string():
    """Generate a Pre-Shared Key(PSK) or Secret string

    PSK is used for VPN Tunnel Authentication.
    PSK is a combination of ASCII letters(small and caps) and digits.
    PSK is 16 characters long.

    Returns:
        str: Random PSK
    """
    psk_length = 16
    return ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for _ in range(psk_length))


def str_to_dict(value):
    """Converts a string expression to dict

    Args:
        value (str): string expression of dict

    Returns:
        dict
    """
    return ast.literal_eval(value)


def consul_key_join(*args):
    """Prepare consul key(partial or complete) with consul
    delimiter('/')

    Args:
        args (tuple): consul key elements

    Returns:
        str: consul key with consul delimiter
    """

    return "/".join(args)