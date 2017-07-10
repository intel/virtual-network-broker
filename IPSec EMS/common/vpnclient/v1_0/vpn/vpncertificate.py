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
from vpnclient.v1_0.vpn.utils_vpn import check_name_len, check_description_len

_COMMAND_COLUMNS = [
    'id',
    'name',
    'description',
    'certificate',
    'key',
    'right_id',
    'vpncacertificate_id'
]

_HTTP_RESOURCE = 'vpncertificates'


class CreateVPNCertificate(CommandResource):
    """Create a VPNCertificate"""
    resource = 'vpncertificates'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            type=check_name_len,
            help=FH(_("Name of the VPNCertificate")))

        parser.add_argument(
            '--description',
            type=check_description_len,
            default='',
            help=FH(_("Description of the VPNCertificate")))

        parser.add_argument(
            '--certificate',
            type=argparse.FileType('rb'),
            help=FH(_("File Path of Certificate")))

        parser.add_argument(
            '--key',
            type=argparse.FileType('rb'),
            help=FH(_("File Path of Key")))

        parser.add_argument(
            '--right-id',
            help=FH(_("ID of VPN Endpoint")))

        parser.add_argument(
            '--vpncacertificate-id',
            help=FH(_("ID of associated VPNCACertificate")))

        return parser


class ShowVPNCertificate(CommandResource):
    """Show information of a given VPNCertificate"""
    resource = 'vpncertificates'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNCERTIFICATE',
            help=FH(_("ID or Name of VPNCertificate to search")))

        return parser


class ListVPNCertificate(CommandResource):
    """List VPNCertificate"""
    resource = 'vpncacertificates'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateVPNCertificate(CommandResource):
    """Update a given VPNCertificate"""
    resource = 'vpncacertificates'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNCERTIFICATE',
            help=FH(_("ID or Name of VPNCertificate to update")))

        parser.add_argument(
            '--name',
            type=check_name_len,
            help=FH(_("Name of the VPNCertificate")))

        parser.add_argument(
            '--description',
            type=check_description_len,
            help=FH(_("Description of the VPNCertificate")))

        parser.add_argument(
            '--certificate',
            type=argparse.FileType('br'),
            help=FH(_("File Path of Certificate")))

        parser.add_argument(
            '--key',
            type=argparse.FileType('rb'),
            help=FH(_("File Path of Key")))

        parser.add_argument(
            '--right-id',
            help=FH(_("ID of VPN Endpoint")))

        parser.add_argument(
            '--vpncacertificate-id',
            help=FH(_("ID of associated VPNCACertificate")))

        return parser


class DeleteVPNCertificate(CommandResource):
    """Delete a given VPNCertificate"""
    resource = 'vpncacertificates'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNCERTIFICATE',
            help=FH(_("ID or Name of VPNCertificate to delete")))

        return parser
