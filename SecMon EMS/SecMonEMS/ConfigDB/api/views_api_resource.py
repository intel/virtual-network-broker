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

"""Mapping from URI names to resource names(Class and Serializer)
"""

from ConfigDB.api.serializers.serializers_classificationobject import (
    ClassificationObject, ClassificationObjectSerializer
)
from ConfigDB.api.serializers.serializers_collector import (
    Collector, CollectorSerializer
)
from ConfigDB.api.serializers.serializers_collectorset import (
    CollectorSet, CollectorSetSerializer
)
from ConfigDB.api.serializers.serializers_netflowassociation import (
    NetFlowAssociation, NetFlowAssociationSerializer
)
from ConfigDB.api.serializers.serializers_netflowconfig import (
    NetFlowConfig, NetFlowConfigSerializer
)
from ConfigDB.api.serializers.serializers_netflowmonitor import (
    NetFlowMonitor, NetFlowMonitorSerializer
)
from ConfigDB.api.serializers.serializers_notification import (
    Notification, NotificationSerializer
)
from ConfigDB.api.serializers.serializers_policy import (
    Policy, PolicySerializer
)
from ConfigDB.api.serializers.serializers_rawforwardassociation import (
    RawForwardAssociation, RawForwardAssociationSerializer
)
from ConfigDB.api.serializers.serializers_ruleobject import (
    RuleObject, RuleObjectSerializer
)
from ConfigDB.api.serializers.serializers_scope import (
    Scope, ScopeSerializer
)
from ConfigDB.api.serializers.serializers_secmondetails import (
    SecmonDetails, SecmonDetailsSerializer
)
from ConfigDB.api.serializers.serializers_sflowassociation import (
    SflowAssociation, SflowAssociationSerializer
)
from ConfigDB.api.serializers.serializers_sflowconfig import (
    SflowConfig, SflowConfigSerializer
)

RESOURCES = {
    'netflowassociation': [
        'NetFlowAssociation',
        NetFlowAssociation,
        NetFlowAssociationSerializer,
    ],
    'rawforwardassociation': [
        'RawForwardAssociation',
        RawForwardAssociation,
        RawForwardAssociationSerializer,
    ],
    'sflowassociation': [
        'SflowAssociation',
        SflowAssociation,
        SflowAssociationSerializer,
    ],
    'netflowconfig': [
        'NetFlowConfig',
        NetFlowConfig,
        NetFlowConfigSerializer,
    ],
    'netflowmonitor': [
        'NetFlowMonitor',
        NetFlowMonitor,
        NetFlowMonitorSerializer,
    ],
    'collector': [
        'Collector',
        Collector,
        CollectorSerializer,
    ],
    'collectorset': [
        'CollectorSet',
        CollectorSet,
        CollectorSetSerializer,
    ],
    'policy': [
        'Policy',
        Policy,
        PolicySerializer,
    ],
    'sflowconfig': [
        'SflowConfig',
        SflowConfig,
        SflowConfigSerializer,
    ],
    'scope': [
        'Scope',
        Scope,
        ScopeSerializer,
    ],
    'classificationobject': [
        'ClassificationObject',
        ClassificationObject,
        ClassificationObjectSerializer,
    ],
    'ruleobject': [
        'RuleObject',
        RuleObject,
        RuleObjectSerializer,
    ],
    'secmondetails': [
        'SecmonDetails',
        SecmonDetails,
        SecmonDetailsSerializer,
    ],
    'notification': [
        'Notification',
        Notification,
        NotificationSerializer,
    ],
}
