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
from services.api.serializers.utils_serializers import generate_uuid, CustomUUIDField


class VPNCACertificate(Resource):
    """Represents a VPNCACertificate object"""
    resource_name = 'VPNCACertificate'
    primary_key = 'id'
    secondary_keys = ('name',)

    def __init__(self, **kwargs):
        # Resource.__init__(self)
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')

        if isinstance(kwargs.get('ca_certificate'), basestring):
            self.ca_certificate = kwargs.get('ca_certificate')
        else:
            self.ca_certificate = kwargs.get('ca_certificate').read()


class VPNCACertificateSerializer(ConsulSerializer):
    """Serializer for VPNCACertificate"""
    consul_model = VPNCACertificate

    #
    # Validators for all the resource fields
    #

    id = CustomUUIDField(format='hex_verbose',
                         default=generate_uuid)

    name = serializers.CharField()

    description = serializers.CharField(required=False)

    ca_certificate = serializers.FileField()