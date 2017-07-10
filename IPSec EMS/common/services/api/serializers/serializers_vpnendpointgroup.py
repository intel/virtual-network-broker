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
    check_vpncertificate_id, generate_uuid, CustomUUIDField
)


class VPNEndpointGroup(Resource):
    """Represents an VPNEndpointGroup object"""
    resource_name = 'VPNEndpointGroup'
    primary_key = 'id'
    secondary_keys = ('name',)


class VPNEndpointGroupSerializer(ConsulSerializer):
    """Serializer for VPNEndpointGroup"""
    consul_model = VPNEndpointGroup

    #
    # Validators for all the resource fields
    #

    id = CustomUUIDField(format='hex_verbose',
                         default=generate_uuid)

    name = serializers.CharField()

    description = serializers.CharField(required=False)

    vpncertificate_id = CustomUUIDField(format='hex_verbose',
                                        validators=[check_vpncertificate_id],
                                        required=False,
                                        default='')
