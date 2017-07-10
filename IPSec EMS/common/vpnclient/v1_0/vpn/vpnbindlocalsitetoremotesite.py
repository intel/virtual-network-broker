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
from vpnclient.v1_0.vpn.utils_vpn import check_name_len

_COMMAND_COLUMNS = [
    'id',
    'name',
    'description',
    'vpnendpointlocalsite_id',
    'peer_vpnendpointremotesite_id',
    'admin_state_up',
    'dpd_action',
    'dpd_interval',
    'dpd_timeout',
    'auth_mode',
    'psk',
    'initiator',
    'ikepolicy_id',
    'ipsecpolicy_id',
]

_HTTP_RESOURCE = 'vpnbindlocalsitetoremotesite'


class CreateVPNBindLocalSiteToRemoteSite(CommandResource):
    """Create an VPNBindLocalSiteToRemoteSite"""
    resource = 'vpnbindlocalsitetoremotesites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            help="Name of the VPNBindLocalSiteToRemoteSite\n\n")

        parser.add_argument(
            '--description',
            default='',
            help="Description of the VPNBindLocalSiteToRemoteSite\n\n")

        parser.add_argument(
            '--vpnendpointlocalsite-id',
            required=True,
            help="ID of VPNEndpointLocalSite\n\n")

        parser.add_argument(
            '--peer-vpnendpointremotesite-id',
            required=True,
            help="ID of Peer VPNEndpointRemoteSite\n\n")

        parser.add_argument(
            '--admin-state-up',
            default=True,
            choices=[True, False],
            type=bool,
            help="Administrative state of the IPSec connection, Default: True"
                 "\n\n")

        parser.add_argument(
            '--dpd-action',
            default='hold',
            choices=['clear',
                     'disabled',
                     'hold',
                     'restart',
                     'restart-by-peer'],
            help="IPsec connection Dead Peer Detection(DPD) attribute action\n"
                 "Default: hold\n\n")

        parser.add_argument(
            '--dpd-interval',
            type=int,
            default='30',
            help="IPsec connection Dead Peer Detection(DPD) attribute\n"
                 "interval. This should be a non negative integer. DPD\n"
                 "'interval' should be less than 'timeout' value.\n"
                 "Default: 30\n\n")

        parser.add_argument(
            '--dpd-timeout',
            type=int,
            default='120',
            help="IPsec connection Dead Peer Detection(DPD) attribute\n"
                 "timeout. This should be a non negative integer. DPD\n"
                 "'timeout' should be greater than 'interval' value.\n"
                 "Default: 120\n\n")

        parser.add_argument(
            '--auth-mode',
            default='psk',
            choices=['psk', 'cert'],
            help=FH(_("Authentication mode for this connection,\n"
                      "Default: psk")))

        parser.add_argument(
            '--psk',
            help=FH(_("Pre-Shared Key string. Only valid if auth-mode is "
                      "'psk'")))

        parser.add_argument(
            '--initiator',
            default='bi-directional',
            choices=['bi-directional', 'response-only'],
            help=FH(_("Initiator state in lowercase, Default: bi-directional")))

        parser.add_argument(
            '--ikepolicy-id',
            required=True,
            help=FH(_("IKEPolicy id to be associated with this Bind record")))

        parser.add_argument(
            '--ipsecpolicy-id',
            required=True,
            help=FH(_("IPsecPolicy id to be associated with this Bind record")))

        return parser


class ShowVPNBindLocalSiteToRemoteSite(CommandResource):
    """Show information of a given VPNBindLocalSiteToRemoteSite"""
    resource = 'vpnbindlocalsitetoremotesites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNBINDLOCALSITETOREMOTESITE',
            help=FH(_("ID or Name of VPNBindLocalSiteToRemoteSite to search")))

        return parser


class ListVPNBindLocalSiteToRemoteSite(CommandResource):
    """List VPNBindLocalSiteToRemoteSites"""
    resource = 'vpnbindlocalsitetoremotesites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateVPNBindLocalSiteToRemoteSite(CommandResource):
    """Update a given VPNBindLocalSiteToRemoteSite"""
    resource = 'vpnbindlocalsitetoremotesites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNBINDLOCALSITETOREMOTESITE',
            help=FH(_("ID or Name of VPNBindLocalSiteToLocalSite to update")))

        parser.add_argument(
            'name',
            type=check_name_len,
            help=FH(_("Name of the VPNBindLocalSiteToRemoteSite")))

        parser.add_argument(
            '--description',
            help=FH(_("Description of the VPNBindLocalSiteToRemoteSite")))

        parser.add_argument(
            '--vpnendpointlocalsite-id',
            help=FH(_("ID of VPNEndpointLocalSite")))

        parser.add_argument(
            '--peer-vpnendpointremotesite-id',
            help=FH(_("ID of Peer VPNEndpointRemoteSite")))

        parser.add_argument(
            '--admin-state-up',
            choices=[True, False],
            type=bool,
            help=FH(_("IKE Phase1 negotiation mode in lowercase")))

        parser.add_argument(
            '--dpd-action',
            choices=['clear',
                     'disabled',
                     'hold',
                     'restart',
                     'restart-by-peer'],
            help=FH(_("IPsec connection Dead Peer Detection(DPD) attribute "
                      "action")))

        parser.add_argument(
            '--dpd-interval',
            type=int,
            help=FH(_("IPsec connection Dead Peer Detection(DPD) attribute \n"
                      "interval. This should be a non negative integer. DPD \n"
                      "'interval' should be less than 'timeout' value.")))

        parser.add_argument(
            '--dpd-timeout',
            type=int,
            help=FH(_("IPsec connection Dead Peer Detection(DPD) attribute \n"
                      "timeout. This should be a non negative integer. DPD \n"
                      "'timeout' should be greater than 'interval' value.")))

        parser.add_argument(
            '--auth-mode',
            choices=['psk', 'cert'],
            help=FH(_("Authentication mode for this connection")))

        parser.add_argument(
            '--psk',
            help=FH(_("Pre-Shared Key string. Only valid if auth-mode is "
                      "'psk'")))

        parser.add_argument(
            '--initiator',
            choices=['bi-directional', 'response-only'],
            help=FH(_("Initiator state in lowercase")))

        parser.add_argument(
            '--ikepolicy-id',
            help=FH(_("IKEPolicy id to be associated with this Bind record")))

        parser.add_argument(
            '--ipsecpolicy-id',
            help=FH(_("IPsecPolicy id to be associated with this Bind record")))

        return parser


class DeleteVPNBindLocalSiteToRemoteSite(CommandResource):
    """Delete a given VPNBindLocalSiteToRemoteSite"""
    resource = 'vpnbindlocalsitetoremotesites'
    cmd_columns = _COMMAND_COLUMNS
    http_resource = _HTTP_RESOURCE

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNBINDLOCALSITETOREMOTESITE',
            help=FH(_("ID or Name of VPNBindLocalSiteToRemoteSite to delete")))

        return parser
