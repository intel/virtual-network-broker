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

import logging
from itertools import izip_longest

from django.utils.translation import ugettext as _
from rest_framework import serializers

from services.api import storage
from services.api.serializers.resource import Resource, ConsulSerializer
from services.api.serializers.utils_serializers import (
    CustomUUIDField, generate_uuid
)
from services.ipsecenforcer.register_deregister import IPsecEnforcerInfo

LOG = logging.getLogger(__name__)


class IPsecEnforcerRegistration(Resource):
    """Represents a IPsecEnforcerRegistration object"""
    resource_name = 'IPsecEnforcerRegistration'
    primary_key = 'id'

    def save(self):
        """Write the record in the storage backend

        Returns:
            self (Resource): Return the object itself

        Raises:
            TypeError: When error storing the resource in backend
        """
        try:
            IPsecEnforcerInfo().register_ipsecenforcer(self)
            return self
        except TypeError:
            LOG.error(_("Error in storing data for %s with id %s" %
                        (self.resource_name, self.id)))
            raise
        finally:
            IPsecEnforcerInfo().delete_ipsecenforcer_to_vpnendpoint_map(
                    self.id,
                    temp=True)

    def update(self):
        pass

    def delete(self):
        IPsecEnforcerInfo().deregister_ipsecenforcer(self)

    def all(self):
        pass

    def get_name(self):
        pass


class IPsecEnforcerRegistrationSerializer(ConsulSerializer):
    """Serializer for IPsecEnforcerRegistration"""
    consul_model = IPsecEnforcerRegistration

    # IPsecEnforcerRegistration Attributes' Choices
    _VPN_ENDPOINT_TYPE = (
        'group',
        'localsite',
    )

    # Validators for all the record fields

    # 'id' is a UUID field which is auto-generated while creating a new
    #  record
    id = CustomUUIDField(format='hex_verbose',
                         default=generate_uuid)

    description = serializers.CharField(allow_blank=True,
                                        default='')

    endpoint_name = serializers.ListField(child=serializers.CharField())

    endpoint_type = serializers.ListField(
        child=serializers.ChoiceField(choices=_VPN_ENDPOINT_TYPE))

    instance_id = serializers.CharField(allow_blank=True)

    # FQDN of VPN Tunnel Interface
    fqdn_tunnel = serializers.CharField()

    # FQDN of IPsec EMS Interface
    fqdn = serializers.CharField()

    macaddress = serializers.CharField(max_length=255,
                                       allow_blank=True)

    def validate(self, attrs):
        """Check that the endpoint_name is valid"""
        endpoint_name = attrs['endpoint_name']
        endpoint_type = attrs['endpoint_type']

        if len(endpoint_name) != len(set(endpoint_name)):
            raise serializers.ValidationError(_("Duplicates are not allowed in "
                                                "the list of endpoint_name"))

        if len(endpoint_name) != len(endpoint_type):
            raise serializers.ValidationError(_("Number of entries in the list "
                                                "of endpoint_type and "
                                                "endpoint_name should be same"))

        for endpoint_name, endpoint_type in izip_longest(endpoint_name,
                                                         endpoint_type):
            if endpoint_type == 'group':
                record = storage.plugin.get_records_by_secondary_index(
                                'vpnendpointgroups',
                                'name',
                                endpoint_name)
            elif endpoint_type == 'localsite':
                record = storage.plugin.get_records_by_secondary_index(
                                'vpnendpointlocalsites',
                                'name',
                                endpoint_name)
            elif endpoint_type == 'remotesite':
                record = storage.plugin.get_records_by_secondary_index(
                                'vpnendpointremotesites',
                                'name',
                                endpoint_name)

            if (record is None) or (not record):
                raise serializers.ValidationError(("endpoint_name {0} is not "
                                                   "a valid endpoint_type "
                                                   "{1}").format(endpoint_name,
                                                                 endpoint_type))
            else:
                IPsecEnforcerInfo().put_ipsecenforcer_to_vpnendpoint_map(
                        attrs['id'],
                        {
                            'endpoint_id': record[0]['id'],
                            'endpoint_type': endpoint_type
                        },
                        temp=True)

        return attrs
