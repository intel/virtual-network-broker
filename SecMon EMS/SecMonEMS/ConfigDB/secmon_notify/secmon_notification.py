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

import itertools
import pdb
from ConfigDB.api import storage
from ConfigDB.secmon_notify import utils
from ConfigDB.secmon_notify import attributes
from ConfigDB.secmon_notify import attributes as attr
import configfile
import inspect
#LOG = configfile.configlogging()

PLUGIN_ASSOCIATION_MAPPING = {'netflow': 'netflowassociation',
                              'sflow': 'sflowassociation',
                              'rawforward': 'rawforwardassociation'}


class SecMonUpdateNotification(object):

    @classmethod
    def record_update(cls, **kwargs):
        print("kwargs details in secmon_notification:", kwargs)
        resource = kwargs.get('resource')
        row_id = kwargs.get('row_id')
        operation = kwargs.get('operation')
        if operation == 'DELETE':
            row_data = kwargs.get('row_data')
            cls._nonbind_record_update(row_id, resource, operation, row_data)
        else:
            cls._nonbind_record_update(row_id, resource, operation)

    @staticmethod
    def _nonbind_record_update(row_id, resource, operation, row_data=None):
        """Update of a Non VPNBIND record

        Check all the VPNBIND records to find if any record has
        reference to this Non-VPNBIND Record. If a reference exists,
        then notify all the IPsecEnforcer(s) using the VPNBIND record
        configurations.

        Args:
            record_id (str): id of the updated record(resource)
            resource (str): name of the resource
        """
        secondary_id = []
        data = {'row_id': row_id, 'resource': resource, 'operation': operation}
