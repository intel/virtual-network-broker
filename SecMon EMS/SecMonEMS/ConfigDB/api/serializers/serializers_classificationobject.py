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

"""Defines serializer for ClassificationObject relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api import attributes as attr
from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

LOG = logging.getLogger(__name__)


class ClassificationObject(Resource):
    """Represents a ClassificationObject object."""
    relation_name = 'classificationobject'
    resource_name = 'ClassificationObject'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.src_ip = kwargs.get('src_ip')
        self.src_mac = kwargs.get('src_mac')
        self.src_ip_subnet = kwargs.get('src_ip_subnet')
        self.minimum_src_port = kwargs.get('minimum_src_port')
        self.maximum_src_port = kwargs.get('maximum_src_port')
        self.dst_ip = kwargs.get('dst_ip')
        self.dst_mac = kwargs.get('dst_mac')
        self.dst_ip_subnet = kwargs.get('dst_ip_subnet')
        self.minimum_dst_port = kwargs.get('minimum_dst_port')
        self.maximum_dst_port = kwargs.get('maximum_dst_port')
        self.protocol = kwargs.get('protocol')


class ClassificationObjectSerializer(serializers.Serializer):
    """Serializer for ClassificationObject"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(required=True,
                               default=generate_uuid)

    name = serializers.CharField(max_length=attr.NAME_MAX_LEN,
                                 required=True)

    src_ip = serializers.CharField(max_length=24,
                                   required=True)

    src_mac = serializers.CharField(max_length=24,
                                    required=False)

    src_ip_subnet = serializers.IntegerField(max_value=32,
                                             required=True)

    minimum_src_port = serializers.IntegerField(max_value=65535,
                                                min_value=1,
                                                required=False)

    maximum_src_port = serializers.IntegerField(max_value=65535,
                                                min_value=1,
                                                required=False)

    dst_ip = serializers.CharField(max_length=24,
                                   required=True)

    dst_mac = serializers.CharField(max_length=24,
                                    required=False)

    dst_ip_subnet = serializers.IntegerField(max_value=32,
                                             required=True)

    minimum_dst_port = serializers.IntegerField(max_value=65525,
                                                min_value=1,
                                                required=False)

    maximum_dst_port = serializers.IntegerField(max_value=65535,
                                                min_value=1,
                                                required=False)

    protocol = serializers.IntegerField(max_value=65535,
                                        min_value=0,
                                        required=True)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for ClassificationObject record object

        Returns:
            None
         """
        return ClassificationObject.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, classificationobject, validated_data):
        """
        Args:
            classificationobject: Existing ClassificationObject record object
            validated_data: New values for ClassificationObject record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id'
        """
        try:
            record = ClassificationObject.serializer_update(
                                                       self,
                                                       classificationobject,
                                                       validated_data)
            return record
        except (IDUpdateNotPermitted, TypeError):
            raise

    # Overwrite Serializer .is_valid() method
    def valid(self, pk):
        """
        Args:
            pk: primary key value

        Returns:
            (bool)
        """
        return ClassificationObject.serializer_valid(self, pk)
