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

from services.api.serializers.error_msg import (
    IKE_MULTIPLE_ENCRYPTION_ERR_MSG, IKE_MULTIPLE_INTEGRITY_ERR_MSG,
    INVALID_ENCRYPTION_ERR_MSG, INVALID_INTEGRITY_ERR_MSG,
    IKE_MULTIPLE_DH_GROUP_ERR_MSG, INVALID_REAUTH_ERR_MSG
)
from services.api.serializers.resource import Resource, ConsulSerializer
from services.api.serializers.utils_serializers import (
    CustomUUIDField, generate_uuid
)
from services.api.serializers.vpn_choices import (
    DH_GROUP, IKEV1_ENCRYPTION_ALGORITHM, IKEV2_ENCRYPTION_ALGORITHM,
    IKEV1_INTEGRITY_ALGORITHM, IKEV2_INTEGRITY_ALGORITHM, LIFETIME_UNITS
)


class IKEPolicy(Resource):
    """Represents an IKEPolicy object"""
    resource_name = 'IKEPolicy'
    primary_key = 'id'
    secondary_keys = ('name',)

    @staticmethod
    def resource_validation(resource_name, attrs):
        """Validate the request"""

        ike_version = attrs['ike_version']

        if ike_version == 'v2':
            encryption_algorithm = IKEV2_ENCRYPTION_ALGORITHM
            integrity_algorithm = IKEV2_INTEGRITY_ALGORITHM
        elif ike_version == 'v1':
            encryption_algorithm = IKEV1_ENCRYPTION_ALGORITHM
            integrity_algorithm = IKEV1_INTEGRITY_ALGORITHM

        if not set(attrs['encryption_algorithm']).issubset(
                set(encryption_algorithm)):
            raise serializers.ValidationError(INVALID_ENCRYPTION_ERR_MSG +
                                              ike_version)

        if not set(attrs['integrity_algorithm']).issubset(
                set(integrity_algorithm)):
            raise serializers.ValidationError(INVALID_INTEGRITY_ERR_MSG +
                                              ike_version)

        if attrs['ike_version'] == 'v1' and attrs['reauth'] == 'no':
            raise serializers.ValidationError(INVALID_REAUTH_ERR_MSG)

        if (attrs['ike_version'] == 'v1' and
                (len(attrs['encryption_algorithm']) > 1)):
            raise serializers.ValidationError(IKE_MULTIPLE_ENCRYPTION_ERR_MSG)

        if (attrs['ike_version'] == 'v1' and
                (len(attrs['integrity_algorithm']) > 1)):
            raise serializers.ValidationError(IKE_MULTIPLE_INTEGRITY_ERR_MSG)

        if attrs['ike_version'] == 'v1' and (len(attrs['dh_group']) > 1):
            raise serializers.ValidationError(IKE_MULTIPLE_DH_GROUP_ERR_MSG)

        return attrs


class IKEPolicySerializer(ConsulSerializer):
    """Serializer for IKEPolicy"""
    consul_model = IKEPolicy

    #
    # IKEPolicy Attributes' Choices
    #

    _IKE_ENCRYPTION_ALGORITHM = list(set(IKEV1_ENCRYPTION_ALGORITHM +
                                         IKEV2_ENCRYPTION_ALGORITHM))

    _IKE_INTEGRITY_ALGORITHM = list(set(IKEV1_INTEGRITY_ALGORITHM +
                                        IKEV2_INTEGRITY_ALGORITHM))

    _IKE_PHASE1_MODE = (
        'aggressive',
        'main',
    )

    _IKE_VERSION = (
        'v1',
        'v2',
    )

    _IKE_REKEY = (
        'yes',
        'no',
    )

    _IKE_REAUTH = (
        'yes',
        'no',
    )

    #
    # Validators for all the resource fields
    #

    id = CustomUUIDField(format='hex_verbose',
                         default=generate_uuid)

    name = serializers.CharField()

    description = serializers.CharField(required=False)

    ike_version = serializers.ChoiceField(choices=_IKE_VERSION,
                                          default='v2')

    encryption_algorithm = serializers.MultipleChoiceField(
            choices=_IKE_ENCRYPTION_ALGORITHM,
            default=['aes128'])

    integrity_algorithm = serializers.MultipleChoiceField(
            choices=_IKE_INTEGRITY_ALGORITHM,
            default=['sha1'])

    dh_group = serializers.MultipleChoiceField(choices=DH_GROUP,
                                               default=['modp1536'])

    phase1_negotiation_mode = serializers.ChoiceField(choices=_IKE_PHASE1_MODE,
                                                      default='main')

    lifetime_value = serializers.IntegerField(max_value=None,
                                              min_value=1,
                                              default=3,
                                              required=False)

    lifetime_units = serializers.ChoiceField(choices=LIFETIME_UNITS,
                                             default='hours')

    rekey = serializers.ChoiceField(choices=_IKE_REKEY,
                                    default='yes')

    reauth = serializers.ChoiceField(choices=_IKE_REAUTH,
                                     default='yes')

