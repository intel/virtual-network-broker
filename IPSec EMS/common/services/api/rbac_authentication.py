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
import logging
import urlparse

import requests

from django.utils.translation import ugettext as _
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_200_OK

from services.api.rbac_settings import RBAC_PROJECT, RBAC_URI

LOG = logging.getLogger(__name__)

RBAC_RULE_TO_HTTP_VERB_MAP = {
    'GET': 'VIEW',
    'POST': 'ADD',
    'PATCH': 'CHANGE',
    'PUT': 'CHANGE',
    'DELETE': 'DELETE',
}


class RBACAuthorization(BasicAuthentication):
    """Authorize the request with RBAC Webservice"""

    def authenticate(self, request, *args, **kwargs):
        try:
            url = (RBAC_URI + '/' + 'v1/main/auth/projects/' + RBAC_PROJECT +
                   '/' + 'permissions' + '/')
            response = requests.request(
                method='GET',
                url=url,
                headers={
                    'X-Auth-Token': request.META.get('HTTP_X_AUTH_TOKEN', ''),
                    'X-SSL-Client-S-DN': request.META.get(
                            'HTTP_SSL_CLIENT_S_DN', ''),
                    'X-Authorization-Endpoint': urlparse.urlparse(
                            request.build_absolute_uri()).path,
                    'Content-Type': request.META.get('CONTENT_TYPE', '')})

            if response.status_code == HTTP_200_OK:
                permissions = response.json()['permissions']
            else:
                raise PermissionDenied(_("Unauthorized access"))

            if not RBAC_RULE_TO_HTTP_VERB_MAP[request.method] in permissions:
                raise PermissionDenied(_("Unauthorized access"))

        except requests.exceptions.RequestException as e:
            LOG.error('%s %s' % (e.__doc__, e.message))
