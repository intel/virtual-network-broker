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


import ast
import errno
import random
import string
import urllib2
import json
import pdb
import urllib
import requests
from socket import error as SocketError
import commands
from ConfigDB.api import storage
from urllib2 import URLError
from ConfigDB.secmon_notify import attributes as attr
import configfile
import inspect
# LOG = configfile.configlogging()

def get_association(resource, row_id):
    """function to get association for collector/collectorset resource

    Args:
        resource: collector/collectorset
        row_id: row id of collector/collectorset

    Returns:
        association: association for collector/collectorset
    """
    association = []
    record = storage.plugin.get_record(resource, row_id)
    if record:
        record_dict = ast.literal_eval(record)
        association = attr.PLUGIN_ASSOCIATION_MAPPING[str(record_dict[attr.COL_TYPE])]
    configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + " association name fetched based on id is : " + str(association))
    return association


def fetch_secondary_id(table_name, secondary_key, secondary_ids, primary_key):
    """function to fetch data from resource based on secondary key

    Args:
        table_name: name of the resource 
        secondary_key: secondary key name
        secondary_ids: list of secondary ids
        primary_key: primary key name

    Returns:
        primary_id_list: list of primary ids of fetched records
    """
    primary_id_list = []
    for secondary_id in secondary_ids:
        records = storage.plugin.get_records_by_secondary_index(table_name,
                                                                secondary_key,
                                                                secondary_id)
        if records is not None:
            for record in records:
                record_dict = ast.literal_eval(record)
                primary_id_list.append((record_dict[attr.PRIMARY_ID]))
    configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + " primary id list generated based on secondary id is : " + str(primary_id_list))
    return primary_id_list


def get_collectorset_id(collector_id):
    """function to get collectorset id from collector id

    Args:
        collector_id: id of collector
    Returns:
        collectorset id
    """
    records = storage.plugin.get_records(attr.COLLECTORSET)
#    pdb.set_trace()
    if records is not None:
        for record in records:
            record_dict = ast.literal_eval(record)
            collector_list_str = record_dict[attr.COLLECTOR_IDS]
            collector_list = ast.literal_eval(collector_list_str)
            for collector_dict in collector_list:
                if str(collector_id) == collector_dict[attr.PRIMARY_ID]:
                    configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + " collectorset id based on collector id is : " + str(record_dict[attr.PRIMARY_ID]))
                    return record_dict[attr.PRIMARY_ID]
    configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + " no collectorset id found")
    return None


def process_delete_association(row_data, **data):
    """function to send notification for delete association

    Args:
        row_data: data of deleted association
        data: data dict with row_id, operation and resource name

    Returns:
        success or failure
    """
    scope_id = row_data[attr.SCOPE_ID]
    scope_ids = []
    scope_ids.append((str(scope_id)))
    return_list = fetch_secondary_id(attr.SECMONDETAILS,
                                     attr.SCOPE_NAME,
                                     scope_ids, 
                                     attr.PRIMARY_ID)
    configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + "secmondetails data based on scope name is " + str(return_list))
    if return_list is not None:
        return_value = get_secmon_info_and_send_notification(return_list,
                                                             **data)


def process_for_each_association_table(secondary_ids, **data):
    """Function to send notification for policy updation.

    Args:
        secondary_ids: list of policy ids
        data: data dict

    Returns:
        success or failure 
    """
    return_list = fetch_secondary_id(attr.NETFLOWASSOCIATION, attr.POLICY_ID,
                                     secondary_ids,
                                     attr.PRIMARY_ID)
    configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + "netflowassociation primary id list based on policy id is " + str(return_list))
    if return_list:
        return_value = process_for_each_associatin_id(attr.NETFLOWASSOCIATION,
                                                      return_list, **data)

    return_list = fetch_secondary_id(attr.SFLOWASSOCIATION,
                                     attr.POLICY_ID,
                                     secondary_ids, attr.PRIMARY_ID)
    configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + "sflowassociation primary id list based on policy id is " + str(return_list))
    if return_list:
        return_value = process_for_each_associatin_id(attr.SFLOWASSOCIATION,
                                                      return_list, **data)

    return_list = fetch_secondary_id(attr.RAWFORWARDASSOCIATION,
                                     attr.POLICY_ID,
                                     secondary_ids, attr.PRIMARY_ID)
    configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + "rawforwardassociation primary id list based on policy id is " + str(return_list))
    if return_list:
        return_value = process_for_each_associatin_id(
                                               attr.RAWFORWARDASSOCIATION,
                                               return_list,
                                               **data)


