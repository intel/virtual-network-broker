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

"""Mapping from URI names to resource names(Class and Serializer)
"""

import logging
import configfile 
import pdb
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from rest_framework import status
# from rest_framework import NotFound
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from ConfigDB.api.exceptions import ResourceNotFound, ResourceExist
from ConfigDB.api.exceptions import IDUpdateNotPermitted
from ConfigDB.api.utils import get_resource_from_path
from ConfigDB.api.utils import get_sk_from_path
from ConfigDB.api.views_api_resource import RESOURCES
from ConfigDB.secmon_notify.notification_process import SecMonNotification
import inspect
# LOG = configfile.configlogging()

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@renderer_classes((JSONRenderer,))
def resource(request, version, namespace, pk='None', sk='None'):
    """Create, list(one or all), update or delete resource.

    Args:
        namespace:
        version:
        request (HttpRequest): Complete HTTP request with header and body
        pk (str): Primary Key of Record. Defaults to 'None'.
        sk (str): Secondary key of record. Defaults to 'None'.

    Returns:
        HTTPResponse with data/error and status code.
    """
    notification_id = '1'
    session_var = 'notification_var'
    notification_table_name = 'notification'

    resource_name = get_resource_from_path(request)
    resource_class = RESOURCES[resource_name][1]
    resource_serializer = RESOURCES[resource_name][2]
#    logger.info('resource name: %s', resource_name)
#    logger.info('request method: %s', request.method)
    if (session_var not in request.session and
            notification_table_name in resource_name and
            request.method == 'PUT'):
        data = JSONParser().parse(request)
        data['id'] = notification_id
        serializer = resource_serializer(data=data)
        if serializer.valid(pk):
            serializer.create(serializer.data)
            SecMonNotification.client(serializer.data['id'],
                                      resource_name,
                                      request.method
                                      )
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        request.session[session_var] = True
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' sending success response for notification')
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    # FIXME(manjula):set session variable to false for notification
    if notification_table_name in resource_name and request.method == 'DELETE':
        notification_var = False

    # FIXME(manjula):list records for collector/collectorset per plugin
    if pk in {'netflow', 'rawforward', 'sflow'}:
        try:
            records = resource_class.get_all_records_by_secondary_index(
                'col_type', pk)
        except ResourceNotFound:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + ' no collector/collectorset data found for ' + pk)
            return Response({'detail': 'Resource not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = resource_serializer(records)
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' successfully fetched collector/collectorset data for ' + pk)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    # list records based on secondary key value
    if sk != 'None':
        try:
            sk_name = get_sk_from_path(request)
            records = resource_class.get_all_records_by_secondary_index(
                sk_name, sk)
        except ResourceNotFound:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + ' no data found for secondary key ' + sk + 'in' + resource_name)
            return Response({'detail': 'Resource not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = resource_serializer(records)
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' successfully fetched data on secondary key ' + sk + 'in' + resource_name)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    # list records based on primary key value
    if request.method != 'POST':
        try:
            record = resource_class.get(pk) if pk != 'None' \
                else resource_class.get_all()
        except ResourceNotFound:
#           logger.error('Resource not found')
            return Response({'detail': 'Resource not found'},
                            status=status.HTTP_404_NOT_FOUND)

    # List all records
    if request.method == 'GET' and pk == 'None':
        serializer = resource_serializer(record, many=True)
        print("sending data for GET request")
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' sending data for GET request for ' + resource_name)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    # List the record with id 'pk'
    if request.method == 'GET':
        serializer = resource_serializer(record)
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' successfully fetched data for ' + resource_name)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    # Create and store a record
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = resource_serializer(data=data)
        if serializer.valid(pk):
            try:
                serializer.create(serializer.data)
                configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' sending notification for post method for ' + resource_name)
                SecMonNotification.client(serializer.data['id'],
                                          resource_name,
                                          request.method
                                          )
                configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' successfully created data for ' + resource_name) 
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except ResourceExist:
                configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + ' record already exist for ' + resource_name)
                return Response({'detail': 'Resource already exist'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    # Update the record with id 'pk'
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = resource_serializer(record,
                                         data=data,
                                         partial=True,
                                         context={'pk': pk})
        try:
            serializer.update(record, data)
            configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' sending notification for put method for ' + resource_name)
            SecMonNotification.client(serializer.data['id'],
                                      resource_name,
                                      request.method)
        except IDUpdateNotPermitted:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + ' id update is not permitted')
            return Response({'detail': '"id" update not permitted'},
                            status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + ' None data cannot be updated')
            return Response({'detail': 'None data cannot be updated'},
                            status=status.HTTP_400_BAD_REQUEST)
        configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' data updated successfully for ' + resource_name)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    # Delete the record with id 'pk'
    if request.method == 'DELETE':
        try:
            serializer = resource_serializer(record)
            data = serializer.data
            record.delete()
            configfile.logging_obj.info(__file__  + ' ' + str(inspect.stack()[0][2]) + ' sending notification for delete method for ' + resource_name)
            SecMonNotification.client(serializer.data['id'],
                                      resource_name,
                                      request.method,
                                      data)
            configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + ' successfully deleted record for ' + resource_name)
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except ResourceNotFound:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + ' Resource not found for DELETE request for ' + resource_name)
            return Response({'detail': 'Resource not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except RuntimeError: 
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + ' Resource cannot be deleted as dependency exist')
            return Response({'detail': 'Resource cannot be deleted as dependency exist'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
