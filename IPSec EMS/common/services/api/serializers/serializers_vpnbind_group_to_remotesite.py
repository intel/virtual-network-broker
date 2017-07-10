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


from rest_framework import serializers

from services.api.serializers.resource import Resource, ConsulSerializer
from services.api.serializers.utils_serializers import (
    check_ikepolicy_id, check_ipsecpolicy_id,
    check_peer_vpnendpointremotesite_id, check_vpncertificate_exists,
    check_vpnendpointgroup_id, generate_uuid, CustomUUIDField
)
from services.api.serializers.vpn_choices import (
    BIND_AUTH_MODE, BIND_DPD_ACTION, BIND_INITIATOR
)


class VPNBindGroupToRemoteSite(Resource):
    """Represents a VPNBindGroupToRemoteSite object

    This is applicable to both group-remotesite and remotesite-group bind.
    """
    resource_name = 'VPNBindGroupToRemoteSite'
    primary_key = 'id'
    secondary_keys = ('name',)

    @staticmethod
    def resource_validation(resource_name, attrs):
        """Validate the request"""

        if attrs['auth_mode'] == 'cert':
            check_vpncertificate_exists(resource_name,
                                        attrs['id'])


class VPNBindGroupToRemoteSiteSerializer(ConsulSerializer):
    """Serializer for VPNBindGroupToRemoteSite"""
    consul_model = VPNBindGroupToRemoteSite

    #
    # Validators for all the resource fields
    #

    id = CustomUUIDField(format='hex_verbose',
                         default=generate_uuid)

    name = serializers.CharField()

    description = serializers.CharField(required=False)

    vpnendpointgroup_id = CustomUUIDField(
        format='hex_verbose',
        validators=[check_vpnendpointgroup_id])

    peer_vpnremotesite_id = CustomUUIDField(
        format='hex_verbose',
        validators=[check_peer_vpnendpointremotesite_id])

    admin_state_up = serializers.BooleanField(default=True)

    dpd_action = serializers.ChoiceField(choices=BIND_DPD_ACTION,
                                         default='hold')

    dpd_interval = serializers.IntegerField(max_value=None,
                                            min_value=1,
                                            default=30)

    dpd_timeout = serializers.IntegerField(max_value=None,
                                           min_value=1,
                                           default=120)

    auth_mode = serializers.ChoiceField(choices=BIND_AUTH_MODE,
                                        default='psk')

    psk = serializers.CharField(allow_blank=False)

    initiator = serializers.ChoiceField(choices=BIND_INITIATOR,
                                        default='bi-directional')

    ikepolicy_id = CustomUUIDField(format='hex_verbose',
                                   validators=[check_ikepolicy_id])

    ipsecpolicy_id = CustomUUIDField(format='hex_verbose',
                                     validators=[check_ipsecpolicy_id])

    def validate(self, attrs):
        if attrs['auth_mode'] == 'cert':
            attrs['psk'] = ''
        return attrs
