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

"""Defines serializer for Policy relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api import attributes as attr
from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

class Policy(Resource):
    """Represents a Policy object."""
    relation_name = 'policy'
    resource_name = 'Policy'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.ruleobject_id = kwargs.get('ruleobject_id')


class PolicySerializer(serializers.Serializer):
    """Serializer for Policy"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(default=generate_uuid,
                               required=True)

    name = serializers.CharField(max_length=attr.NAME_MAX_LEN,
                                 required=True)

    ruleobject_id = serializers.CharField(max_length=None,
                                          required=True)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for Policy record object

        Returns:
            None
         """
        return Policy.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, policy, validated_data):
        """
        Args:
            policy: Existing Association record object
            validated_data: New values for Policy record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id' of policy
        """
        try:
            record = Policy.serializer_update(self,
                                              policy,
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
        return Policy.serializer_valid(self, pk)
