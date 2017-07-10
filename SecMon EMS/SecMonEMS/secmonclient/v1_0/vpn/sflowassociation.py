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
import pdb
from django.utils.translation import ugettext as _
from secmonclient.utils import FH
from secmonclient.v1_0.vpn.command_resource import CommandResource
from secmonclient.v1_0.vpn.utils_vpn import (
    check_integer_range, remove_duplicates_from_list,
    help_algorithm_options, help_dh_options
)
# from secmonclient.v1_0.vpn.vpn_choices import (
#    IKEV1_INTEGRITY_ALGORITHM, IKEV2_INTEGRITY_ALGORITHM,
#    IKEV1_ENCRYPTION_ALGORITHM, IKEV2_ENCRYPTION_ALGORITHM,
#    DH_GROUP, LIFETIME_UNITS
# )

COMMAND_COLUMNS = [
    'id',
    'originator_vm_id',
    'collector_id',
    'direction',
    'policy_id',
    'scope_id',
]

HTTP_RESOURCE = 'sflowassociation'

# SFlowAssocciation Attributes' Choices

DIRECTIONCHOICES = [
    'INGRESS',
    'EGRESS',
    'BOTH',
]


def common_verify_collector_arguments(attrs):

    if attrs.get('direction') not in DIRECTIONCHOICES	:
        error_msg = _("direction has invalid choice(s) for SFlowAssociation")
        raise argparse.ArgumentTypeError(error_msg)


class CreateSFlowAssociation(CommandResource):
    """Create an SFlowAssociation"""
    resource = 'slowassociation'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            '--collector-id',
            metavar='COLLECTOR_ID',
            help=FH(_("Collector_ID of the SFlowAssociation")))

        parser.add_argument(
            '--originator-vm-id',
            metavar='ORIGINATOR_VM_ID',
            help=FH(_("Originator_vm_id of the SFlowAssociation")))

        parser.add_argument(
            '--policy-id',
            metavar='POICY_ID',
            help=FH(_("Policy_id of the SFlowAssociation")))

        parser.add_argument(
            '--scope-id',
            metavar='SCOPE_ID',
            help=FH(_("Scope_id of the SFlowAssociation")))

        parser.add_argument(
            '--direction',
            choices=DIRECTIONCHOICES,
            help=FH(_("SFlowAssociation Direction")))

        return parser

    @staticmethod
    def verify_arguments(attrs):
        common_verify_collector_arguments(attrs)


class ShowSFlowAssociation(CommandResource):
    """Show information of a given SFlowAssociation"""
    resource = 'sflowassociation'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='SFLOWASSOCIATION',
            help=FH(_("ID oF SFlowAssociation to search\n\n")))

        return parser


class ListSFlowAssociation(CommandResource):
    """List SFlowAssociation"""
    resource = 'sflowassociation'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            '-D', '--show-details',
            help=FH(_("Show detailed information")),
            action='store_true',
            default=False, )

        parser.add_argument(
            '--field',
            dest='fields',
            metavar='FIELD',
            help=FH(_(
                   "Specify the field(s) to be displayed in the output. You\n"
                   "can repeat this option.")),
            action='append',
            default=[])

        parser.add_argument(
            '--sort-key',
            metavar='FIELD',
            action='append',
            help=FH(_(
                   "Sorts the list by the specified fields in the specified\n"
                   "directions. You can repeat this option, but you must\n"
                   "specify an equal number of sort_direction and sort_key\n"
                   "values. Extra sort_direction options are ignored.\n"
                   "Missing sort_direction options use the default asc\n"
                   "value.")),
            default=[])

        parser.add_argument(
            '--sort-direction',
            metavar='{asc,desc}',
            help=FH(_("Sorts the list in the specified direction. You can\n"
                      "repeat this option.\n\n")),
            action='append',
            default=[],
            choices=['asc', 'desc'])

        formatter_group = parser.add_argument_group(
            title='output formatters',
            description='output formatter options')
        formatter_group.add_argument(
            '--format',
            dest='formatter',
            default='table',
            choices=['csv', 'html', 'table'],
            help=FH(_("the output format, Default: table\n\n")))

        return parser


class UpdateSFlowAssociation(CommandResource):
    """Update a given SFlowAssociation"""
    resource = 'sflowassociation'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='SFLOWASSOCIATION',
            help=FH(_("ID of SFlowAssociation to update")))

        parser.add_argument(
            '--collector-id',
            metavar='COLLECTOR_ID',
            help=FH(_("Collector_ID of the SFlowAssociation")))

        parser.add_argument(
            '--originator-vm-id',
            metavar='ORIGINATOR_VM_ID',
            help=FH(_("Originator_vm_id of the SFlowAssociation")))

        parser.add_argument(
            '--policy-id',
            metavar='POICY_ID',
            help=FH(_("Policy_id of the SFlowAssociation")))

        parser.add_argument(
            '--scope-id',
            metavar='SCOPE_ID',
            help=FH(_("Scope_id of the SFlowAssociation")))

        parser.add_argument(
            '--direction',
            choices=DIRECTIONCHOICES,
            help=FH(_("SFlowAssociation Direction")))

        return parser

    @staticmethod
    def verify_arguments(attrs):
        common_verify_collector_arguments(attrs)


class DeleteSFlowAssociation(CommandResource):
    """Delete a given SFlowAssociation"""
    resource = 'sflowassociation'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='SFLOWASSOCIATION',
            help=FH(_("ID of SFlowAssociation to delete")))

        return parser
