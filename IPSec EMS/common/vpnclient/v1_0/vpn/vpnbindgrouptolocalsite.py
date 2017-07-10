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
from vpnclient.v1_0.command_list import ListCommand
from vpnclient.v1_0.command_resource import CommandResource
from vpnclient.v1_0.vpn.utils_vpn import check_name_len

COMMAND_COLUMNS = [
    'id',
    'name',
    'description',
    'vpnendpointgroup_id',
    'peer_vpnendpointlocalsite_id',
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

HTTP_RESOURCE = 'vpnbindgrouptolocalsite'


class CreateVPNBindGroupToLocalSite(CommandResource):
    """Create an VPNBindGroupToLocalSite"""
    resource = 'vpnbindgrouptolocalsites'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            help="Name of the VPNBindGroupToLocalSite\n\n")

        parser.add_argument(
            '--description',
            default='',
            help="Description of the VPNBindGroupToLocalSite\n\n")

        parser.add_argument(
            '--vpnendpointgroup-id',
            required=True,
            help="ID of VPNEndpointGroup\n\n")

        parser.add_argument(
            '--peer-vpnendpointlocalsite-id',
            required=True,
            help="ID of Peer VPNEndpointLocalSite\n\n")

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
            help="Authentication mode for this connection,\n"
                 "Default: psk\n\n")

        parser.add_argument(
            '--psk',
            help="Pre-Shared Key string. Only valid if auth-mode is 'psk'\n\n")

        parser.add_argument(
            '--initiator',
            default='bi-directional',
            choices=['bi-directional', 'response-only'],
            help="Initiator state in lowercase, Default: bi-directional\n\n")

        parser.add_argument(
            '--ikepolicy-id',
            required=True,
            help="IKEPolicy id to be associated with this Bind record\n\n")

        parser.add_argument(
            '--ipsecpolicy-id',
            required=True,
            help="IPsecPolicy id to be associated with this Bind record\n\n")

        return parser


class ShowVPNBindGroupToLocalSite(CommandResource):
    """Show information of a given VPNBindGroupToLocalSite"""
    resource = 'vpnbindgrouptolocalsites'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNBINDGROUPTOLOCALSITE',
            help="ID or Name of VPNBindGroupToLocalSite to search\n\n")

        return parser


class ListVPNBindGroupToLocalSite(CommandResource):
    """List VPNBindGroupToLocalSites"""
    resource = 'vpnbindgrouptolocalsites'

    @staticmethod
    def add_known_arguments(parser):
        return ListCommand.add_args(parser)


class UpdateVPNBindGroupToLocalSite(CommandResource):
    """Update a given VPNBindGroupToLocalSite"""
    resource = 'vpnbindgrouptolocalsites'

    @staticmethod
    def add_known_arguments(parser):

        parser.add_argument(
            'id',
            metavar='VPNBINDGROUPTOLOCALSITE',
            help="ID or Name of VPNBindGroupToLocalSite to update\n\n")

        parser.add_argument(
            '--name',
            type=check_name_len,
            help="Name of the VPNBindGroupToLocalSite\n\n")

        parser.add_argument(
            '--description',
            help="Description of the VPNBindGroupToLocalSite\n\n")

        parser.add_argument(
            '--vpnendpointgroup-id',
            help="ID of VPNEndpointGroup\n\n")

        parser.add_argument(
            '--peer-vpnendpointlocalsite-id',
            help="ID of Peer VPNEndpointLocalSite\n\n")

        parser.add_argument(
            '--admin-state-up',
            choices=[True, False],
            type=bool,
            help="IKE Phase1 negotiation mode in lowercase\n\n")

        parser.add_argument(
            '--dpd-action',
            choices=['clear',
                     'disabled',
                     'hold',
                     'restart',
                     'restart-by-peer'],
            help="IPsec connection Dead Peer Detection(DPD) attribute "
                 "action\n\n")

        parser.add_argument(
            '--dpd-interval',
            type=int,
            help="IPsec connection Dead Peer Detection(DPD) attribute\n"
                 "interval. This should be a non negative integer. DPD\n"
                 "'interval' should be less than 'timeout' value.\n\n")

        parser.add_argument(
            '--dpd-timeout',
            type=int,
            help="IPsec connection Dead Peer Detection(DPD) attribute\n"
                 "timeout. This should be a non negative integer. DPD\n"
                 "'timeout' should be greater than 'interval' value.\n\n")

        parser.add_argument(
            '--auth-mode',
            choices=['psk', 'cert'],
            help="Authentication mode for this connection\n\n")

        parser.add_argument(
            '--psk',
            help="Pre-Shared Key string. Only valid if auth-mode is 'psk'\n\n")

        parser.add_argument(
            '--initiator',
            choices=['bi-directional', 'response-only'],
            help="Initiator state in lowercase\n\n")

        parser.add_argument(
            '--ikepolicy-id',
            help="IKEPolicy id to be associated with this Bind record\n\n")

        parser.add_argument(
            '--ipsecpolicy-id',
            help="IPsecPolicy id to be associated with this Bind record\n\n")

        return parser


class DeleteVPNBindGroupToLocalSite(CommandResource):
    """Delete a given VPNBindGroupToLocalSite"""
    resource = 'vpnbindgrouptolocalsites'

    @staticmethod
    def add_known_arguments(parser):
        parser.add_argument(
            'id',
            metavar='VPNBINDGROUPTOLOCALSITE',
            help="ID or Name of VPNBindGroupToLocalSite to delete\n\n")

        return parser


