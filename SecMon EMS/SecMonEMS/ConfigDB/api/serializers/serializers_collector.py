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

"""Defines serializer for Collector relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api import attributes as attr
from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

PLUGINNAME = (
    ('netflow', 'netflow'),
    ('sflow', 'sflow'),
    ('rawforward', 'rawforward'),
)

ENCAPPROTO = (
    ('UDP', 'UDP'),
    ('SFLOW', 'SFLOW'),
)


class Collector(Resource):
    """Represents a Collector object."""
    relation_name = 'collector'
    resource_name = 'Collector'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.ip_address = kwargs.get('ip_address')
        self.udp_port = kwargs.get('udp_port')
        self.col_type = kwargs.get('col_type')
        self.encapsulation_protocol = kwargs.get('encapsulation_protocol')
#        self.association = kwargs.get('association')


class CollectorSerializer(serializers.Serializer):
    """Serializer for Collector"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(required=True,
                               default=generate_uuid)

    name = serializers.CharField(max_length=attr.NAME_MAX_LEN,
                                 required=True)

    ip_address = serializers.CharField(max_length=24,
                                       required=True)

    udp_port = serializers.IntegerField(max_value=65535,
                                        min_value=1,
                                        required=True)

    col_type = serializers.ChoiceField(choices=PLUGINNAME,
                                       required=True)

    encapsulation_protocol = serializers.ChoiceField(choices=ENCAPPROTO,
                                                     default='',
                                                     required=False)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for Collector record object

        Returns:
            None
         """
        return Collector.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, collector, validated_data):
        """
        Args:
            collector: Existing Collector record object
            validated_data: New values for Collector record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id'
        """
        try:
            record = Collector.serializer_update(self,
                                                 collector,
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
        return Collector.serializer_valid(self, pk)
