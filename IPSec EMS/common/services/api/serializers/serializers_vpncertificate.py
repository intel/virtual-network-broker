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
    check_vpncacertificate_id, generate_uuid, CustomUUIDField
)


class VPNCertificate(Resource):
    """Represents a VPNCertificate object"""
    resource_name = 'VPNCertificate'
    primary_key = 'id'
    secondary_keys = ('name',)

    def __init__(self, **kwargs):
        # Resource.__init__(self)
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')

        if isinstance(kwargs.get('certificate'), basestring):
            self.certificate = kwargs.get('certificate')
        else:
            self.certificate = kwargs.get('certificate').read()

        if isinstance(kwargs.get('key'), basestring):
            self.key = kwargs.get('key')
        else:
            self.key = kwargs.get('key').read()

        self.right_id = kwargs.get('right_id')
        self.vpncacertificate_id = kwargs.get('vpncacertificate_id')


class VPNCertificateSerializer(ConsulSerializer):
    """Serializer for VPNCertificate"""
    consul_model = VPNCertificate

    #
    # Validators for all the resource fields
    #

    id = CustomUUIDField(format='hex_verbose',
                         default=generate_uuid)

    name = serializers.CharField()

    description = serializers.CharField(required=False)

    certificate = serializers.FileField()

    # TODO: Private Key is stored in plain text
    key = serializers.FileField()

    right_id = serializers.CharField(allow_blank=False)

    vpncacertificate_id = CustomUUIDField(format='hex_verbose',
                                          validators=[check_vpncacertificate_id])
