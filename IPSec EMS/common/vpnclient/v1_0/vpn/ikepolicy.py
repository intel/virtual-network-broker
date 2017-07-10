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
    IKEV1_INTEGRITY_ALGORITHM, IKEV2_INTEGRITY_ALGORITHM,
    IKEV1_ENCRYPTION_ALGORITHM, IKEV2_ENCRYPTION_ALGORITHM,
    DH_GROUP, LIFETIME_UNITS
)

_COMMAND_COLUMNS = [
    'id',
    'name',
    'description',
    'encryption_algorithm',
    'integrity_algorithm',
    'dh_group',
    'phase1_negotiation_mode',
    'lifetime_value',
    'lifetime_units',
    'ike_version',
    'rekey',
    'reauth',
]

_HTTP_RESOURCE = 'ikepolicies'

# IKEPolicy Attributes' Choices

_IKE_PHASE1_MODE = [
    'aggressive',
    'main',
]

_IKE_VERSION = [
    'v1',
    'v2',
]

_IKE_REKEY = [
    'yes',
    'no',
]

_IKE_REAUTH = [
    'yes',
    'no',
]


def common_verify_ikepolicy_arguments(attrs):

    if attrs.get('ike_version', None) == 'v1':

        if not set(attrs.get('encryption_algorithm', [])).issubset(
                set(IKEV1_ENCRYPTION_ALGORITHM)):
            error_msg = _("encryption-algorithm has invalid choice(s) for IKE "
                          "version 1")
            raise argparse.ArgumentTypeError(error_msg)

        if not set(attrs.get('integrity_algorithm', [])).issubset(
                set(IKEV1_INTEGRITY_ALGORITHM)):
            error_msg = _("integrity-algorithm has invalid choice(s) for IKE "
                          "version 1")
            raise argparse.ArgumentTypeError(error_msg)

    if attrs.get('ike_version', None) == 'v2':

        if not set(attrs.get('encryption_algorithm', [])).issubset(
                set(IKEV2_ENCRYPTION_ALGORITHM)):
            error_msg = _("encryption-algorithm has invalid choice(s) for IKE "
                          "version 2")
            raise argparse.ArgumentTypeError(error_msg)

        if not set(attrs.get('integrity_algorithm', [])).issubset(
                set(IKEV2_INTEGRITY_ALGORITHM)):
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


