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

"""Defines serializer for SecmonDetails relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api import attributes as attr
from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

class SecmonDetails(Resource):
    """Represents a SecmonDetails object."""
    relation_name = 'secmondetails'
    resource_name = 'SecmonDetails'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
        self.scope_name = kwargs.get('scope_name')
        self.ip_address = kwargs.get('ip_address')
        self.mac_address = kwargs.get('mac_address')
        self.port = kwargs.get('port')


class SecmonDetailsSerializer(serializers.Serializer):
    """Serializer for SecmonDetails"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(required=True,
                               default=generate_uuid)

    scope_name = serializers.CharField(max_length=attr.NAME_MAX_LEN,
                                       required=True)

    ip_address = serializers.CharField(max_length=24,
                                       required=True)

    mac_address = serializers.CharField(max_length=24,
                                        required=True)

    port = serializers.IntegerField(max_value=65535,
                                    min_value=1,
                                    required=True)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for SecmonDetails record object

        Returns:
            None
         """
        return SecmonDetails.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, secmondetails, validated_data):
        """
        Args:
            secmondetails: Existing Collector record object
            validated_data: New values for Collector record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id'
        """
        try:
            record = SecmonDetails.serializer_update(self,
                                                     secmondetails,
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
        return SecmonDetails.serializer_valid(self, pk)
