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

from services.api.views_resource import RESOURCES

DELIMITER = '_'


def get_resource_info(url_name, **path_kwargs):
    """Get the RBAC Resource and Project information from URI and path
    kwargs for RBAC Resources CRUD operation

    Args:
        url_name (str): Name of resolved URI(Endpoint) in urlconf
        path_kwargs (dict): HTTPRequest Path kwargs

    Returns:
        tuple: tuple of resource_class, resource_serializer, project_info,
            pk_value
    """
    resource_info = {}

    try:
        pk_value = path_kwargs['pk']
    except KeyError:
        pk_value = None

    resource_info.update({
        'pk_value': pk_value,
    })

    resource_class, resource_serializer = get_resource_info_for_crud(url_name)
    resource_info.update({
            'resource_class': resource_class,
            'resource_serializer': resource_serializer,
    })

    return resource_info


def get_resource_info_for_crud(url_name):
    """Get the RBAC Resource and Project information from URI and path
    kwargs for RBAC Resources CRUD operation

    Args:
        url_name (str): Name of resolved URI(Endpoint) in urlconf

    Returns:
        tuple: tuple of RBAC project id, project name, project
            serializer and a combined primary/secondary record
    """
    resource_name = DELIMITER.join(url_name.split(DELIMITER)[:-1])

    resource_class, resource_serializer = RESOURCES[resource_name][1:]

    return resource_class, resource_serializer


def get_resource_from_path(request):
    """Get the resource name from URI

    Args:
        request (Request) :  Complete HTTP request with header and
            body

    Returns:
        resource name
    """
    # e.g. In a URI (e.g. /v1/<namespace>/ipsecvpn/resource), 'resource' name
    # is the fifth element if split with separator '/'
    return request.get_full_path().decode('unicode-escape').encode(
            'utf8').rsplit('/')[4]

