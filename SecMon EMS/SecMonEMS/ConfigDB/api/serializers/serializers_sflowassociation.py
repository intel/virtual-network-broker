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

"""Defines serializer for SflowAssociation relation.
"""

import logging

from rest_framework import serializers

from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

DIRECTIONCHOICES = (
    ('INGRESS', 'INGRESS'),
    ('EGRESS', 'EGRESS'),
    ('BOTH', 'BOTH'),
)


class SflowAssociation(Resource):
    """Represents a SflowAssociation object."""
    relation_name = 'sflowassociation'
    resource_name = 'SflowAssociation'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        self.id = kwargs.get('id')
#        self.originator_vm_id = kwargs.get('originator_vm_id')
        self.collector_id = kwargs.get('collector_id')
        self.direction = kwargs.get('direction')
        self.policy_id = kwargs.get('policy_id')
        self.scope_id = kwargs.get('scope_id')


class SflowAssociationSerializer(serializers.Serializer):
    """Serializer for SflowAssociation"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(default=generate_uuid,
                               required=True)

#    originator_vm_id = serializers.CharField(max_length=None,
#                                             required=True)

    collector_id = serializers.CharField(max_length=None,
                                         required=True)

    direction = serializers.ChoiceField(choices=DIRECTIONCHOICES,
                                        required=True)

    policy_id = serializers.CharField(max_length=None,
                                      required=True)

    scope_id = serializers.CharField(max_length=None,
                                     required=True)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for SflowAssociation record object

        Returns:
            None
         """
        return SflowAssociation.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, sflowassociation, validated_data):
        """
        Args:
            sflowassociation: Existing SflowAssociation record object
            validated_data: New values for SflowAssociation record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id'
        """
        try:
            record = SflowAssociation.serializer_update(self,
                                                        sflowassociation,
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
        return SflowAssociation.serializer_valid(self, pk)
