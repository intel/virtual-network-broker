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

VPN_BIND = [
   'VPNBindGroupToGroup',
   'VPNBindGroupToLocalSite',
   'VPNBindGroupToRemoteSite',
   'VPNBindLocalSiteToLocalSite',
   'VPNBindLocalSiteToRemoteSite',
]

VPN_BIND_GROUP = [
    'VPNBindGroupToGroup',
    'VPNBindGroupToLocalSite',
    'VPNBindGroupToRemoteSite',
]

VPN_BIND_LOCALSITE = [
    'VPNBindLocalSiteToLocalSite',
    'VPNBindLocalSiteToRemoteSite',
    'VPNBindGroupToLocalSite',
]

VPN_BIND_REMOTESITE = [
    'VPNBindGroupToRemoteSite',
    'VPNBindLocalSiteToRemoteSite',
]

# Resource Name to Relation/Table Name Mapping
RESOURCE_TO_RELATION_MAP = {
    'Resource': 'resource',

    # Policy
    'IKEPolicy': 'ikepolicies',
    'IPsecPolicy': 'ipsecpolicies',

    # Bind
    'VPNBindGroupToGroup': 'vpnbind_group_to_group',
    'VPNBindGroupToLocalSite': 'vpnbind_group_to_localsite',
    'VPNBindGroupToRemoteSite': 'vpnbind_group_to_remotesite',
    'VPNBindLocalSiteToLocalSite': 'vpnbind_localsite_to_localsite',
    'VPNBindLocalSiteToRemoteSite': 'vpnbind_localsite_to_remotesite',

    # Endpoint
    'VPNEndpointGroup': 'vpnendpointgroups',
    'VPNEndpointLocalSite': 'vpnendpointlocalsites',
    'VPNEndpointRemoteSite': 'vpnendpointremotesites',

    # Certificates
    'VPNCertificate': 'vpncertificates',
    'VPNCACertificate': 'vpncacertificates',

    # IPsecEnforcer
    'IPsecEnforcerRegistration': 'ipsec_enforcer_registrations',
    'VPNEndpointIPsecEnforcerFQDNMap': 'vpnendpoint_to_ipsec_enforcer_fqdn_map',
    'IPsecEnforcerVPNEndpointMap': 'ipsec_enforcer_to_vpnendpoint_map',
    'IPsecEnforcerConfigVersion': 'ipsec_enforcer_config_version',
}

# Relation Dependencies(Non-VPNBIND Resources)
RESOURCE_DEPENDENCY_MAP = {
    'IKEPolicy': [VPN_BIND,
                  'ikepolicy_id'],
    'IPsecPolicy': [VPN_BIND,
                    'ipsecpolicy_id'],
    'VPNEndpointGroup': [VPN_BIND_GROUP,
                         'vpnendpointgroup_id',
                         'peer_endpointgroup_id'],
    'VPNEndpointLocalSite': [VPN_BIND_LOCALSITE,
                             'vpnendpointlocalsite_id',
                             'peer_endpointlocalsite_id'],
    'VPNEndpointRemoteSite': [VPN_BIND_REMOTESITE,
                              'vpnendpointremotesite_id',
                              'peer_endpointremotesite_id'],
}


#
# ENUM values for VPN Policy configuration parameters
#

# VPN BIND Attributes' Choices

BIND_INITIATOR = [
    'bi-directional',
    'response-only',
]

BIND_DPD_ACTION = [
    'clear',
    'disabled',
    'hold',
    'restart',
    'restart-by-peer',
]

BIND_AUTH_MODE = [
    'psk',
    'cert',
]

# STATUS is only applicable for Bind Site(Local or Remote) Connections
BIND_SITE_STATUS = [
    'ACTIVE',
    'DOWN',
    'BUILD',
    'ERROR',
    'PENDING_CREATE',
    'PENDING_UPDATE',
    'PENDING_DELETE',
]

# Diffie Hellman(DH) Groups
DH_GROUP = [
    'modp768',
    'modp1024',
    'modp1536',
    'modp2048',
    'modp3072',
    'modp4096',
    'modp6144',
    'modp8192',
    'modp1024s160',
    'modp2048s224',
    'modp2048s256',
    'ecp192',
    'ecp224',
    'ecp256',
    'ecp384',
    'ecp521',
    'ecp224bp',
    'ecp256bp',
    'ecp384bp',
    'ecp512bp',
]

