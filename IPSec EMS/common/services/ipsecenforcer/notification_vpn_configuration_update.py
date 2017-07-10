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

import itertools

from services.api import storage
from services.api.serializers.utils_serializers import get_vpnendpoints_field
from services.api.serializers.vpn_choices import (
    VPN_BIND, RESOURCE_DEPENDENCY_MAP,
    RESOURCE_TO_RELATION_MAP)
from services.ipsecenforcer.send_notification import IPsecEnforcerNotify


class IPsecConfigUpdateNotification(object):

    # Remove the below fields from VPN(IPsec) records as they are not
    # required for policy configuration at IPsecEnforcer
    unrequired_fields = ('name', 'description')

    @classmethod
    def record_update(cls, **kwargs):
        """Updation of record

        Args:
            **kwargs: resource name, original record before updation,
                record updates
        """
        resource = kwargs.get('resource')
        record = kwargs.get('record')
        record_update = kwargs.get('record_update')
        record_id = record['id']

        for field in cls.unrequired_fields:
            record_update.pop(field, None)
        if not record_update:
            return

        if resource not in VPN_BIND:
            cls._non_vpnbind_record_update(resource, record_id)
        else:
            cls._vpnbind_record_update_or_delete(resource,
                                                 record,
                                                 record_update)

    @classmethod
    def vpnbind_record_delete(cls, **kwargs):
        """Deletion of VPNBind record

        Args:
            **kwargs: resource name, original record before updation
        """
        resource = kwargs.get('resource')
        record = kwargs.get('record')

        relation = RESOURCE_TO_RELATION_MAP[resource]
        endpoint, peer_endpoint = get_vpnendpoints_field(relation)
        endpoint_id = record[endpoint]
        peer_endpoint_id = record[peer_endpoint]

        # Notify IPsecEnforcer(s) of both vpnendpoint and peer-vpnendpoint
        IPsecEnforcerNotify.vpnbind_endpoints_update(endpoint_id,
                                                     peer_endpoint_id)

    @staticmethod
    def _vpnbind_record_update_or_delete(resource, record, record_update):
        """Updation of VPNBind Record

        Args:
            resource (str):  name of the resource
            record (dict): original record before updation
            record_update (dict): record updates
        """
        relation = RESOURCE_TO_RELATION_MAP[resource]
        endpoint, peer_endpoint = get_vpnendpoints_field(relation)
        endpoint_id = record[endpoint]
        peer_endpoint_id = record[peer_endpoint]

        # Notify IPsecEnforcer(s) of both vpnendpoint and the peer
        # vpnendpoint
        IPsecEnforcerNotify.vpnbind_endpoints_update(endpoint_id,
                                                     peer_endpoint_id)

        # In case endpoint is being updated
        endpoint_id = record_update.pop(endpoint, None)
        if endpoint_id is not None:
            IPsecEnforcerNotify.notify_ipsecenforcers_of_vpnendpoint(
                    endpoint_id)

        endpoint_id = record_update.pop(peer_endpoint, None)
        if endpoint_id is not None:
            IPsecEnforcerNotify.notify_ipsecenforcers_of_vpnendpoint(
                    endpoint_id)

    @staticmethod
    def _non_vpnbind_record_update(resource, record_id):
        """Updation of a Non-VPNBind record

        Check all the VPNBind records to find if any record has
        reference to this Non-VPNBind Record. If a reference exists,
        then notify all the IPsecEnforcer(s) using the VPNBind record
        configurations.

        Args:
            resource (str): name of the resource
            record_id (str): id of the updated record(resource)
        """
        # Find the dependent VPNBind relations and their corresponding field
        # names in the relation
        relations = RESOURCE_DEPENDENCY_MAP[resource][0]
        fields = RESOURCE_DEPENDENCY_MAP[resource][1:]

        for resource, field in itertools.product(relations, fields):

            relation = RESOURCE_TO_RELATION_MAP[resource]
            # Fetch all records of the VPNBind relation
            records = storage.plugin.get_records(relation)
            for record in records:
                if record[field] == record_id:

                    endpoint, peer_endpoint = get_vpnendpoints_field(relation)
                    endpoint_id = record[endpoint]
                    peer_endpoint_id = record[peer_endpoint]

                    # Notify IPsecEnforcer(s) of both vpnendpoint and the peer
                    # vpnendpoint
                    IPsecEnforcerNotify.vpnbind_endpoints_update(
                            endpoint_id,
                            peer_endpoint_id)