#        pdb.set_trace()
        configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + ' notification data received:' + str(data))
        if resource == attr.COLLECTOR:
            collectorset_id = ''
            collectorset_id_list = []
            secondary_ids = 'Collector:' + row_id
            association_name = utils.get_association(attr.COLLECTOR, row_id)
            if association_name:
                secondary_id.append((secondary_ids))
                return_list = utils.fetch_secondary_id(association_name,
                                                       attr.COLLECTOR_ID,
                                                       secondary_id,
                                                       attr.PRIMARY_ID,
                                                       )
                if return_list:
                    utils.process_for_each_associatin_id(association_name,
                                                         return_list,
                                                         **data
                                                         )
                else:
                    collectorset_id = utils.get_collectorset_id(row_id)
                    if collectorset_id is not None:
                        collectorset_id = 'Collectorset:' + collectorset_id
                        collectorset_id_list.append((collectorset_id))
                        return_list = utils.fetch_secondary_id(
                                                         association_name,
                                                         attr.COLLECTOR_ID,
                                                         collectorset_id_list,
                                                         attr.PRIMARY_ID,
                                                              )
                        if return_list:
                            utils.process_for_each_associatin_id(
                                                    association_name,
                                                    return_list,
                                                    **data
                                                                 )
        elif resource == attr.COLLECTORSET:
            secondary_ids = 'Collectorset:' + row_id
            association_name = utils.get_association(attr.COLLECTORSET,
                                                     row_id)
            if association_name:
                secondary_id.append((secondary_ids))
                return_list = utils.fetch_secondary_id(association_name,
                                                       attr.COLLECTOR_ID,
                                                       secondary_id,
                                                       attr.PRIMARY_ID,
                                                       )
                if return_list:
                    utils.process_for_each_associatin_id(association_name,
                                                         return_list,
                                                         **data
                                                         )
        elif resource == attr.NETFLOWASSOCIATION:
            secondary_ids = row_id
            association_name = attr.NETFLOWASSOCIATION
            if operation != attr.DELETE:
                secondary_id.append((secondary_ids))
                utils.process_for_each_associatin_id(association_name,
                                                     secondary_id,
                                                     **data)
            else:
                utils.process_delete_association(row_data,
                                                 **data
                                                 )
        elif resource == attr.NETFLOWCONFIG:
            secondary_ids = row_id
            secondary_id.append((secondary_ids))
            association_name = attr.NETFLOWCONFIG
            utils.process_for_each_associatin_id(association_name,
                                                 secondary_id,
                                                 **data
                                                 )
        elif resource == attr.NETFLOWMONITOR:
            secondary_ids = row_id
            secondary_id.append((secondary_ids))
            association_name = attr.NETFLOWMONITOR
            utils.process_for_each_associatin_id(association_name,
                                                 secondary_id,
                                                 **data
                                                 )
        elif resource == attr.SFLOWCONFIG:
            secondary_ids = row_id
            secondary_id.append((secondary_ids))
            association_name = attr.SFLOWCONFIG
            utils.process_for_each_associatin_id(association_name,
                                                 secondary_id,
                                                 **data
                                                 )
        elif resource == attr.SFLOWASSOCIATION:
            secondary_ids = row_id
            association_name = attr.SFLOWASSOCIATION
            if operation != attr.DELETE:
                secondary_id.append((secondary_ids))
                utils.process_for_each_associatin_id(association_name,
                                                     secondary_id,
                                                     **data
                                                     )
            else:
                utils.process_delete_association(row_data,
                                                 **data
                                                 )
        elif resource == attr.RAWFORWARDASSOCIATION:
            secondary_ids = row_id
            association_name = attr.RAWFORWARDASSOCIATION
            if operation != attr.DELETE:
                secondary_id.append((secondary_ids))
                utils.process_for_each_associatin_id(association_name,
                                                     secondary_id,
                                                     **data
                                                     )
            else:
                utils.process_delete_association(row_data,
                                                 **data
                                                 )
        elif resource == attr.CLASSIFICATIONOBJECT:
            secondary_ids = row_id
            policies_list = []
            secondary_id.append((secondary_ids))
            return_list = utils.fetch_secondary_id(attr.RULEOBJECT,
                                                   attr.CLASSIFICATION_ID,
                                                   secondary_id,
                                                   attr.PRIMARY_ID
                                                   )
            if return_list:
                return_list1 = utils.fetch_secondary_id(attr.POLICY,
                                                        attr.RULEOBJECT_ID,
                                                        return_list,
                                                        attr.PRIMARY_ID
                                                        )
                if return_list1:
                    policies = ",".join(return_list1)
                    data[attr.POLICIES] = policies
                    utils.process_for_each_association_table(return_list1,
                                                             **data
                                                             )
        elif resource == attr.RULEOBJECT:
            secondary_ids = row_id
            policies = ''
            policies_list = []
            secondary_id.append((secondary_ids))
            return_list = utils.fetch_secondary_id(attr.POLICY,
                                                   attr.RULEOBJECT_ID,
                                                   secondary_id,
                                                   attr.PRIMARY_ID
                                                   )
            if return_list:
                policies = ",".join(return_list)
                data[attr.POLICIES] = policies
                utils.process_for_each_association_table(return_list,
                                                         **data
                                                         )
        elif resource == attr.POLICY:
            secondary_ids = row_id
            association_name = attr.POLICY
            secondary_id.append((secondary_ids))
            utils.process_for_each_association_table(secondary_id,
                                                     **data
                                                     )
        elif resource == attr.SCOPE:
            secondary_ids = row_id
            secondary_id.append((secondary_ids))
            return_list = utils.fetch_secondary_id(attr.SECMONDETAILS,
                                                   attr.SCOPE_NAME,
                                                   secondary_id,
                                                   attr.PRIMARY_ID
                                                   )
            if return_list:
                utils.get_secmon_info_and_send_notification(return_list,
                                                            **data)
        elif resource == attr.NOTIFICATION:
            print("inside notification change")
            secondary_ids = row_id
            secondary_id.append((secondary_ids))
            association_name = attr.NOTIFICATION
            utils.process_for_each_associatin_id(association_name,
                                                 secondary_id,
                                                 **data
                                                 )            
