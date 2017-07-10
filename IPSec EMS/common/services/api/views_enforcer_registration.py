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

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from rest_framework.exceptions import NotFound, status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from services.api.exceptions import ResourceNotFound
from services.api.serializers.serializers_enforcer_registration import (
    IPsecEnforcerRegistration, IPsecEnforcerRegistrationSerializer
)
from services.ipsecenforcer.notification_ipc_client_listener import (
    IPsecEnforcerNotification
)
from services.ipsecenforcer.prepare_vpn_configuration import (
    IPsecEnforcerConfig
)
from services.ipsecenforcer.register_deregister import IPsecEnforcerInfo


@api_view(['GET', 'POST', 'DELETE'])
@renderer_classes((JSONRenderer,))
def ipsec_enforcer_registration(request, version, namespace, pk='None'):
    """Create, list(one or all), update or delete resource.

    Args:
        version (str): API version
        namespace (str): Tenant name
        request (HttpRequest): Complete HTTP request with header and
            body
        pk (str): Primary Key of Record. Defaults to 'None'.

    Note: version and namespace is currently not used. It is for future
        support of multiple API versions and multi tenants.

    Returns:
        HTTPResponse with data/error and status code.
    """
    # Retrieve record(s) to be used by later operations(except POST)
    # pk = 'None' means retrieve all records
    if request.method != 'POST':
        try:
            record = IPsecEnforcerRegistration.get(id=pk)
        except ResourceNotFound:
            raise NotFound(detail=("Resource {0} with id {1} not "
                                   "found").format(IPsecEnforcerRegistration,
                                                   pk))

    # Get the record with id 'pk'
    if request.method == 'GET':
        policy = IPsecEnforcerConfig().prepare_ipsec_enforcer_config(pk)
        return Response(policy, status=status.HTTP_200_OK)

    # Create and store a record
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = IPsecEnforcerRegistrationSerializer(
                data=data,
                context={
                    'resource_name': 'IPsecEnforcerRegistration'
                }
        )
        if serializer.is_valid():
            serializer.save()
            IPsecEnforcerNotification.client_ipsecenforcer_register(
                    serializer.data['id'])
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            serializer.log_invalid()
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    # Delete the record with id 'pk'
    if request.method == 'DELETE':
        # Before de-registration(deletion), fetch all the VPNEndpoint(s)
        # associated with IPsecEnforcer
        mapping_records = (
            IPsecEnforcerInfo.get_ipsecenforcer_to_vpnendpoint_map(
                    record.id)
        )

        # Delete the record
        record.delete()

        # Notify the peer IPsecEnforcer(s)
        IPsecEnforcerNotification.client_ipsecenforcer_deregister(
                    record.id,
                    mapping_records)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
