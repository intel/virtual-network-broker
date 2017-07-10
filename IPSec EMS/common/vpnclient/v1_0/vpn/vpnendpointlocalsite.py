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
from vpnclient.v1_0.vpn.utils_vpn import (
    check_cidr, check_cidrs, check_description_len, check_name_len
)

_COMMAND_COLUMNS = [
    'id',
    'name',
    'description',
    'cidrs',
    'vpncertificate_id',
]

_HTTP_RESOURCE = 'vpnendpointlocalsites'


def common_verify_endpointlocalsite_arguments(attrs):
    cidrs = attrs.get('cidrs', [])
    if cidrs:
        check_cidrs(attrs.get('cidrs'))


class CreateVPNEndpointLocalSite(CommandResource):
    """Create an VPNEndpointLocalSite"""
    resource = 'vpnendpointlocalsites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            type=check_name_len,
            help=FH(_("Name of the VPNEndpointLocalSite")))

        parser.add_argument(
            '--description',
            type=check_description_len,
            default='',
            help=FH(_("Description of the VPNEndpointLocalSite")))

        parser.add_argument(
            '--cidrs',
            type=check_cidr,
            required=True,
            action='append',
            help=FH(_("Subnet(s) in CIDR format")))

        parser.add_argument(
            '--vpncertificate-id',
            help=FH(_("ID of VPNCertificate\n"
                      "Only required for when authentication mode is 'cert'")))

        return parser

    @staticmethod
    def verify_arguments(attrs):
        common_verify_endpointlocalsite_arguments(attrs)


class ShowVPNEndpointLocalSite(CommandResource):
    """Show information of a given VPNEndpointLocalSite"""
    resource = 'vpnendpointlocalsites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNENDPOINTLOCALSITE',
            help=FH(_("ID or Name of VPNEndpointLocalSite to search")))

        return parser


class ListVPNEndpointLocalSite(CommandResource):
    """List VPNEndpointLocalSites"""
    resource = 'vpnendpointlocalsites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateVPNEndpointLocalSite(CommandResource):
    """Update a given VPNEndpointLocalSite"""
    resource = 'vpnendpointlocalsites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNENDPOINTLOCALSITE',
            help=FH(_("ID or Name of VPNEndpointLocalSite to update")))

        parser.add_argument(
            '--name',
            type=check_name_len,
            help=FH(_("Name of the VPNEndpointLocalSite")))

        parser.add_argument(
            '--description',
            type=check_description_len,
            help=FH(_("Description of the VPNEndpointLocalSite")))

        parser.add_argument(
            '--cidrs',
            type=check_cidrs,
            action='append',
            help=FH(_("Subnet(s) in CIDR format")))

        parser.add_argument(
            '--vpncertificate-id',
            help=FH(_("ID of VPNCertificate\n"
                      "Only required for when authentication mode is 'cert'")))

        return parser

    @staticmethod
    def verify_arguments(attrs):
        common_verify_endpointlocalsite_arguments(attrs)


class DeleteVPNEndpointLocalSite(CommandResource):
    """Delete a given VPNEndpointLocalSite"""
    resource = 'vpnendpointlocalsites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNENDPOINTLOCALSITE',
            help=FH(_("ID or Name of VPNEndpointLocalSite to delete")))

        return parser
