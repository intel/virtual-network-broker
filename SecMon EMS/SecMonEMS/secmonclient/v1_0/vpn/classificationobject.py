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
    'src_ip',
    'src_mac',
    'src_ip_subnet',
    'minimum_src_port',
    'maximum_src_port',
    'dst_ip',
    'dst_mac',
    'dst_ip_subnet',
    'minimum_dst_port',
    'maximum_dst_port',
    'protocol',
]

HTTP_RESOURCE = 'classificationobject'

# Classificationobject Attributes' Choices


class CreateClassificationObject(CommandResource):
    """Create an Classificationobject"""
    resource = 'classificationobject'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            help=FH(_("Name of the Classificationobject")))

        parser.add_argument(
            '--src-ip',
            help=FH(_("Source IP of the Classificationobject")))

        parser.add_argument(
            '--src-mac',
            help=FH(_("Source IP of the Classificationobject")))

        parser.add_argument(
            '--src-ip-subnet',
            type=check_integer_range,
            help=FH(_("Source IP subnet for Classificationobject")))

        parser.add_argument(
            '--minimum-src-port',
            type=check_integer_range,
            help=FH(_("Minimum source port for Classificationobject")))

        parser.add_argument(
            '--maximum-src-port',
            type=check_integer_range,
            help=FH(_("Maximum source port for Classificationobject")))

        parser.add_argument(
            '--dst-ip',
            help=FH(_("Destination IP of the Classificationobject")))

        parser.add_argument(
            '--dst-mac',
            help=FH(_("Destination MAC of the Classificationobject")))

        parser.add_argument(
            '--dst-ip-subnet',
            type=check_integer_range,
            help=FH(_("Destination IP subnet for Classificationobject")))

        parser.add_argument(
            '--minimum-dst-port',
            type=check_integer_range,
            help=FH(_("Minimum destination port for Classificationobject")))

        parser.add_argument(
            '--maximum-dst-port',
            type=check_integer_range,
            help=FH(_("Maximum destination port for Classificationobject")))

        parser.add_argument(
            '--protocol',
            help=FH(_("Protocol for Classificationobject")))

        return parser


class ShowClassificationObject(CommandResource):
    """Show information of a given Classificationobject"""
    resource = 'classificationobject'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='CLASSIFICATIONOBJECT',
            help=FH(_("ID of Classificatioobject to search\n\n")))

        return parser


class ListClassificationObject(CommandResource):
    """List Classificationobject"""
    resource = 'classificationobject'
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


class UpdateClassificationObject(CommandResource):
    """Update a given Classificationobject"""
    resource = 'classificationobject'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='CLASSIFICATIONOBJECT',
            help=FH(_("ID of ClassificationObject to update")))

        parser.add_argument(
            'name',
            metavar='NAME',
            help=FH(_("Name of the Classificationobject")))

        parser.add_argument(
            '--src-ip',
            help=FH(_("Source IP of the Classificationobject")))

        parser.add_argument(
            '--src-mac',
            help=FH(_("Source IP of the Classificationobject")))

        parser.add_argument(
            '--src-ip-subnet',
            type=check_integer_range,
            help=FH(_("Source IP subnet for Classificationobject")))

        parser.add_argument(
            '--minimum-src-port',
            type=check_integer_range,
            help=FH(_("Minimum source port for Classificationobject")))

        parser.add_argument(
            '--maximum-src-port',
            type=check_integer_range,
            help=FH(_("Maximum source port for Classificationobject")))

        parser.add_argument(
            '--dst-ip',
            help=FH(_("Destination IP of the Classificationobject")))

        parser.add_argument(
            '--dst-mac',
            help=FH(_("Destination MAC of the Classificationobject")))

        parser.add_argument(
            '--dst-ip-subnet',
            type=check_integer_range,
            help=FH(_("Destination IP subnet for Classificationobject")))

        parser.add_argument(
            '--minimum-dst-port',

            type=check_integer_range,
            help=FH(_("Minimum destination port for Classificationobject")))

        parser.add_argument(
            '--maximum-dst-port',
            type=check_integer_range,
            help=FH(_("Maximum destination port for Classificationobject")))

        parser.add_argument(
            '--protocol',
            type=check_integer_range,
            help=FH(_("Protocol for Classificationobject")))

        return parser


class DeleteClassificationObject(CommandResource):
    """Delete a given Classificationobject"""
    resource = 'classificationobject'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='CLASSIFICATIONOBJECT',
            help=FH(_("ID of Classificationobject to delete")))

        return parser
