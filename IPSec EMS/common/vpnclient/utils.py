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

from __future__ import print_function
import argparse
import re
import sys
import os

import netaddr as netaddr
import ipaddress

MAX_URI_LEN = 8192


def _cmd_help(text):
    return text + os.linesep + os.linesep

FH = _cmd_help


def env(var, default=None):
    """Returns the environment variable set.
    If value is non-empty, defaults to '' or default value set.

    Args:
        var (str): environment variable name
        default (str): 'default' value for environment variable

    Returns:
        environment variable value or passed 'default' value
    """
    value = os.environ.get(var, None)
    if value:
        return value
    return default if default else ''


def check_ipaddress_or_fqdn(value):
    """Validate if value is valid IPv4/IPv6 or valid hostname

    Args:
        value (str): ipaddress or fqdn

    Returns:
        If valid return value

    Raises:
        argparse.ArgumentTypeError: Invalid IPv4/IPv6 and fqdn format
    """
    try:
        ipaddress.ip_address((unicode(ipaddress, "utf-8")))
    except ValueError:
        if not is_valid_host(ipaddress):
            msg = "{0} is not a valid IP Address format".format(ipaddress)
            raise argparse.ArgumentTypeError(msg)
    return value


def check_http_timeout(http_timeout):
    """Validate HTTP timeout value
    Args:
        http_timeout (str): HTTP request timeout

    Returns:
        int conversion of http_timeout
    """
    if http_timeout:
        if not is_positive_float(http_timeout):
            msg = _('http-timeout is not a positive value')
            raise argparse.ArgumentTypeError(msg)
        return http_timeout
    else:
        return http_timeout


def check_key(key):
    """Validate certificate private key file
    Args:
        key (str): private key file path

    Returns:
        original key path
    """
    if key:
        if not os.path.exists(key):
            msg = _('key is a not a valid file')
            raise argparse.ArgumentTypeError(msg)
    return key


def check_cert(cert):
    """Validate HTTPS certificate

    Args:
        cert (str): certificate path

    Returns:
        original certificate path
    """
    check_if_empty(cert, 'cert')
    if not os.path.exists(cert):
        msg = _('cert is a not a valid file')
        raise argparse.ArgumentTypeError(msg)
    return cert


def check_fqdn(fqdn):
    """Check if EMS URL is valid

    Args:
        fqdn (str): FQDN or IP address of EMS

    Returns:
        None
    """
    check_if_empty(fqdn, 'fqdn')
    if not is_valid_ipaddress(fqdn):
        msg = _('ipsec-ems-fqdn is a not a valid URL')
        raise argparse.ArgumentTypeError(msg)
    return fqdn


def check_namespace(namespace):
    """Namespace(or Domain) check

    Args:
        namespace (str): namespace or domain of EMS

    Returns:
        None
    """
    check_if_empty(namespace, 'namespace')
    return namespace


def check_auth_strategy(auth_strategy):
    """Validate authentication strategy

    Args:
        auth_strategy (str):

    Returns:
        None
    """
    check_if_empty(auth_strategy, 'auth_strategy')
    return auth_strategy


def check_if_empty(var, usage_pattern):
    """Check if argument is falsy or just blank (i.e. '    ')

    Args:
        var (An argparse parser): argparse parser with attribute's value
        usage_pattern (str): Argument display name

    Returns:
        None
    """
    if (var is None) or (not var and not var.isspace()):
        print_usage(usage_pattern)


def print_usage(usage_pattern):
    """Print usage message for the argument to stdout and exit

    Args:
        usage_pattern (str): Argument display name

    Returns:
        None
    """
    # Replace '-' with '_' for displaying Environment variable name
    env_pattern = usage_pattern.replace('-', '_')

    # Special handling for 'fqdn'
    if usage_pattern == 'fqdn':
        usage_pattern = 'ipsec-ems-fqdn'

    print("You must provide {0} via either --{1} or Env: IPSEC_EMS_{2}".
          format(usage_pattern,
                 usage_pattern,
                 env_pattern.decode('utf-8').upper(), file=sys.stdout))
    sys.exit(0)


# def check_uri_length(self, action):
#     """
#
#     Args:
#         self:
#         action:
#
#     Returns:
#
#     """
#         uri_len = len(url)
#         if uri_len > MAX_URI_LEN:
#             raise exceptions.RequestURITooLong(
#                 excess=uri_len - MAX_URI_LEN)

def str_to_class(str):
    return getattr(sys.modules[__name__], str)


def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def str2dict(strdict):
    """Convert key1=value1,key2=value2,... string into dictionary.
    :param strdict: key1=value1,key2=value2
    """
    result = {}
    if strdict:
        for kv in strdict.split(','):
            key, sep, value = kv.partition('=')
            if not sep:
                msg = "invalid key-value '%s', expected format: key=value"
                raise argparse.ArgumentTypeError(msg % kv)
            result[key] = value
    return result


def prepare_body(argparser, attr_list):
    body = {attr: argparser.get(attr) for attr in attr_list
            if argparser.get(attr)}
    return body


def find_subcommand_action(sub_command):
    """Find the commands resource and action to be performed

    Args:
        sub_command (str) : sub_command name

    Returns:
        URI Resource and HTTP Method
    """
    split = sub_command.split('-')
    return split[2]


def is_positive_float(s):
    """Check if str represents a positive float

    Args:
        s (str): string to be checked

    Returns:
        True : if 's' represents positive float
        False : is 's' does not represent positive float
    """
    try:
        float(s)
        if s >= 0:
            return True
        else:
            return False
    except ValueError:
        return False


def is_valid_cidr(cidr):
    """Check if cidr is a valid subnet(cidr)

    Args:
        cidr (str): cidr or subnet address

    Returns:
        True : if cidr is valid
        False : if cider is an invalid subnet
    """
    try:
        netaddr.IPNetwork(cidr)
        return True
    except netaddr.AddrFormatError:
        return False


def is_valid_ipaddress(ip):
    """Validate IP Address

    Args:
        ip (str): IP Address

    Returns:
        True : if ip is valid
        False : if ip is invalid
    """
    is_valid = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)"
                        "{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",
                        ip)
    return is_valid


def is_valid_host(hostname):
    """Validate DNS(or domain or hostname)

    Args:
        hostname (str): domain or hostname

    Returns:
        True : if hostname is valid
        False : if hostname is invalid
    """
    is_valid = re.match("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*"
                        "([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$",
                        hostname)
    return is_valid


