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

import json
import logging
import urlparse

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

from services.api.rbac_settings import RBAC_URI

LOG = logging.getLogger(__name__)


@api_view(['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def resource(request, version, namespace, pk='None'):
    try:
        url = RBAC_URI + request.get_full_path()
        response = requests.request(
                method=request.method,
                url=url,
                data=json.dumps(request.data),
                headers={
                    'X-Auth-Token': request.META.get('HTTP_X_AUTH_TOKEN', ''),
                    'X-SSL-Client-S-DN': request.META.get(
                            'HTTP_SSL_CLIENT_S_DN', ''),
                    'X-Authorization-Endpoint': urlparse.urlparse(
                            request.build_absolute_uri()).path,
                    'Content-Type': request.META.get('CONTENT_TYPE', '')})

        response_content_type = response.headers.get('Content-Type', None)
        response_data = response.content

        # Only JSON response is formatted
        if response_content_type == 'application/json':
                response_data = response.json()

        return Response(response_data,
                        status=response.status_code,
                        headers=response.headers,
                        content_type=response_content_type)

    except requests.exceptions.RequestException as e:
        LOG.error('%s %s' % (e.__doc__, e.message))



