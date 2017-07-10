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

"""Defines serializer for NetFlowMonitor relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

class NetFlowMonitor(Resource):
    """Represents a NetFlowMonitor object."""
    relation_name = 'netflowmonitor'
    resource_name = 'NetFlowMonitor'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
        self.scope_id = kwargs.get('scope_id')
        self.match_fields = kwargs.get('match_fields')
        self.collect_fields = kwargs.get('collect_fields')


class NetFlowMonitorSerializer(serializers.Serializer):
    """Serializer for NetFlowMonitor"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(required=True,
                               default=generate_uuid)

    scope_id = serializers.CharField(max_length=None,
                                     required=True)

    match_fields = serializers.CharField(max_length=None,
                                         required=True)

    collect_fields = serializers.CharField(max_length=None,
                                           required=True)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for NetFlowMonitor record object

        Returns:
            None
        """
        return NetFlowMonitor.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, netflowmonitor, validated_data):
        """
        Args:
            netflowmonitor: Existing NetFlowMonitor record object
            validated_data: New values for NetFlowMonitor record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id'
        """
        try:
            record = NetFlowMonitor.serializer_update(self,
                                                      netflowmonitor,
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
        return NetFlowMonitor.serializer_valid(self, pk)
