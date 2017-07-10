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

"""Defines serializer for NetFlowConfig relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

class NetFlowConfig(Resource):
    """Represents a NetFlowConfig object."""
    relation_name = 'netflowconfig'
    resource_name = 'NetFlowConfig'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
        self.active_timeout = kwargs.get('active_timeout')
        self.scope_id = kwargs.get('scope_id')
        self.inactive_timeout = kwargs.get('inactive_timeout')
        self.refresh_rate = kwargs.get('refresh_rate')
        self.timeout_rate = kwargs.get('timeout_rate')
        self.maxflows = kwargs.get('maxflows')


class NetFlowConfigSerializer(serializers.Serializer):
    """Serializer for NetFlowConfig"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(default=generate_uuid,
                               required=True)

    scope_id = serializers.CharField(max_length=None,
                                     required=True)

    active_timeout = serializers.IntegerField(max_value=65535,
                                              min_value=0,
                                              required=True)
    inactive_timeout = serializers.IntegerField(max_value=65535,
                                                min_value=0,
                                                required=True)
    refresh_rate = serializers.IntegerField(max_value=65535,
                                            min_value=0,
                                            required=True)
    timeout_rate = serializers.IntegerField(max_value=65535,
                                            min_value=0,
                                            required=True)
    maxflows = serializers.IntegerField(max_value=65535,
                                        min_value=0,
                                        required=True)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for NetFlowConfig record object

        Returns:
            None
        """
        return NetFlowConfig.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, netflowconfig, validated_data):
        """
        Args:
            netflowconfig: Existing NetFlowConfig record object
            validated_data: New values for NetFlowConfig record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id'
        """
        try:
            record = NetFlowConfig.serializer_update(self,
                                                     netflowconfig,
                                                     validated_data)
            return record
        except (IDUpdateNotPermitted, TypeError):
            raise

    def valid(self, pk):
        """checks if a serializer is valid or not

        Args:
            pk: primary key value

        Returns:
            (bool)
        """
        return NetFlowConfig.serializer_valid(self, pk)
