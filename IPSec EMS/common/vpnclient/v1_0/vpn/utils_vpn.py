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

from collections import OrderedDict
import ipaddress
import re

import argparse

from vpnclient.v1_0.vpn.vpn_choices import (
    IKEV1_ENCRYPTION_ALGORITHM, IKEV2_ENCRYPTION_ALGORITHM,
    IKEV1_INTEGRITY_ALGORITHM, IKEV2_INTEGRITY_ALGORITHM,
    IPSEC_IKEV1_ENCRYPTION_ALGORITHM, IPSEC_IKEV2_ENCRYPTION_ALGORITHM,
    IPSEC_IKEV1_INTEGRITY_ALGORITHM, IPSEC_IKEV2_INTEGRITY_ALGORITHM,
    DH_GROUP,
    NAME_MAX_LEN, DESCRIPTION_MAX_LEN)


def help_algorithm_options(record_type, algorithm):
    if record_type == 'ike':
        if algorithm == 'encryption':
            v1_algorithm = IKEV1_ENCRYPTION_ALGORITHM
            v2_algorithm = IKEV2_ENCRYPTION_ALGORITHM
        elif algorithm == 'integrity':
            v1_algorithm = IKEV1_INTEGRITY_ALGORITHM
            v2_algorithm = IKEV2_INTEGRITY_ALGORITHM
    if record_type == 'ipsec':
        if algorithm == 'encryption':
            v1_algorithm = IPSEC_IKEV1_ENCRYPTION_ALGORITHM
            v2_algorithm = IPSEC_IKEV2_ENCRYPTION_ALGORITHM
        elif algorithm == 'integrity':
            v1_algorithm = IPSEC_IKEV1_INTEGRITY_ALGORITHM
            v2_algorithm = IPSEC_IKEV2_INTEGRITY_ALGORITHM

    encryption_help = "\n\n" + _("Options for IKE version v1:") + "\n"
    encryption_help += _prepare_help_options(v1_algorithm)

    encryption_help += "\n\n" + _("Options for IKE version v2:") + "\n"
    encryption_help += _prepare_help_options(v2_algorithm)

    return encryption_help


def help_dh_options():
    dh_group_help = "\n\n" + _("Options:") + "\n"
    dh_group_help += _prepare_help_options(DH_GROUP)
    return dh_group_help


def _prepare_help_options(lst):
    options = ''
    options_chunk = ''
    for element in lst:
        options_chunk += element + ', '
        if len(options_chunk) > 50:
            options += element + ', ' + '\n'
            options_chunk = ''
        else:
            options += element + ', '
    if options[-1] == '\n':
        options = options[:-1]
    if options[-1] == ' ':
        options = options[:-2]
    return options


def remove_duplicates_from_list(lst):
    """Remove duplicate from a provided list

    Args:
        lst (list):

    Returns:
        lst
    """
    if lst is None:
        raise ValueError

    # Note: OrderedDict also maintains the order of the elements
    return list(OrderedDict.fromkeys(lst))


def check_cidrs(cidrs):
    """Validate cidr(s) or subnet(s)

    Args:
        cidrs (list): Subnet(s) in CIDR format

    Returns:
        cidrs (list)

    Raises:
        argparse.ArgumentTypeError: If CIDR's list is empty(None), invalid CIDR
        format or inconsistent versions of CIDR in the list
    """
    if (cidrs is None) or (not cidrs):
        msg = _("CIDRs list is empty")
        raise argparse.ArgumentTypeError(msg)

    # Inconsistent versions of CIDR in the list
    cidr_type_list = []
    for cidr in cidrs:
        try:
            cidr_type = type(ipaddress.ip_network((unicode(cidr, "utf-8"))))
        except:
            msg = "{0} is not a valid CIDR format".format(cidr)
            raise argparse.ArgumentTypeError(msg)

        cidr_type_list.append(cidr_type)

    # Inconsistent versions of CIDR in the list
    check_v4 = all(isinstance(x, ipaddress.IPv4Network) for x in cidr_type_list)

    check_v6 = all(isinstance(x, ipaddress.IPv6Network) for x in cidr_type_list)

    if check_v4 and check_v6:
        raise argparse.ArgumentTypeError(_("All the CIDRs must be of either "
                                           "IPv4 or IPv6 format"))


def check_cidr(cidr):
    """Validate cidr or subnet

    Args:
        cidr (string): Subnet in CIDR format

    Returns:
        cidr (string)

    Raises:
        argparse.ArgumentTypeError: If CIDR is invalid
    """
    if (cidr is None) or (not cidr and not cidr.isspace()):
        msg = "CIDR {0} is empty".format(cidr)
        raise argparse.ArgumentTypeError(msg)

    msg_subpart = _(" is not a valid CIDR format")
    try:
        cidr_type = type(ipaddress.ip_network((unicode(cidr, "utf-8"))))
    except ValueError:
        raise argparse.ArgumentTypeError(cidr + msg_subpart)

    if cidr_type not in (ipaddress.IPv4Network, ipaddress.IPv6Network):
        raise argparse.ArgumentTypeError(cidr + msg_subpart)

    return cidr


def check_ipaddress_or_fqdn(value):
    """Validate if value is valid IPv4/IPv6 or valid hostname

    Args:
        value (str): ipaddress or fqdn

    Returns:
        If valid return value

    Raises:
        argparse.ArgumentTypeError: If invalid IPv4/IPv6 or fqdn format
    """
    try:
        ipaddress.ip_address((unicode(value, "utf-8")))
    except ValueError:
        if not _is_valid_host(value):
            msg = "{0} is not a valid IP Address format".format(ipaddress)
            raise argparse.ArgumentTypeError(msg)
    return value


def _is_valid_host(hostname):
    """Validate DNS(FQDN or domain or hostname)

    Args:
        hostname (str): FQDN or domain or hostname

    Returns:
        True : if hostname is valid
        False : if hostname is invalid
    """
    is_valid = re.match("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*"
                        "([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$",
                        hostname)
    return is_valid


def check_lifetime_value(lifetime_value):
    """Validate lifetime value
    Args:
        lifetime_value (str): lifetime value

    Returns:
        int conversion of lifetime value
    """
    if lifetime_value:
        if lifetime_value < 0:
            msg = _("lifetime value is not a positive integer")
            raise argparse.ArgumentTypeError(msg)
        return lifetime_value
    else:
        return lifetime_value


def check_name_len(name):
    """Check name length of the resource

    Args:
        name (str): name of the resource

    Returns:
        name

    Raises:
        argparse.ArgumentTypeError: if name length is longer than
            DESCRIPTION_MAX_LEN
    """
    length = NAME_MAX_LEN
    if name is not None and len(name) > length:
        msg = _("name length can not be greater than %s") + str(length)
        raise argparse.ArgumentTypeError(msg)
    else:
        return name


def check_description_len(description):
    """Check description length of the resource

    Args:
        description (str): description of the resource

    Returns:
        description

    Raises:
        argparse.ArgumentTypeError: if description length is longer
            than DESCRIPTION_MAX_LEN
    """
    length = DESCRIPTION_MAX_LEN
    if description is not None and len(description) > length:
        msg = _("description length can not be greater than ") + str(length)
        raise argparse.ArgumentTypeError(msg)
    else:
        return description


class DefaultList(list):
    """For argparse 'append' action, remove the default value if any value
    has been provided for the argument"""
    def __copy__(self):
        return []