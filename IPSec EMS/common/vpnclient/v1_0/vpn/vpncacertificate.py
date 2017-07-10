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

COMMAND_COLUMNS = [
    'id',
    'name',
    'description',
    'ca_certificate',
]

HTTP_RESOURCE = 'vpncacertificates'


class CreateVPNCACertificate(CommandResource):
    """Create a VPNCACertificate"""
    resource = 'vpncacertificates'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            type=check_name_len,
            help=FH(_("Name of the VPNCACertificate")))

        parser.add_argument(
            '--description',
            type=check_description_len,
            default='',
            help=FH(_("Description of the VPNCACertificate")))

        parser.add_argument(
            '--ca-certificate',
            type=argparse.FileType('rb'),
            help=FH(_("File Path of CA Certificate")))

        return parser


class ShowVPNCACertificate(CommandResource):
    """Show information of a given VPNCACertificate"""
    resource = 'vpncacertificates'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNCACERTIFICATE',
            help=FH(_("ID or Name of VPNCACertificate to search")))

        return parser


class ListVPNCACertificate(CommandResource):
    """List VPNCACertificate"""
    resource = 'vpncacertificates'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateVPNCACertificate(CommandResource):
    """Update a given VPNCACertificate"""
    resource = 'vpncacertificates'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNCACERTIFICATE',
            help=FH(_("ID or Name of VPNCACertificate to update")))

        parser.add_argument(
            '--name',
            type=check_name_len,
            help=FH(_("Name of the VPNCACertificate")))

        parser.add_argument(
            '--description',
            type=check_description_len,
            help=FH(_("Description of the VPNCACertificate")))

        parser.add_argument(
            '--ca-certificate',
            type=argparse.FileType('br'),
            help=FH(_("File Path of CA Certificate")))

        return parser


class DeleteVPNCACertificate(CommandResource):
    """Delete a given VPNCACertificate"""
    resource = 'vpncacertificates'
    cmd_columns = COMMAND_COLUMNS
    http_resource = HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNCACERTIFICATE',
            help=FH(_("ID or Name of VPNCACertificate to delete")))

        return parser
