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
from rest_framework.decorators import (
    api_view, renderer_classes, parser_classes
)
from rest_framework.exceptions import NotFound, status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from services.api.exceptions import ResourceNotFound, PKUpdateNotPermitted
from services.api.serializers.utils_serializers import pop_key, pop_keys
from services.api.views_utils import get_resource_from_path
from services.api.views_resource import RESOURCES


@api_view(['GET', 'POST',  'PUT', 'DELETE'])
@renderer_classes((JSONRenderer,))
@parser_classes((FormParser, MultiPartParser))
def resource(request, version, namespace, pk='None'):
    """Create, list(one or all), update or delete resource.

    Args:
        version (str): API version
        namespace (str): Tenant name
        request (Request): Complete HTTP request with header and
            body
        pk (str): Primary Key of Record. Defaults to 'None'.

    Note: version and namespace is currently not used. It is for future
        support of multiple API versions and multi tenants.

    Returns:
        HTTPResponse with data/error and status code.
    """
    uri_resource_name = get_resource_from_path(request)
    resource_name = RESOURCES[uri_resource_name][0]
    resource_class = RESOURCES[uri_resource_name][1]
    resource_serializer = RESOURCES[uri_resource_name][2]

    # Retrieve record(s) to be used by later operations(except POST)
    # pk = 'None' means retrieve all records
    if request.method != 'POST':
        try:
            record = resource_class.get(id=pk) if pk != 'None' \
                else resource_class.all()
        except ResourceNotFound:
            raise NotFound(detail=("Resource {0} with id {1} not "
                                   "found").format(resource_name, pk))

    # List all records
    if request.method == 'GET' and pk == 'None':
        serializer = resource_serializer(record, many=True)
        pop_keys(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    # List the record with id 'pk'
    if request.method == 'GET':
        serializer = resource_serializer(record)
        record = resource_class.get(id=serializer.data['id']).__dict__
        pop_key(record)
        return Response(record,
                        status=status.HTTP_200_OK)

    # Create and store a record
    if request.method == 'POST':
        serializer = resource_serializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            record = resource_class.get(id=serializer.data['id']).__dict__
            pop_key(record)
            return Response(record,
                            status=status.HTTP_201_CREATED)
        else:
            serializer.log_invalid()
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    # Update the record with id 'pk'
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = resource_serializer(record,
                                         data=data,
                                         partial=True,
                                         context={'pk': pk})
        if serializer.is_valid():
            try:
                serializer.save()
            except PKUpdateNotPermitted:
                return Response({'detail': '"id" update not permitted'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            serializer.log_invalid()
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    # Delete the record with id 'pk'
    if request.method == 'DELETE':
        record.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
