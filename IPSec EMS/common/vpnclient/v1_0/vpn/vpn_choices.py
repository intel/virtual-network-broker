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

# Common definitions for string field maximum length
NAME_MAX_LEN = 100
DESCRIPTION_MAX_LEN = 100

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


"""
IKE SA Specific choices
"""

# Encryption

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

# Integrity

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

"""
IPsec Connection Specific choices
"""

# Encryption

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

# Integrity

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

