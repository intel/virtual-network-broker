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
    check_cidrs, check_vpncertificate_id, generate_uuid,
    remove_duplicates_from_list, CustomUUIDField
)


class VPNEndpointLocalSite(Resource):
    """Represents an VPNEndpointLocalSite object"""
    resource_name = 'VPNEndpointLocalSite'
    primary_key = 'id'
    secondary_keys = ('name',)


class VPNEndpointLocalSiteSerializer(ConsulSerializer):
    """Serializer for VPNEndpointLocalSite"""
    consul_model = VPNEndpointLocalSite

    #
    # Validators for all the resource fields
    #

    id = CustomUUIDField(format='hex_verbose',
                         default=generate_uuid)

    name = serializers.CharField()

    description = serializers.CharField(required=False)

    cidrs = serializers.ListField(child=serializers.CharField(),
                                  validators=[check_cidrs])

    vpncertificate_id = CustomUUIDField(format='hex_verbose',
                                        validators=[check_vpncertificate_id],
                                        required=False,
                                        default='')

    @staticmethod
    def validate_cidrs(value):
        return remove_duplicates_from_list(value)
