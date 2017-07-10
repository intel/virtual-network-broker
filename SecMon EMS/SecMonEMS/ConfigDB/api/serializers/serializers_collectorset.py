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

"""Defines serializer for CollectoSet relation.
"""

import logging
import json, ast
from rest_framework import serializers
import string
from ConfigDB.api import attributes as attr
from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.serializers.resource import Resource
from ConfigDB.api.utils import generate_uuid

PLUGINNAME = (
    ('netflow', 'netflow'),
    ('sflow', 'sflow'),
    ('rawforward', 'rawforward'),
)


class CollectorSet(Resource):
    """Represents a CollectorSet object."""
    relation_name = 'collectorset'
    resource_name = 'CollectorSet'

    def __init__(self, **kwargs):
        Resource.__init__(self)
        print("inside collectorset class:", kwargs)
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.collector_ids = kwargs.get('collector_ids')
        self.col_type = kwargs.get('col_type')
        self.lb_algo = kwargs.get('lb_algo')


class CollectorSetSerializer(serializers.Serializer):
    """Serializer for CollectorSet"""

    # Validators for all the record fields
    # 'id' is a UUID field which is auto-generated while creating a new record.
    id = serializers.CharField(required=True,
                               default=generate_uuid)

    name = serializers.CharField(max_length=attr.NAME_MAX_LEN,
                                 required=True)

    collector_ids = serializers.CharField(max_length=None,
                                          required=True)

    col_type = serializers.ChoiceField(choices=PLUGINNAME,
                                       required=True)

    lb_algo = serializers.IntegerField(max_value=2,
                                       min_value=0,
                                       required=True)

    # Overwrite Serializer .create() method
    def create(self, validated_data):
        """
        Args:
            validated_data: New values for CollectorSet record object

        Returns:
            None
         """
#        print("validated data in create:", validated_data)
        collector_ids_str = str(validated_data['collector_ids'])
        collector_ids_str = collector_ids_str.replace("{u'", "{'")
        collector_ids_str = collector_ids_str.replace(": u'", ": '")
        collector_ids_str = collector_ids_str.replace(", u'", ", '")       
        validated_data['collector_ids'] = collector_ids_str
        return CollectorSet.serializer_create(validated_data)

    # Overwrite Serializer .update() method
    def update(self, collectorset, validated_data):
        """
        Args:
            vpnendpointremotesite: Existing VPNEndPointRemoteSite record object
            validated_data: New values for VPNEndPointRemoteSite record object

        Returns:
            None

        Raises:
            IDUpdateNotPermitted: On updating the 'id' of policy
        """
        try:
            collector_ids_str = str(validated_data['collector_ids'])
            collector_ids_str = collector_ids_str.replace("{u'", "{'")
            collector_ids_str = collector_ids_str.replace(": u'", ": '")
            collector_ids_str = collector_ids_str.replace(", u'", ", '")
            validated_data['collector_ids'] = collector_ids_str
            record = CollectorSet.serializer_update(self,
                                                    collectorset,
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
        return CollectorSet.serializer_valid(self, pk)
