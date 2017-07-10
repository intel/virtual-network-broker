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

import pdb
from collections import OrderedDict
#import ipaddress
import re

import argparse

from secmonclient.v1_0.vpn.vpn_choices import (
    IKEV1_ENCRYPTION_ALGORITHM, IKEV2_ENCRYPTION_ALGORITHM,
    IKEV1_INTEGRITY_ALGORITHM, IKEV2_INTEGRITY_ALGORITHM,
    IPSEC_IKEV1_ENCRYPTION_ALGORITHM, IPSEC_IKEV2_ENCRYPTION_ALGORITHM,
    IPSEC_IKEV1_INTEGRITY_ALGORITHM, IPSEC_IKEV2_INTEGRITY_ALGORITHM,
    DH_GROUP
)
from secmonclient.v1_0.vpn.command_column import (FIELD_MAPPING,
                REVERSE_FIELD_MAPPING)

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
#    pdb.set_trace()
    if (cidrs is None) or (not cidrs):
        msg = _("CIDRs list is empty")
        raise argparse.ValidationError(msg)

    # Inconsistent versions of CIDR in the list
    cidr_type_list = []
    for cidr in cidrs:
        cidr_type = type(ipaddress.ip_network((unicode(cidr, "utf-8"))))
        cidr_type_list.append(cidr_type)

    check = all(isinstance(x, type(ipaddress.IPv4Network)) for x in
                cidr_type_list)
    if not check:
        raise argparse.ValidationError(_("All the CIDRs must be of either IPv4 "
                                         "or IPv6 format"))


def check_cidr(cidr):
    """Validate cidr or subnet

    Args:
        cidr (string): Subnet in CIDR format

    Returns:
        cidr (string)

    """
    if (cidr is None) or (not cidr and not cidr.isspace()):
        msg = "CIDR {0} is empty".format(cidr)
        raise argparse.ArgumentTypeError(msg)

    cidr_type = type(ipaddress.ip_network((unicode(cidr, "utf-8"))))

    if cidr_type not in (ipaddress.IPv4Network,
                         ipaddress.IPv6Network):
        msg = "{0} is not a valid CIDR format".format(cidr)
        raise argparse.ArgumentTypeError(msg)

    return cidr


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
        if not _is_valid_host(ipaddress):
            msg = "{0} is not a valid IP Address format".format(ipaddress)
            raise argparse.ArgumentTypeError(msg)
    return value

def string_to_integer_field_mapping(result_dict):
#    pdb.set_trace()
    for result in result_dict:
        if result in FIELD_MAPPING:                       
            result_value = FIELD_MAPPING[result]
            var = result_dict[result]
            var1= str(var)
            field_value = result_value[var1]
            result_dict[result] = field_value
#        elif result in ACTION_MAPPING:
#            result_value = ACTION_MAPPING[result]
#            var1 = result_dict[result]
#            field_value = result_value[var1]
#            result_dict[result] = field_value
#        elif result in PROTOCOL_MAPPING:
#            result_value = PROTOCOL_MAPPING[result]
#            var1 = result_dict[result]
#            field_value = result_value[var1]
#            result_dict[result] = field_value
    return result_dict

# def integer_to_string_mapping_list(result_dict):
#    pdb.set_trace() 
#    for result in result_dict:
#      for result_key in result:
#        if result_key in REVERSE_FIELD_MAPPING:
#           result_value= REVERSE_FIELD_MAPPING[result_key]
#           var1 = result[result_key]
#           field_value = result_value[var1]
#           result[result_key] = field_value
#    return result_dict

def integer_to_string_mapping_show(result_dict):
#    pdb.set_trace()
    for result in result_dict:
        if result in REVERSE_FIELD_MAPPING:
            result_value = REVERSE_FIELD_MAPPING[result]
            var = result_dict[result]
            var1 = str(var)
            field_value = result_value[var1]
            result_dict[result] = field_value
#        elif result in REVERSE_ACTION_MAPPING:
#            result_value = REVERSE_ACTION_MAPPING[result]
#            var1 = result_dict[result]
#            field_value = result_value[var1]
#            result_dict[result] = field_value
#        elif result in REVERSE_PROTOCOL_MAPPING:
#            result_value = REVERSE_PROTOCOL_MAPPING[result]
#            var1 = result_dict[result]
#            field_value = result_value[var1]
#            result_dict[result] = field_value
    return result_dict

def check_integer_range(integer_value_str):
    """Validate integer range
    Args:
        integer_value (str): integer value

    Returns:
        int value
    """
#    pdb.set_trace()
    if integer_value_str == None:
        return False
    integer_value = int(integer_value_str)
    if integer_value < 1 or integer_value >= 65535:
#            msg = _("not a valid integer value")
 #           raise argparse.ArgumentTypeError()
            return False
    else:
            return integer_value

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


def _is_valid_host(hostname):
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

