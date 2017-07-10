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
from services.api.serializers.utils_serializers import(
    check_ikepolicy_id, check_ipsecpolicy_id,
    check_peer_vpnendpointremotesite_id, check_vpncertificate_exists,
    check_vpnendpointlocalsite_id, generate_uuid, CustomUUIDField
)
from services.api.serializers.vpn_choices import (
    BIND_AUTH_MODE, BIND_DPD_ACTION, BIND_INITIATOR, BIND_SITE_STATUS
)


class VPNBindLocalSiteToRemoteSite(Resource):
    """Represents a VPNBindLocalSiteToRemoteSite object."""
    resource_name = 'VPNBindLocalSiteToRemoteSite'
    primary_key = 'id'
    secondary_keys = ('name',)

    @staticmethod
    def resource_validation(resource_name, attrs):
        """Validate the request"""

        if attrs['auth_mode'] == 'cert':
            check_vpncertificate_exists(resource_name,
                                        attrs['id'])


class VPNBindLocalSiteToRemoteSiteSerializer(ConsulSerializer):
    """Serializer for VPNBindLocalSiteToRemoteSite

    This is applicable to both localsite-remotesite and
    remotesite-localsite bind.
    """
    consul_model = VPNBindLocalSiteToRemoteSite

    #
    # Validators for all the resource fields
    #

    id = CustomUUIDField(format='hex_verbose',
                         default=generate_uuid)

    name = serializers.CharField()

    description = serializers.CharField(required=False)

    vpnendpointlocalsite_id = CustomUUIDField(
        validators=[check_vpnendpointlocalsite_id])

    peer_vpnendpointremotesite_id = CustomUUIDField(validators=
        [check_peer_vpnendpointremotesite_id])

    admin_state_up = serializers.BooleanField(default=True)

    dpd_action = serializers.ChoiceField(choices=BIND_DPD_ACTION,
                                         default='hold')

    dpd_interval = serializers.IntegerField(max_value=None,
                                            min_value=1,
                                            default=30)

    dpd_timeout = serializers.IntegerField(max_value=None,
                                           min_value=1,
                                           default=120)

    auth_mode = serializers.ChoiceField(BIND_AUTH_MODE,
                                        default='psk')

    psk = serializers.CharField(allow_blank=False)

    initiator = serializers.ChoiceField(choices=BIND_INITIATOR,
                                        default='bi-directional')

    status = serializers.ChoiceField(choices=BIND_SITE_STATUS,
                                     default='PENDING_CREATE')

    ikepolicy_id = CustomUUIDField(format='hex_verbose',
                                   validators=[check_ikepolicy_id])

    ipsecpolicy_id = CustomUUIDField(format='hex_verbose',
                                     validators=[check_ipsecpolicy_id])

    def validate(self, attrs):
        if attrs['auth_mode'] == 'cert':
            attrs['psk'] = ''
        return attrs
