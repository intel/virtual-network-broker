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

from django.utils.translation import ugettext as _
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
)
from services.api.rbac_authentication import RBACAuthorization
from services.api.views_utils import get_resource_info
from services.ipsecenforcer.notification_ipc_client_listener import \
    IPsecEnforcerNotification

LOG = logging.getLogger(__name__)


class GenericCommonResourceMixin(object):
    """This Mixin does the provides common methods required for all the
    CRUD operations. It initializes the HTTP request, finds the
    serializer class for the HTTP resource and fills the serializer
    context. It also logs the HTTP request in before finalizing the
    response.
    """

    authentication_classes = (RBACAuthorization,)

    def initial(self, request, *args, **kwargs):
        resource_info = get_resource_info(request.resolver_match.url_name,
                                          **kwargs)
        for key in resource_info.keys():
            self.kwargs[key] = resource_info[key]

        super(GenericCommonResourceMixin, self).initial(request,
                                                        *args,
                                                        **kwargs)

    def get_serializer_class(self):
        return self.kwargs['resource_serializer']

    def get_serializer_context(self):
        return {
            self.kwargs['resource_class'].primary_key: self.kwargs['pk_value'],
        }

    def get_resource_class_and_search_info(self):
        rbac_resource = self.kwargs['resource_class']

        search_info = {
            rbac_resource.primary_key: self.kwargs['pk_value'],
        }

        return rbac_resource, search_info

    def finalize_response(self, request, response, *args, **kwargs):
        LOG.info('"%s %s %s" %s',
                 request.method,
                 request.get_full_path(),
                 request.META.get('SERVER_PROTOCOL'),
                 response.status_code)

        if response.status_code == HTTP_401_UNAUTHORIZED:
            response['WWW-Authenticate'] = 'TokenBased'

        return super(GenericCommonResourceMixin, self).finalize_response(
                request,
                response,
                *args,
                **kwargs)


"""View to handle CRUD operation for RBAC Resources"""


class GenericListCreateResourceView(GenericCommonResourceMixin,
                                    ListCreateAPIView):
    """Create(POST)/List(GET) for IPsec EMS HTTP resources"""

    def get_queryset(self):
        rbac_resource, search_info = self.get_resource_class_and_search_info()

        return rbac_resource.all(**search_info)


class GenericRetrieveUpdateDestroyResourceView(GenericCommonResourceMixin,
                                               RetrieveUpdateDestroyAPIView):
    """Show(GET)/Update(PATCH)/Delete(DELETE) for IPsec EMS HTTP resources"""

    def get_object(self):
        rbac_resource, search_info = self.get_resource_class_and_search_info()

        resource_object = rbac_resource.get(**search_info)

        if resource_object is None:
            raise NotFound(detail=_("%s with %s %s not found") %
                                  (rbac_resource.resource_name,
                                   rbac_resource.primary_key,
                                   self.kwargs['pk_value']))

        return resource_object

    def put(self, request, *args, **kwargs):
        # HTTP PUT method is not allowed on RBAC Resources
        raise MethodNotAllowed(request.method)

    def patch(self, request, *args, **kwargs):
        updated_record = super(GenericRetrieveUpdateDestroyResourceView,
                               self).patch(request,
                                           *args,
                                           **kwargs)
        # IPsecEnforcerNotification.client(
        #          self.get_serializer_class().resource_name,
        #          self.get_object().__dict__,
        #          request.data)

        return Response(updated_record.data, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        super(GenericRetrieveUpdateDestroyResourceView, self).delete(request,
                                                                     *args,
                                                                     **kwargs)
        # IPsecEnforcerNotification.client(
        #           self.get_serializer_class().resource_name,
        #           self.get_object().__dict__)

        return Response(status=HTTP_204_NO_CONTENT)
