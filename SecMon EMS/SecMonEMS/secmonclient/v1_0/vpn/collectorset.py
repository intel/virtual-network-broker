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
#from django.utils.translation import ugettext as _
from secmonclient.utils import FH
from secmonclient.v1_0.vpn.command_resource import CommandResource
from secmonclient.v1_0.vpn.utils_vpn import (
    check_integer_range, remove_duplicates_from_list,
    help_algorithm_options, help_dh_options
)

COMMAND_COLUMNS = [
    'id',
    'name',
    'collector_ids',
    'col_type',
    'lb_algo'
]

HTTP_RESOURCE = 'collectorset'

# Collectorset Attributes' Choices

PLUGIN_NAME = [
    'netflow',
    'sflow',
    'rawforward',
]

LB_ALGO_NAME = [
    'session_based',
    'round_robin',
    'weighted_round_robin',
]


def common_verify_collectorset_arguments(attrs):

    if attrs.get('col_type') not in PLUGIN_NAME:
        error_msg = _("col_type has invalid choice(s) for Collectorset")
        raise argparse.ArgumentTypeError(error_msg)

#    if attrs.get('lb_algo') not in LB_ALGO_NAME:
#        error_msg = _("lb_algo has invalid choice(s) for Collectorset")
#        raise argparse.ArgumentTypeError(error_msg)


class CreateCollectorset(CommandResource):
    """Create an Collectorset"""
    resource = 'collectorset'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            help=FH(_("Name of the Collectorset")))

        parser.add_argument(
            '--collector-ids',
            help=FH(_("Collector_IDs of the Collectorset")))

        parser.add_argument(
            '--col-type',
            choices=PLUGIN_NAME,
            help=FH(_("Collector Type")))

        parser.add_argument(
            '--lb-algo',
#            choices=LB_ALGO_NAME,
            help=FH(_("Lb_algo of the collectorset")))

        return parser

    @staticmethod
    def verify_arguments(attrs):

        common_verify_collectorset_arguments(attrs)


class ShowCollectorset(CommandResource):
    """Show information of a given Collectorset"""
    resource = 'collectorset'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='COLLECTORSET',
            help=FH(_("ID of Collectorset to search\n\n")))

        return parser


class ListCollectorset(CommandResource):
    """List Collectorset"""
    resource = 'collectorset'
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


class UpdateCollectorset(CommandResource):
    """Update a given Collectorset"""
    resource = 'collectorset'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='COLLECTORSET',
            help=FH(_("ID of Collectorset to update")))

        parser.add_argument(
            'name',
            metavar='NAME',
            help=FH(_("Name of the Collectorset")))

        parser.add_argument(
            '--collector-ids',
            help=FH(_("Collector_IDs of the Collectorset")))

        parser.add_argument(
            '--col-type',
            choices=PLUGIN_NAME,
            help=FH(_("Collectorset Type")))

        parser.add_argument(
            '--lb-algo',
#            choices=LB_ALGO_NAME,
            help=FH(_("Lb_algo of the collectorset")))

        return parser

    @staticmethod
    def verify_arguments(attrs):

        common_verify_collectorset_arguments(attrs)


class DeleteCollectorset(CommandResource):
    """Delete a given Collectorset"""
    resource = 'collectorset'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='COLLECTORSET',
            help=FH(_("ID of Collectorset to delete")))

        return parser
