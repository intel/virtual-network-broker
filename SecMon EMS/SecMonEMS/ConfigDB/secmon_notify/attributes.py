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

""" Common definitions
"""
# resource name
NETFLOWASSOCIATION = 'netflowassociation'
COLLECTOR = 'collector'
NETFLOWCONFIG = 'netflowconfig'
NETFLOWMONITOR = 'netflowmonitor'
SFLOWCONFIG = 'sflowconfig'
SFLOWASSOCIATION = 'sflowassociation'
RAWFORWARDASSOCIATION = 'rawforwardassociation'
CLASSIFICATIONOBJECT = 'classificationobject'
RULEOBJECT = 'ruleobject'
POLICY = 'policy'
SCOPE = 'scope'
SECMONDETAILS = 'secmondetails'
COLLECTORSET = 'collectorset'
NOTIFICATION = 'notification'

# operation name
DELETE = 'DELETE'

# field name
PRIMARY_ID = 'id'
COLLECTOR_ID = 'collector_id'
COLLECTORSET_ID = 'collectorset_id'
COLLECTOR_IDS = 'collector_ids'
CLASSIFICATION_ID = 'classificationobject_id'
RULEOBJECT_ID = 'ruleobject_id'
POLICIES = 'policies'
COL_TYPE = 'col_type'
POLICY_ID = 'policy_id'
SCOPE_ID = 'scope_id'
ROW_ID = 'row_id'
IP_ADDRESS = 'ip_address'
PORT = 'port'
SCOPE_NAME = 'scope_name'
POST = 'POST'

# Dict name
PLUGIN_ASSOCIATION_MAPPING = {'netflow': 'netflowassociation',
                              'sflow': 'sflowassociation',
                              'rawforward': 'rawforwardassociation'}