def process_for_each_associatin_id(association_name, secondary_ids, **data):
    """Function to get scope id from association and send notification
       based on details fetched from secmon details.

    Args:
        association_name: name of association to get scope from
        secondary_ids: list of association ids
        data: data dict

    Returns:
        success or failure
    """
    for association_id in secondary_ids:
        scope_ids = []
        scope_data = storage.plugin.get_record(association_name,
                                               association_id)
        print("scope_data in process_for_each_associatin_id:", scope_data)
        if scope_data:
            record_dict = ast.literal_eval(scope_data)
            if association_name == attr.NOTIFICATION:
                scope_ids.append((record_dict[attr.ROW_ID]))
            else:
                scope_ids.append((record_dict[attr.SCOPE_ID]))
            return_list = fetch_secondary_id(attr.SECMONDETAILS,
                                             attr.SCOPE_NAME,
                                             scope_ids, attr.PRIMARY_ID)
            if return_list is not None:
                if association_name == attr.NOTIFICATION:
                    record_dict['resource'] = record_dict['table_name']
                    del record_dict['table_name']
                    return_value = get_secmon_info_and_send_notification(
                                                              return_list,
                                                              **record_dict)
                else:
                    return_value = get_secmon_info_and_send_notification(
                                                              return_list,
                                                              **data)


def get_secmon_info_and_send_notification(scope_ids, **json_data):
    """Function to send notification to the secmon

    Args:
        scope_ids: list of scope ids
        json_data: data dict

    Returns:
        success or Failure
    """
#    print("inside get_secmon_info_and_send_notification, json_data:", json_data)
    json_data1 = {}
    for scope_id in scope_ids:
        scope_data = storage.plugin.get_record(attr.SECMONDETAILS, scope_id)
        if scope_data is not None:
            json_data1 = '{"table_name":"'+json_data['resource']+'","row_id":"'+json_data['row_id']+'",'+'"operation":"'+json_data['operation']+'"'+'}'
            if 'policies' in json_data:
                json_data1 = '{"table_name":"'+json_data['resource']+'","row_id":"'+json_data['row_id']+'",'+'"operation":"'+json_data['operation']+'",'+'"policies":"'+json_data['policies']+'"'+'}'
            record_dict = ast.literal_eval(scope_data)
            data = str(json_data1)
            ip_address1 = record_dict[attr.IP_ADDRESS]
            port1 = record_dict[attr.PORT]
            secmon_url = 'http://' + str(ip_address1) + ':' + str(port1) + '/'
            configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + " url of secmon to sent notification to : " + secmon_url)
            configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + " data to be sent to secmon: " + str(data))
            request_headers = {"Content-Type": "application/json", }
            try:
                req = urllib2.Request(secmon_url,
                                      data, headers=request_headers)
                req.get_method = lambda: 'POST'
                f = urllib2.urlopen(req).read()
                if f == 'success':
                    configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + " Sending notification: Success")
                else:
                    configfile.logging_obj.info(__file__ + ' ' + str(inspect.stack()[0][2]) + " Sending notification: Failed")
            except SocketError as e:
                if e.errno != errno.ECONNRESET:
                    configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + " Conncetion reset by peer")
            except URLError:
                configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + " no connection")
