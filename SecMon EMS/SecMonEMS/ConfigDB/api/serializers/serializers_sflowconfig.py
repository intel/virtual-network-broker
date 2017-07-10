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

"""Defines serializer for SflowConfig relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

class SflowConfig(Resource):
    """Represents a SflowConfig object."""
    relation_name = 'sflowconfig'
    resource_name = 'SflowConfig'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
        self.scope_id = kwargs.get('scope_id')
        self.agent_ip = kwargs.get('agent_ip')
        self.agent_subid = kwargs.get('agent_subid')
        self.sampling_rate = kwargs.get('sampling_rate')
        self.truncate_to_size = kwargs.get('truncate_to_size')


class SflowConfigSerializer(serializers.Serializer):
    """Serializer for SflowConfig"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(required=True,
                               default=generate_uuid)

    scope_id = serializers.CharField(max_length=None,
                                     required=True)

    agent_ip = serializers.CharField(max_length=24,
                                     required=True)

    agent_subid = serializers.IntegerField(max_value=None,
                                           min_value=0,
                                           required=True)

    sampling_rate = serializers.IntegerField(max_value=None,
                                             required=True)

    truncate_to_size = serializers.IntegerField(max_value=65535,
                                                min_value=0,
                                                required=False)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for sflowconfig record object

        Returns:
            None
         """
        return SflowConfig.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, sflowconfig, validated_data):
        """
        Args:
            sflowconfig: Existing Collector record object
            validated_data: New values for SflowConfig record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id'
        """
        try:
            record = SflowConfig.serializer_update(self,
                                                   sflowconfig,
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
        return SflowConfig.serializer_valid(self, pk)
