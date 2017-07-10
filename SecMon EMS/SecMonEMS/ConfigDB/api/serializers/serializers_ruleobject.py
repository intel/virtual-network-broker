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

"""Defines serializer for RuleObject relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api import attributes as attr
from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

class RuleObject(Resource):
    """Represents a RuleObject object."""
    relation_name = 'ruleobject'
    resource_name = 'RuleObject'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.classificationobject_id = kwargs.get('classificationobject_id')
        self.priority = kwargs.get('priority')
        self.truncate_to_size = kwargs.get('truncate_to_size')
        self.action = kwargs.get('action')


class RuleObjectSerializer(serializers.Serializer):
    """Serializer for RuleObject"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(required=True,
                               default=generate_uuid)

    name = serializers.CharField(max_length=attr.NAME_MAX_LEN,
                                 required=True)

    classificationobject_id = serializers.CharField(max_length=64,
                                                    required=True)

    priority = serializers.IntegerField(max_value=65535,
                                        min_value=1,
                                        required=True)

    truncate_to_size = serializers.IntegerField(max_value=65535,
                                                min_value=0,
                                                default=0,
                                                required=True)

    action = serializers.IntegerField(max_value=1,
                                      min_value=0,
                                      required=True)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for RuleObject record object

        Returns:
            None
        """
        return RuleObject.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, ruleobject, validated_data):
        """
        Args:
            ruleobject: Existing RuleObject record object
            validated_data: New values for RuleObject record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id'
        """
        try:
            record = RuleObject.serializer_update(self,
                                                  ruleobject,
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
        return RuleObject.serializer_valid(self, pk)
