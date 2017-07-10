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

"""Defines serializer for Scope relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api import attributes as attr
from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

PLUGINSTATUS = (
    ('enable', 'enable'),
    ('disable', 'disable'),
)


class Scope(Resource):
    """Represents a Scope object."""
    relation_name = 'scope'
    resource_name = 'Scope'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.sflowstatus = kwargs.get('sflowstatus')
        self.netflowstatus = kwargs.get('netflowstatus')
        self.rawforwardstatus = kwargs.get('rawforwardstatus')


class ScopeSerializer(serializers.Serializer):
    """Serializer for Scope"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.

    id = serializers.CharField(required=True,
                               default=generate_uuid)

    name = serializers.CharField(max_length=attr.NAME_MAX_LEN,
                                 required=True)

    sflowstatus = serializers.ChoiceField(choices=PLUGINSTATUS,
                                          default='disable')

    netflowstatus = serializers.ChoiceField(choices=PLUGINSTATUS,
                                            default='disable')

    rawforwardstatus = serializers.ChoiceField(choices=PLUGINSTATUS,
                                               default='disable')

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for Scope record object

        Returns:
            None
         """
        return Scope.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, scope, validated_data):
        """
        Args:
            scope: Existing Collector record object
            validated_data: New values for Collector record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id'
        """
        try:
            record = Scope.serializer_update(self,
                                             scope,
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
        return Scope.serializer_valid(self, pk)
