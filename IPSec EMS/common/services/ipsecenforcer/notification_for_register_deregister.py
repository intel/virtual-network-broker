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

from services.api import storage
from services.api.serializers.utils_serializers import get_vpnendpoints_field
from services.api.serializers.vpn_choices import (
    RESOURCE_TO_RELATION_MAP, VPN_BIND_GROUP, VPN_BIND_LOCALSITE
)
from services.ipsecenforcer.send_notification import IPsecEnforcerNotify


class IPsecEnforcerRegistrationNotification(object):

    @classmethod
    def start(cls, **kwargs):
        """

        Args:
            **kwargs:
        """

        mapping_records = kwargs.get('mapping_records')

        for record in mapping_records:
            #
            # VPNEndpointGroup
            #
            group_record = storage.plugin.get_record(
                    RESOURCE_TO_RELATION_MAP['VPNEndpointGroup'],
                    record['endpoint_id'])

            if group_record and (record['endpoint_type'] == 'group'):
                for resource in VPN_BIND_GROUP:
                    relation = RESOURCE_TO_RELATION_MAP[resource]
                    vpn_bind_records = storage.plugin.get_records(relation)

                    for vpn_bind_record in vpn_bind_records:
                        cls.vpnbind_search(relation,
                                           vpn_bind_record,
                                           record['endpoint_id'])

            #
            # VPNEndpointLocalSite
            #
            group_record = storage.plugin.get_record(
                    RESOURCE_TO_RELATION_MAP['VPNEndpointLocalSite'],
                    record['endpoint_id'])

            if group_record and (record['endpoint_type'] == 'localsite'):
                for resource in VPN_BIND_LOCALSITE:
                    relation = RESOURCE_TO_RELATION_MAP[resource]
                    vpn_bind_records = storage.plugin.get_records(relation)

                    for vpn_bind_record in vpn_bind_records:
                        cls.vpnbind_search(relation,
                                           vpn_bind_record,
                                           record['endpoint_id'])

            #
            # VPNEndpointRemoteSite
            #
            group_record = storage.plugin.get_record(
                    RESOURCE_TO_RELATION_MAP['VPNEndpointRemoteSite'],
                    record['endpoint_id'])

            if group_record and (record['endpoint_type'] == 'remotesite'):
                for resource in VPN_BIND_LOCALSITE:
                    relation = RESOURCE_TO_RELATION_MAP[resource]
                    vpn_bind_records = storage.plugin.get_records(relation)

                    for vpn_bind_record in vpn_bind_records:
                        cls.vpnbind_search(relation,
                                           vpn_bind_record,
                                           record['endpoint_id'])

    @staticmethod
    def vpnbind_search(relation, vpnbind_record, vpnendpoint_id):
        """Search the

        Args:
            relation (str): Name if VPNEndpoint relation
            vpnbind_record (dict):  VPNBind Record
            vpnendpoint_id (str): id of VPNEndpoint
        """
        endpoint, peer_endpoint = get_vpnendpoints_field(relation)
        if vpnbind_record[endpoint] == vpnendpoint_id:
            IPsecEnforcerNotify.notify_ipsecenforcers_of_vpnendpoint(
                    vpnbind_record[peer_endpoint])
        elif vpnbind_record[peer_endpoint] == vpnendpoint_id:
            IPsecEnforcerNotify.notify_ipsecenforcers_of_vpnendpoint(
                    vpnbind_record[endpoint])
