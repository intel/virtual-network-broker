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

"""Defines serializer for Notification relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api import attributes as attr
from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

OPERATION = (
    ('POST', 'POST'),
    ('PUT','PUT'),
    ('DELETE','DELETE'),
    ('FLUSH','FLUSH')
)


class Notification(Resource):
    """Represents a Notification object."""
    relation_name = 'notification'
    resource_name = 'Notification'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
        self.table_name = kwargs.get('table_name')
        self.row_id = kwargs.get('row_id')
        self.operation = kwargs.get('operation')
        self.row_data = kwargs.get('row_data')


class NotificationSerializer(serializers.Serializer):
    """Serializer for Notification"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(required=True,
                               default=generate_uuid)

    table_name = serializers.CharField(max_length=attr.NAME_MAX_LEN,
                                       required=True)

    row_id = serializers.CharField(max_length=None,
                                   required=True)

    row_data = serializers.CharField(max_length=None,
                                     required=False)

    operation = serializers.ChoiceField(choices=OPERATION,
                                        required=True)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for Notification record object

        Returns:
            None
         """
        return Notification.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, notification, validated_data):
        """
        Args:
            notification: Existing Notification record object
            validated_data: New values for Notification record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id'
        """
        try:
            record = Notification.serializer_update(self,
                                                    notification,
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
        return Notification.serializer_valid(self, pk)
