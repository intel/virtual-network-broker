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

from vpnclient.utils import FH
from vpnclient.v1_0.command_list import ListCommand
from vpnclient.v1_0.command_resource import CommandResource
from vpnclient.v1_0.vpn.utils_vpn import check_name_len, check_description_len

_COMMAND_COLUMNS = [
    'id',
    'name',
    'description',
    'vpncertificate_id',
]

_HTTP_RESOURCE = 'vpnendpointgroups'


class CreateVPNEndpointGroup(CommandResource):
    """Create a VPNEndpointGroup"""
    resource = 'vpnendpointgroups'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            type=check_name_len,
            help=FH(_("Name of the VPNEndpointGroup")))

        parser.add_argument(
            '--description',
            type=check_description_len,
            default='',
            help=FH(_("Description of the VPNEndpointGroup")))

        parser.add_argument(
            '--vpncertificate-id',
            help=FH(_("ID of VPNCertificate \n"
                      "Only required for when authentication mode is 'cert'")))

        return parser


class ShowVPNEndpointGroup(CommandResource):
    """Show information of a given VPNEndpointGroup"""
    resource = 'vpnendpointgroups'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNENDPOINTGROUP',
            help=FH(_("ID or Name of VPNEndpointGroup to search")))

        return parser


class ListVPNEndpointGroup(CommandResource):
    """List VPNEndpointGroups"""
    resource = 'vpnendpointgroups'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateVPNEndpointGroup(CommandResource):
    """Update a given VPNEndpointGroup"""
    resource = 'vpnendpointgroups'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNENDPOINTGROUP',
            help=FH(_("ID or Name of VPNEndpointGroup to update")))

        parser.add_argument(
            '--name',
            type=check_name_len,
            help=FH(_("Name of the VPNEndpointGroup")))

        parser.add_argument(
            '--description',
            type=check_description_len,
            help=FH(_("Description of the VPNEndpointGroup")))

        parser.add_argument(
            '--vpncertificate-id',
            help=FH(_("ID of VPNCertificate \n"
                      "Only required for when authentication mode is 'cert'")))

        return parser


class DeleteVPNEndpointGroup(CommandResource):
    """Delete a given VPNEndpointGroup"""
    resource = 'vpnendpointgroups'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNENDPOINTGROUP',
            help=FH(_("ID or Name of VPNEndpointGroup to delete")))

        return parser
