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

from vpnclient.utils import FH
from vpnclient.v1_0.command_list import ListCommand
from vpnclient.v1_0.command_resource import CommandResource
from vpnclient.v1_0.vpn.utils_vpn import (
    check_lifetime_value, help_algorithm_options, help_dh_options,
    check_name_len, DefaultList)
from vpnclient.v1_0.vpn.vpn_choices import (
    IPSEC_IKEV1_ENCRYPTION_ALGORITHM, IPSEC_IKEV2_ENCRYPTION_ALGORITHM,
    IPSEC_IKEV1_INTEGRITY_ALGORITHM, IPSEC_IKEV2_INTEGRITY_ALGORITHM,
    DH_GROUP, LIFETIME_UNITS
)

_COMMAND_COLUMNS = [
    'id',
    'name',
    'description',
    'transform_protocol',
    'encryption_algorithm',
    'integrity_algorithm',
    'dh_group',
    'esn_mode',
    'encapsulation_mode',
    'lifetime_value',
    'lifetime_units',
]

_HTTP_RESOURCE = 'ipsecpolicies'

# IPsecPolicy Attributes' Choices

_IPSEC_ESN_MODE = [
        'esn',
        'noesn',
]

_IPSEC_TRANSFORM_PROTOCOL = [
    'ah',
    'esp',
]

_IPSEC_ENCAPSULATION_MODE = [
    'transport',
    'tunnel',
]


def common_verify_ikepolicy_arguments(attrs):

    if attrs.get('ike_version', None) == 'v1':

        if not set(attrs.get('encryption_algorithm', [])).issubset(
                set(IPSEC_IKEV1_ENCRYPTION_ALGORITHM)):
            error_msg = _("encryption-algorithm has invalid choice(s) for IKE "
                          "version 1")
            raise argparse.ArgumentTypeError(error_msg)

        if not set(attrs.get('integrity_algorithm', [])).issubset(
                set(IPSEC_IKEV1_INTEGRITY_ALGORITHM)):
            error_msg = _("integrity-algorithm has invalid choice(s) for IKE "
                          "version 1")
            raise argparse.ArgumentTypeError(error_msg)

    if attrs.get('ike_version', None) == 'v2':

        if not set(attrs.get('encryption_algorithm', [])).issubset(
                set(IPSEC_IKEV2_ENCRYPTION_ALGORITHM)):
            error_msg = _("encryption-algorithm has invalid choice(s) for IKE "
                          "version 2")
            raise argparse.ArgumentTypeError(error_msg)

        if not set(attrs.get('integrity_algorithm', [])).issubset(
                set(IPSEC_IKEV2_INTEGRITY_ALGORITHM)):
            error_msg = _("integrity-algorithm has invalid choice(s) for IKE "
                          "version 2")
            raise argparse.ArgumentTypeError(error_msg)

    dh_group = attrs.get('dh_group')
    if dh_group is not None and not set(dh_group).issubset(
                set(DH_GROUP)):
            error_msg = _("dh_group has invalid choice(s)")
            raise argparse.ArgumentTypeError(error_msg)

    if (attrs.get('ike_version', None) == 'v1' and
            attrs.get('reauth', None) == 'no'):
        error_msg = _("reauth value 'no' is an invalid choice for IKE "
                      "version 1")
        raise argparse.ArgumentTypeError(error_msg)

    if (attrs.get('ike_version', None) == 'v1' and
            len(attrs.get('encryption_algorithm', [])) > 1):
        error_msg = _("Multiple encryption-algorithm values are not applicable "
                      "for IKE version 1")
        raise argparse.ArgumentTypeError(error_msg)

    if (attrs.get('ike_version', None) == 'v1' and
            len(attrs.get('auth_algorithm', [])) > 1):
        error_msg = _("Multiple integrity-algorithm values are not applicable "
                      "for IKE version 1")
        raise argparse.ArgumentTypeError(error_msg)

    if (attrs.get('ike_version', None) == 'v1' and
            len(attrs.get('dh_group', [])) > 1):
        error_msg = _("Multiple dh_group values are not applicable for IKE "
                      "version 1")
        raise argparse.ArgumentTypeError(error_msg)


