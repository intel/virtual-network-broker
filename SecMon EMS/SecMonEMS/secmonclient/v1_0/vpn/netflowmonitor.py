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

COMMAND_COLUMNS = [
    'id',
    'scope_id',
    'match_fields',
    'collect_fields',
]

HTTP_RESOURCE = 'netflowmonitor'


class CreateNetFlowMonitor(CommandResource):
    """Create a NetFlowMonitor"""
    resource = 'netflowmonitor'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            '--scope-id',
            help=FH(_("Scope_ID for Netflowmonitor")))

        parser.add_argument(
            '--match-fields',
            help=FH(_("Match_fields of the Netflowmonitor")))

        parser.add_argument(
            '--collect-fields',
            help=FH(_("Collect_fields for Netflowmonitor")))

        return parser


class ShowNetFlowMonitor(CommandResource):
    """Show information of a given Netflowmonitor"""
    resource = 'netflowmonitor'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='NETFLOWMONITOR',
            help=FH(_("Name of Netflowmonitor to search\n\n")))

        return parser


class ListNetFlowMonitor(CommandResource):
    """List NetFlowMonitor"""
    resource = 'netflowmonitor'
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


class UpdateNetFlowMonitor(CommandResource):
    """Update a given Netflowmonitor"""
    resource = 'netflowmonitor'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='NETFLOWMONITOR',
            help=FH(_("ID of Netflowmonitor to update")))

        parser.add_argument(
            '--scope-id',
            help=FH(_("Scope_ID for Netflowmonitor")))

        parser.add_argument(
            '--match-fields',
            help=FH(_("Match_fields of the Netflowmonitor")))

        parser.add_argument(
            '--collect-fields',
            help=FH(_("Collect_fields for Netflowmonitor")))

        return parser


class DeleteNetFlowMonitor(CommandResource):
    """Delete a given NetFlowMonitor"""
    resource = 'netflowmonitor'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='NETFLOWMONITOR',
            help=FH(_("ID of Netflowmonitor to delete")))

        return parser