class CreateIKEPolicy(CommandResource):
    """Create an IKEPolicy"""
    resource = 'ikepolicy'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            type=check_name_len,
            help=FH(_("Name of the IKEPolicy")))

        parser.add_argument(
            '--description',
            default='',
            help=FH(_("Description of the IKEPolicy")))

        parser.add_argument(
            '--ike-version',
            default='v2',
            choices=_IKE_VERSION,
            help=FH(_("IKE version in lowercase, Default: v2")))

        parser.add_argument(
            '--encryption-algorithm',
            default=DefaultList(['aes128']),
            action='append',
            help=FH(_(
                  "Encryption algorithm in lowercase, Default: aes-128 \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "encryption-algorithms") +
                  help_algorithm_options('ike', 'encryption')))

        parser.add_argument(
            '--integrity-algorithm',
            default=DefaultList(['sha1']),
            action='append',
            help=FH(_(
                  "Authentication algorithm in lowercase, Default: sha1 \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "integrity-algorithms") +
                  help_algorithm_options('ike', 'integrity')))

        parser.add_argument(
            '--dh-group',
            default=DefaultList(['modp1536']),
            action='append',
            help=FH(_(
                  "Diffie-Hellman dhgroup in lowercase, Default: modp1536 \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "dh-groups") + help_dh_options()))

        parser.add_argument(
            '--phase1-negotiation-mode',
            default='main',
            choices=_IKE_PHASE1_MODE,
            help=FH(_("IKE Phase1 negotiation mode in lowercase, \n"
                      "Default: main")))

        parser.add_argument(
            '--lifetime-value',
            type=check_lifetime_value,
            default='3600',
            help=FH(_("IKE lifetime value of the security association, \n"
                      "Default: 3600")))

        parser.add_argument(
            '--lifetime-units',
            default='seconds',
            choices=LIFETIME_UNITS,
            help=FH(_("IKE lifetime units of the security association in \n"
                      "lowercase, Default: seconds")))

        parser.add_argument(
            '--rekey',
            default='yes',
            choices=_IKE_REKEY,
            help=FH(_("Whether a connection should be renegotiated when it \n"
                      "is about to expire in lowercase, Default: yes")))

        parser.add_argument(
            '--reauth',
            default='yes',
            choices=_IKE_REAUTH,
            help=FH(_("whether rekeying should also reauthenticate the peer \n"
                      "in lower case, Default: yes \n"
                      "Option 'no' is only valid for IKE version 1.")))

        return parser

    @staticmethod
    def verify_arguments(attrs):
        common_verify_ikepolicy_arguments(attrs)


class ShowIKEPolicy(CommandResource):
    """Show information of a given IKEPolicy"""
    resource = 'ikepolicy'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='IKEPOLICY',
            help=FH(_("ID or Name of IKEPolicy to search")))

        return parser


class ListIKEPolicy(CommandResource):
    """List IKEPolicies"""
    resource = 'ikepolicy'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateIKEPolicy(CommandResource):
    """Update a given IKEPolicy"""
    resource = 'ikepolicy'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='IKEPOLICY',
            help=FH(_("ID or Name of IKEPolicy to update")))

        parser.add_argument(
            '--name',
            type=check_name_len,
            help=FH(_("Name of the IKEPolicy")))

        parser.add_argument(
            '--description',
            help=FH(_("Description of the IKEPolicy")))

        parser.add_argument(
            '--ike-version',
            choices=_IKE_VERSION,
            help=FH(_("IKE version in lowercase")))

        parser.add_argument(
            '--encryption-algorithm',
            action='append',
            help=FH(_(
                  "Encryption algorithm in lowercase. \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "encryption-algorithms") +
                   help_algorithm_options('ike', 'encryption')))

        parser.add_argument(
            '--integrity-algorithm',
            action='append',
            help=FH(_(
                 "Authentication algorithm in lowercase. \n"
                 "For IKE version 2, repeat this option to specify multiple \n"
                 "integrity-algorithms") +
                 help_algorithm_options('ike', 'integrity')))

        parser.add_argument(
            '--dh-group',
            action='append',
            help=FH(_(
                  "Diffie-Hellman dhgroup in lowercase. \n"
                  "For IKE version 2, repeat this option to specify multiple \n"
                  "dh-groups") + help_dh_options()))

        parser.add_argument(
            '--phase1-negotiation-mode',
            choices=_IKE_PHASE1_MODE,
            help=FH(_("IKE Phase1 negotiation mode in lowercase")))

        parser.add_argument(
            '--lifetime-value',
            type=int,
            help=FH(_("IKE lifetime value of the security association")))

        parser.add_argument(
            '--lifetime-units',
            choices=LIFETIME_UNITS,
            help=FH(_("IKE lifetime units of the security association in \n"
                      "lowercase")))

        parser.add_argument(
            '--rekey',
            choices=_IKE_REKEY,
            help=FH(_("Whether a connection should be renegotiated when it \n"
                      "is about to expire")))

        parser.add_argument(
            '--reauth',
            choices=_IKE_REAUTH,
            help=FH(_("Whether rekeying should also reauthenticate the peer. \n"
                      "Option 'no' is only valid for IKE version 1")))

        return parser

    @staticmethod
    def verify_arguments(attrs):
        common_verify_ikepolicy_arguments(attrs)


class DeleteIKEPolicy(CommandResource):
    """Delete a given IKEPolicy"""
    resource = 'ikepolicy'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='IKEPOLICY',
            help=FH(_("ID or Name of IKEPolicy to delete")))

        return parser