class CreateIPsecPolicy(CommandResource):
    """Create an IPsecPolicy"""
    resource = 'ipsecpolicies'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            type=check_name_len,
            help=FH(_("Name of the IPsecPolicy")))

        parser.add_argument(
            '--description',
            default='',
            help=FH(_("Description of the IPsecPolicy")))

        parser.add_argument(
            '--transform-protocol',
            default='esp',
            choices=_IPSEC_TRANSFORM_PROTOCOL,
            help=FH(_("Transform protocol in lowercase, Default: esp")))

        parser.add_argument(
            '--encryption-algorithm',
            default=DefaultList(['aes128']),
            action='append',
            help=FH(_(
                  "Encryption algorithm in lowercase, Default: aes-128 \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "encryption-algorithms") +
                  help_algorithm_options('ipsec', 'encryption')))

        parser.add_argument(
            '--integrity-algorithm',
            default=DefaultList(['sha1']),
            action='append',
            help=FH(_(
                  "Authentication algorithm in lowercase, Default: sha1 \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "integrity-algorithms") +
                  help_algorithm_options('ipsec', 'integrity')))

        parser.add_argument(
            '--dh-group',
            default=DefaultList(['modp1536']),
            action='append',
            help=FH(_(
                  "Diffie-Hellman dhgroup in lowercase, Default: modp1536 \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "dh-groups") + help_dh_options()))

        parser.add_argument(
            '--esn-mode',
            default='noesn',
            choices=_IPSEC_ESN_MODE,
            help=FH(_("Extended Sequence Number(ESN) Mode, Default: noesn")))

        parser.add_argument(
            '--encapsulation-mode',
            default='tunnel',
            choices=_IPSEC_ENCAPSULATION_MODE,
            help=FH(_("Encapsulation mode in lowercase, Default: tunnel")))

        parser.add_argument(
            '--lifetime-value',
            type=check_lifetime_value,
            default='3600',
            help=FH(_("IPsec lifetime value of the security association")))

        parser.add_argument(
            '--lifetime-units',
            default='seconds',
            choices=LIFETIME_UNITS,
            help=FH(_("IPsec lifetime units of the security association")))

        return parser


class ShowIPsecPolicy(CommandResource):
    """Show information of a given IPsecPolicy"""
    cmd_resource = 'ipsecpolicy'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class ListIPsecPolicy(CommandResource):
    """List IPsecPolicies"""
    resource = 'ipsecpolicies'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateIPsecPolicy(CommandResource):
    """Update a given IPsecPolicy"""
    resource = 'ipsecpolicies'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='IPSECPOLICY',
            help=FH(_("ID or Name of IPsecPolicy to update")))

        parser.add_argument(
            '--name',
            type=check_name_len,
            help=FH(_("Name of the IPsecPolicy")))

        parser.add_argument(
            '--description',
            help=FH(_("Description of the IPsecPolicy")))

        parser.add_argument(
            '--transform-protocol',
            choices=_IPSEC_TRANSFORM_PROTOCOL,
            help=FH(_("Transform protocol in lowercase")))

        parser.add_argument(
            '--encryption-algorithm',
            action='append',
            help=FH(_(
                  "Encryption algorithm in lowercase. \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "encryption-algorithms") +
                  help_algorithm_options('ipsec', 'encryption')))

        parser.add_argument(
            '--integrity-algorithm',
            action='append',
            help=FH(_(
                  "Authentication algorithm in lowercase. \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "integrity-algorithms") +
                  help_algorithm_options('ipsec', 'integrity')))

        parser.add_argument(
            '--dh-group',
            action='append',
            help=FH(_(
                  "Diffie-Hellman dhgroup in lowercase, Default: modp1536 \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "dh-groups") + help_dh_options()))

        parser.add_argument(
            '--esn-mode',
            choices=_IPSEC_ESN_MODE,
            help=FH(_("Extended Sequence Number(ESN) Mode, Default: noesn")))

        parser.add_argument(
            '--encapsulation-mode',
            choices=_IPSEC_ENCAPSULATION_MODE,
            help=FH(_("Encapsulation mode in lowercase")))

        parser.add_argument(
            '--lifetime-value',
            type=int,
            help=FH(_("IPsec lifetime value of the security association")))

        parser.add_argument(
            '--lifetime-units',
            choices=LIFETIME_UNITS,
            help=FH(_("IPsec lifetime units of the security association in \n"
                      "lowercase")))

        return parser


class DeleteIPsecPolicy(CommandResource):
    """Delete a given IPsecPolicy"""
    resource = 'ipsecpolicies'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='IPSECPOLICY',
            help=FH(_("ID or Name of IPsecPolicy to delete")))

        return parser
