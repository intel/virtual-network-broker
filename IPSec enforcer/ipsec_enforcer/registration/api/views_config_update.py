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

from multiprocessing.connection import Client

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (
    api_view, renderer_classes
)
from rest_framework.exceptions import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


@csrf_exempt
@api_view(['GET',])
@renderer_classes((JSONRenderer,))
def ipsecenforcer_config_update(request, version, namespace, pk='None'):
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
    client = Client(('localhost', 8081))
    client.send("update")
    return Response(status=status.HTTP_200_OK)
