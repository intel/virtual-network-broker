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

from rest_framework import serializers

from services.api.serializers.resource import Resource, ConsulSerializer
from services.api.serializers.utils_serializers import (
    CustomUUIDField, generate_uuid
)
from services.api.serializers.vpn_choices import (
    DH_GROUP, IPSEC_IKEV1_ENCRYPTION_ALGORITHM,
    IPSEC_IKEV2_ENCRYPTION_ALGORITHM, IPSEC_IKEV1_INTEGRITY_ALGORITHM,
    IPSEC_IKEV2_INTEGRITY_ALGORITHM, LIFETIME_UNITS
)


class IPsecPolicy(Resource):
    """Represents a IPsecPolicy object"""
    resource_name = 'IPsecPolicy'
    primary_key = 'id'
    secondary_keys = ('name',)

    @staticmethod
    def resource_validation(resource_name, attrs):
        pass


class IPsecPolicySerializer(ConsulSerializer):
    """Serializer for IPsecPolicy"""
    consul_model = IPsecPolicy

    # IPsecPolicy Attributes' Choices

    _IKE_ENCRYPTION_ALGORITHM = list(set(IPSEC_IKEV1_ENCRYPTION_ALGORITHM +
                                         IPSEC_IKEV2_ENCRYPTION_ALGORITHM))

    _IKE_INTEGRITY_ALGORITHM = list(set(IPSEC_IKEV1_INTEGRITY_ALGORITHM +
                                        IPSEC_IKEV2_INTEGRITY_ALGORITHM))

    _IPSEC_ESN_MODE = (
        'esn',
        'noesn',
    )

    _IPSEC_TRANSFORM_PROTOCOL = (
        'ah',
        'esp',
    )

    _IPSEC_ENCAPSULATION_MODE = (
        'transport',
        'tunnel',
    )

    #
    # Validators for all the resource fields
    #

    id = CustomUUIDField(format='hex_verbose',
                         default=generate_uuid)

    name = serializers.CharField()

    description = serializers.CharField(required=False)

    transform_protocol = serializers.ChoiceField(
            choices=_IPSEC_TRANSFORM_PROTOCOL,
            default='esp')

    encryption_algorithm = serializers.MultipleChoiceField(
            choices=_IKE_ENCRYPTION_ALGORITHM,
            default=['aes128'])

    integrity_algorithm = serializers.MultipleChoiceField(
            choices=_IKE_INTEGRITY_ALGORITHM,
            default=['sha1'])

    dh_group = serializers.MultipleChoiceField(choices=DH_GROUP,
                                               default=['modp1536'])

    esn_mode = serializers.ChoiceField(
            choices=_IPSEC_ESN_MODE,
            default='noesn')

    encapsulation_mode = serializers.ChoiceField(
            choices=_IPSEC_ENCAPSULATION_MODE,
            default='tunnel')

    lifetime_value = serializers.IntegerField(max_value=None,
                                              min_value=1,
                                              default=3600)

    lifetime_units = serializers.ChoiceField(choices=LIFETIME_UNITS,
                                             default='seconds')
