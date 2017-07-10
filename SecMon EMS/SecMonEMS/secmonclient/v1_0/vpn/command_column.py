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

# Command output columns

IKEPOLICY_COLUMNS = [
    'id',
    'name',
    'description',
    'encryption_algorithm',
    'integrity_algorithm',
    'phase1_negotiation_mode',
    'lifetime_value',
    'lifetime_units',
    'ike_version',
    'rekey',
    'reauth',
]

IPSECPOLICY_COLUMNS = [
    'id',
    'name',
    'description',
    'transform_protocol',
    'encryption_algorithm',
    'auth_algorithm',
    'dh_group',
    'encapsulation_mode',
    'lifetime_value',
    'lifetime_units',
]

VPNENDPOINTGROUP_COLUMNS = [
    'id',
    'name',
    'description',
]

VPNENDPOINTLOCALSITE_COLUMNS = [
    'id',
    'name',
    'description',
    'cidrs',
]

VPNENDPOINTREMOTESITE_COLUMNS = [
    'id',
    'name',
    'description',
    'peer_address',
    'peer_cidrs',
]

VPNBINDGROUPTOGROUP_COLUMNS = [
    'id',
    'name',
    'description',
    'vpnendpointgroup_id',
    'peer_vpnendpointgroup_id',
    'admin_state_up',
    'dpd_action',
    'dpd_interval',
    'dpd_timeout',
    'auth_mode',
    'psk',
    'initiator',
    'ikepolicy_id',
    'ipsecpolicy_id',
]

VPNBINDGROUPTOLOCALSITE_COLUMNS = [
    'id',
    'name',
    'description',
    'vpnendpointgroup_id',
    'peer_vpnendpointgroup_id',
    'admin_state_up',
    'dpd_action',
    'dpd_interval',
    'dpd_timeout',
    'auth_mode',
    'psk',
    'initiator',
    'ikepolicy_id',
    'ipsecpolicy_id',
]

VPNBINDGROUPTOREMOTESITE_COLUMNS = [
    'id',
    'name',
    'description',
    'vpnendpointgroup_id',
    'peer_vpnendpointgroup_id',
    'admin_state_up',
    'dpd_action',
    'dpd_interval',
    'dpd_timeout',
    'auth_mode',
    'psk',
    'initiator',
    'ikepolicy_id',
    'ipsecpolicy_id',
]

VPNBINDLOCALSITETOLOCALSITE_COLUMNS = [
    'id',
    'name',
    'description',
    'vpnendpointlocalsite_id',
    'peer_vpnendpointlocalsite_id',
    'admin_state_up',
    'dpd_action',
    'dpd_interval',
    'dpd_timeout',
    'auth_mode',
    'psk',
    'initiator',
    'ikepolicy_id',
    'ipsecpolicy_id',
]

VPNBINDLOCALSITETOREMOTESITE_COLUMNS = [
    'id',
    'name',
    'description',
    'vpnendpointgroup_id',
    'peer_vpnendpointgroup_id',
    'admin_state_up',
    'dpd_action',
    'dpd_interval',
    'dpd_timeout',
    'auth_mode',
    'psk',
    'initiator',
    'ikepolicy_id',
    'ipsecpolicy_id',
]

VPNBINDLOCALSITE_COLUMNS = [
    'id',
    'name',
    'description',
    'vpnendpointlocalsite_id',
    'peer_vpnendpointlocalsite_id',
    'admin_state_up',
    'dpd_action',
    'dpd_interval',
    'dpd_timeout',
    'auth_mode',
    'connection_id',
    'peer_connection_id',
    'psk',
    'initiator',
    'status'
    'ikepolicy_id',
    'ipsecpolicy_id',
]

VPNBINDREMOTESITE_COLUMNS = [
    'id',
    'name',
    'description',
    'vpnendpointlocalsite_id',
    'peer_vpnendpointremotesite_id',
    'admin_state_up',
    'dpd_action',
    'dpd_interval',
    'dpd_timeout',
    'auth_mode',
    'connection_id',
    'peer_connection_id',
    'psk',
    'initiator',
    'status',
    'ikepolicy_id',
    'ipsecpolicy_id',
]

FIELD_MAPPING = {
    'lb_algo':{'session_based':'0', 'round_robin':'1', 'weighted_round_robin':'2',},
    'action' : {'forward':'1', 'drop':'0',},
    'protocol' : {'ICMP':'1', 'TCP':'6', 'UDP':'17', 'SCTP':'132',},
}

REVERSE_FIELD_MAPPING = {
    'lb_algo':{'0':'session_based','1':'round_robin','2':'weighted_round_robin',},
    'action' : {'1':'forward', '0':'drop',},
    'protocol' : {'1':'ICMP', '6':'TCP', '17':'UDP', '132':'SCTP',},
}

#ACTION_MAPPING = {
#    'action' : {'forward':1, 'drop':0,}
#}

#REVERSE_ACTION_MAPPING = {
#    'action' : {1:'forward', 0:'drop',}

#}

#PROTOCOL_MAPPING = {
#    'protocol' : {'ICMP':1, 'TCP':6, 'UDP':17, 'SCTP':132,}
#}

#REVERSE_PROTOCOL_MAPPING = {
#    'protocol' : {1:'ICMP', 6:'TCP', 17:'UDP', 132:'SCTP',}
#}
