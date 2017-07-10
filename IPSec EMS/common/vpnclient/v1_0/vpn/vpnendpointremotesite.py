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
    check_cidr, check_cidrs, check_ipaddress_or_fqdn, check_name_len,
    check_description_len
)

_COMMAND_COLUMNS = [
    'id',
    'name',
    'description',
    'peer_address',
    'peer_cidrs',
    'vpncertificate_id',
]

_HTTP_RESOURCE = 'vpnendpointremotesites'


def common_verify_endpointremotesite_arguments(attrs):
    peer_cidrs = attrs.get('peer_cidrs', [])
    if peer_cidrs:
        check_cidrs(attrs.get('peer_cidrs'))


class CreateVPNEndpointRemoteSite(CommandResource):
    """Create a VPNEndpointRemoteSite"""
    resource = 'vpnendpointremotesites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):

        parser.add_argument(
            'name',
            metavar='NAME',
            type=check_name_len,
            help=FH(_("Name of the VPNEndpointRemoteSite")))

        parser.add_argument(
            '--description',
            type=check_description_len,
            default='',
            help=FH(_("Description of the VPNEndpointRemoteSite")))

        parser.add_argument(
            '--peer-address',
            required=True,
            type=check_ipaddress_or_fqdn,
            help=FH(_("Peer gateway public IPv4/IPv6 address or FQDN")))

        parser.add_argument(
            '--peer-cidrs',
            required=True,
            type=check_cidr,
            action='append',
            help=FH(_("Peer subnet(s) in CIDR format. Repeat this option to \n"
                      "specify multiple CIDRs")))

        parser.add_argument(
            '--vpncertificate-id',
            help=FH(_("ID of VPNCertificate\n"
                      "Only required for when authentication mode is 'cert'")))

        return parser

    @staticmethod
    def verify_arguments(attrs):
        common_verify_endpointremotesite_arguments(attrs)


class ShowVPNEndpointRemoteSite(CommandResource):
    """Show information of a given VPNEndpointRemoteSite"""
    resource = 'vpnendpointremotesites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNENDPOINTREMOTESITE',
            help=FH(_("ID or Name of VPNEndpointRemoteSite to search")))

        return parser


class ListVPNEndpointRemoteSite(CommandResource):
    """List VPN EndpointRemoteSites"""
    resource = 'vpnendpointremotesites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateVPNEndpointRemoteSite(CommandResource):
    """Update a given VPNEndpointRemoteSite"""
    resource = 'vpnendpointremotesites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNENDPOINTREMOTESITE',
            help=FH(_("ID or Name of VPNEndpointRemoteSite to update")))

        parser.add_argument(
            '--name',
            type=check_name_len,
            help=FH(_("Name of the VPNEndpointRemoteSite")))

        parser.add_argument(
            '--description',
            type=check_description_len,
            help=FH(_("Description of the VPNEndpointRemoteSite")))

        parser.add_argument(
            '--peer-address',
            type=check_ipaddress_or_fqdn,
            help=FH(_("Peer gateway public IPv4/IPv6 address or FQDN")))

        parser.add_argument(
            '--peer-cidrs',
            type=check_cidr,
            action='append',
            help=FH(_("Peer subnet(s) in CIDR format. Repeat this option to \n"
                      "specify multiple CIDRs)")))

        parser.add_argument(
            '--vpncertificate-id',
            help=FH(_("ID of VPNCertificate\n"
                      "Only required for when authentication mode is 'cert'")))

        return parser

    @staticmethod
    def verify_arguments(attrs):
        common_verify_endpointremotesite_arguments(attrs)


class DeleteVPNEndpointRemoteSite(CommandResource):
    """Delete a given VPNEndpointRemoteSite"""
    resource = 'vpnendpointremotesites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNENDPOINTREMOTESITE',
            help=FH(_("ID or Name of VPNEndpointRemoteSite to delete")))

        return parser
