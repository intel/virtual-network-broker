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

from __future__ import unicode_literals

from services.api.serializers.serializers_ikepolicy import (
    IKEPolicy, IKEPolicySerializer
)
from services.api.serializers.serializers_ipsecpolicy import (
    IPsecPolicy, IPsecPolicySerializer
)
from services.api.serializers.serializers_vpnbind_group_to_group import (
    VPNBindGroupToGroup, VPNBindGroupToGroupSerializer
)
from services.api.serializers.serializers_vpnbind_group_to_localsite import (
    VPNBindGroupToLocalSite, VPNBindGroupToLocalSiteSerializer
)
from services.api.serializers.serializers_vpnbind_group_to_remotesite import (
    VPNBindGroupToRemoteSite, VPNBindGroupToRemoteSiteSerializer
)
from services.api.serializers.serializers_vpnbind_localsite_to_localsite \
    import (
        VPNBindLocalSiteToLocalSite, VPNBindLocalSiteToLocalSiteSerializer,
    )
from services.api.serializers.serializers_vpnbind_localsite_to_remotesite \
    import (
        VPNBindLocalSiteToRemoteSite, VPNBindLocalSiteToRemoteSiteSerializer
    )
from services.api.serializers.serializers_vpncacertificate import (
    VPNCACertificate, VPNCACertificateSerializer
)
from services.api.serializers.serializers_vpncertificate import (
    VPNCertificate, VPNCertificateSerializer
)
from services.api.serializers.serializers_vpnendpointgroup import (
    VPNEndpointGroup, VPNEndpointGroupSerializer
)
from services.api.serializers.serializers_vpnendpointlocalsite import (
    VPNEndpointLocalSite, VPNEndpointLocalSiteSerializer
)
from services.api.serializers.serializers_vpnendpointremotesite import (
    VPNEndpointRemoteSite, VPNEndpointRemoteSiteSerializer
)

"""
    Mapping from URI names to project (Class and Serializer)

    Note: HTTP resource is the key for the below dictionary.
"""

RESOURCES = {
    'ikepolicies': (
        'IKEPolicy',
        IKEPolicy,
        IKEPolicySerializer,
    ),
    'ipsecpolicies': (
        'IPSecPolicy',
        IPsecPolicy,
        IPsecPolicySerializer,
    ),
    'vpnbindgrouptogroup': (
        'VPNBindGroupToGroup',
        VPNBindGroupToGroup,
        VPNBindGroupToGroupSerializer,
    ),
    'vpnbindgrouptolocalsite': (
        'VPNBindGroupToLocalSite',
        VPNBindGroupToLocalSite,
        VPNBindGroupToLocalSiteSerializer,
    ),
    'vpnbindgrouptoremotesite': (
        'VPNBindGroupToRemoteSite',
        VPNBindGroupToRemoteSite,
        VPNBindGroupToRemoteSiteSerializer,
    ),
    'vpnbindlocalsitetolocalsite': (
        'VPNBindLocalSiteToLocalSite',
        VPNBindLocalSiteToLocalSite,
        VPNBindLocalSiteToLocalSiteSerializer,
    ),
    'vpnbindlocalsitetoremotesite': (
        'VPNBindLocalSiteToRemoteSite',
        VPNBindLocalSiteToRemoteSite,
        VPNBindLocalSiteToRemoteSiteSerializer,
    ),
    'vpncacertificates': (
        'VPNCACertificate',
        VPNCACertificate,
        VPNCACertificateSerializer,
    ),
    'vpncertificates': (
        'VPNCertificate',
        VPNCertificate,
        VPNCertificateSerializer,
    ),
    'vpnendpointgroups': (
        'VPNEndPointGroup',
        VPNEndpointGroup,
        VPNEndpointGroupSerializer,
    ),
    'vpnendpointlocalsites': (
        'VPNEndPointLocalSite',
        VPNEndpointLocalSite,
        VPNEndpointLocalSiteSerializer,
    ),
    'vpnendpointremotesites': (
        'VPNEndpointRemoteSite',
        VPNEndpointRemoteSite,
        VPNEndpointRemoteSiteSerializer,
    ),
}