# Lifetime Units(IKE SA and IPsec Connection)
LIFETIME_UNITS = [
    'seconds',
    'minutes',
    'hours',
    'days',
]

"""IKE SA Specific choices"""

#
# Encryption
#

IKEV1_ENCRYPTION_ALGORITHM = [
    'aes128',
    'aes192',
    'aes256',
    '3des',
    'blowfish128',
    'blowfish192',
    'blowfish256',
]

IKEV2_ENCRYPTION_ALGORITHM = [
    'null',
    'aes128',
    'aes192',
    'aes256',
    'aes128ctr',
    'aes192ctr',
    'aes256ctr',
    'aes128ccm8',
    'aes192ccm8',
    'aes256ccm8',
    'aes128ccm12',
    'aes192ccm12',
    'aes256ccm12',
    'aes128ccm16',
    'aes192ccm16',
    'aes256ccm16',
    'aes128gcm8',
    'aes192gcm8',
    'aes256gcm8',
    'aes128gcm12',
    'aes192gcm12',
    'aes256gcm12',
    'aes128gcm16',
    'aes192gcm16',
    'aes256gcm16',
    '3des',
    'cast128',
    'blowfish128',
    'blowfish192',
    'blowfish256',
]

#
# Integrity
#

IKEV1_INTEGRITY_ALGORITHM = [
    'md5',
    'sha1',
    'sha256',
    'sha384',
    'sha512',
]

IKEV2_INTEGRITY_ALGORITHM = [
    'md5',
    'sha1',
    'sha256',
    'sha384',
    'sha512',
    'aesxcbc',
    'aesxcbc',
]

"""IPsec Connection Specific choices"""

#
# Encryption
#

IPSEC_IKEV1_ENCRYPTION_ALGORITHM = [
    'null',
    'aes128',
    'aes192',
    'aes256',
    'aes128ctr',
    'aes192ctr',
    'aes256ctr',
    'aes128ccm8',
    'aes192ccm8',
    'aes256ccm8',
    'aes128ccm12',
    'aes192ccm12',
    'aes256ccm12',
    'aes128ccm16',
    'aes192ccm16',
    'aes256ccm16',
    'aes128gcm8',
    'aes192gcm8',
    'aes256gcm8',
    'aes128gcm12',
    'aes192gcm12',
    'aes256gcm12',
    'aes128gcm16',
    'aes192gcm16',
    'aes256gcm16',
    'aes128gmac',
    'aes192gmac',
    'aes256gmac',
    '3des',
    'blowfish128',
    'blowfish192',
    'blowfish256',
]

IPSEC_IKEV2_ENCRYPTION_ALGORITHM = [
    'null',
    'aes128',
    'aes192',
    'aes256',
    'aes128ctr',
    'aes192ctr',
    'aes256ctr',
    'aes128ccm8',
    'aes192ccm8',
    'aes256ccm8',
    'aes128ccm12',
    'aes192ccm12',
    'aes256ccm12',
    'aes128ccm16',
    'aes192ccm16',
    'aes256ccm16',
    'aes128gcm8',
    'aes192gcm8',
    'aes256gcm8',
    'aes128gcm12',
    'aes192gcm12',
    'aes256gcm12',
    'aes128gcm16',
    'aes192gcm16',
    'aes256gcm16',
    'aes128gmac',
    'aes192gmac',
    'aes256gmac',
    '3des',
    'blowfish128',
    'blowfish192',
    'blowfish256',
]

#
# Integrity
#

IPSEC_IKEV1_INTEGRITY_ALGORITHM = [
    'md5',
    'sha1',
    'sha256',
    'sha256_96',
    'sha384',
    'sha512',
    'aesxcbc',
    'aes128gmac',
    'aes192gmac',
    'aes256gmac',
]

IPSEC_IKEV2_INTEGRITY_ALGORITHM = [
    'md5',
    'md5_128',
    'sha1',
    'sha1_160',
    'sha256',
    'sha256_96',
    'sha384',
    'sha512',
    'aes128gmac',
    'aes192gmac',
    'aes256gmac',
]
