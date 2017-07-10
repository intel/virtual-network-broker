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
import fnmatch
import logging
import six
import consul
from yapsy.IPlugin import IPlugin

import consul_config as cfg
import configfile
import inspect
# LOG = configfile.configlogging()


class ConsulIO(IPlugin):
    """This a plugin to store configuration or other data in
    backend with Consul(https://www.consul.io/docs/agent/http/kv.html).

       Consul store records in the KV(Key/Value) pair.

       The configuration or user data is modelled in KV pair before
       storing in Consul as below:

       Key = relation_name/primary_index_name/primary_index_value
       Value = Record tuple in JSON/str/BLOB format

       To illustrate above, consider a relation/table 'policy'
       with 'id' as primary index. And a record tuple in the relation
       'policy' as
       below:

       {
         "id":"fc5221be-b9d0-11e5-8338-005056b46cff",
         "name":"policy_1",
         "version":"v1"
       }

       For the above record, the Consul KV pair will look as:

       Key = policy/id/fc5221be-b9d0-11e5-8338-005056b46cff

       Value = '{"id":"fc5221be-b9d0-11e5-8338-005056b46cff",
                 "name":"policy_1", "version":"v1"}'


       Secondary Index(es):
       In addition, to help retrieve the stored record with other than
       primary   index, we also prepare and store additional Consul
       record(s) as below:

       Key = relation_name/secondary_index_name/secondary_index_value/ /
             primary_index_name/primary_index_value
       Value = relation_name/primary_index_name/primary_index_value

       To illustrate this part, suppose one of the secondary index of
       relation 'policy' is 'name'. Then the KV Pair for this will
       look like below:

       Key = policy/name/policy_1/id/ /
             fc5221be-b9d0-11e5-8338-005056b46cff
       Value = policy/id/fc5221be-b9d0-11e5-8338-005056b46cff

       A relation could have multiple secondary indexes. So for every
       record, we store this KV pair for each secondary index.

       Relation Name and Primary and Secondary Index:
       The primary index and secondary index(es) for each relation is
       defined in the consul_config module.

    Note:
       This module uses the Python client of Consul to perform KV
       operations
       (http://python-consul.readthedocs.org/en/latest/)
       Installation : pip install python-consul

    """

    def __init__(self):
        super(ConsulIO, self).__init__()
        self.connection = consul.Consul(host=cfg.CONSUL_HOST,
                                        port=cfg.CONSUL_PORT,
                                        consistency=cfg.CONSUL_CONSISTENCY)

    def put_record(self, relation_name, record):
        """Store a record in Consul

        Args:
            relation_name (str): Name of the relation/table
            record (object) : Relation/Table record

        Returns:
            None

        Raises:
            TypeError : If relation_name is not a 'string' type and/or
                record is None
        """
        if not isinstance(relation_name, basestring) or (record is None):
            raise TypeError
        records = self.get_records(relation_name)
        self._store_record_in_consul(relation_name, record)

    def get_record(self, relation_name, field_value):
        """Retrieve a record from Consul with the required primary
        index value

        Args:
            relation_name (str): Name of the relation/table
            field_value (str) : Primary index value

        Returns:
            A record with matching primary index value

        Raises:
            TypeError : If passed arguments are not of 'string' type
        """
        if not isinstance(relation_name, basestring) or \
                not isinstance(field_value, basestring):
            raise TypeError

        # Find the Primary Index of the relation
        field = self._get_relation_index(relation_name, 'primary')

        # Prepare the key in the required format
        # e.g. policy/id/fc5221be-b9d0-11e5-8338-005056b46cff
        key = relation_name + '/' + field + '/' + field_value

        # Fetch the record with the prepared key
        consul_index, data = self.connection.kv.get(key)
#        print("data['Value']:", data['Value'])
        if data is not None:
            return data['Value']
        else:
            return None

    def get_records_by_secondary_index(self, relation_name, secondary_index,
                                       field_value):
        """Retrieve a list of record for a secondary index from a
        relation

        Args:
            relation_name (str): Name of the relation/table
            secondary_index (str) : Required secondary index
            field_value (str) : Secondary index value

        Returns:
            None or List of records with the given secondary index
            value in the relation.

        Raises:
            TypeError : If passed arguments are not of 'string' type
        """
        if not isinstance(relation_name, basestring) or \
                not isinstance(secondary_index, basestring) or \
                not isinstance(field_value, basestring):
            raise TypeError
        # Prepare the key prefix with secondary index in the required
        # format
        # e.g. policy/name/policy_1
        key = relation_name + '/' + secondary_index + '/' + field_value
        # Find the primary index value for the given secondary index
        # value
        consul_index, data = self.connection.kv.get(key, recurse=True)
        if not data:
            return None

        primary_index_records = [record['Value'] for record in data]

        if primary_index_records is None:
            return None

        records = []
        # Fetch the record with the primary index value
        for primary_index in primary_index_records:
            consul_index, data = self.connection.kv.get(primary_index)
            # LOG.debug(data)
            # Prepare a list of all the Consul records' 'Value' field
            if data is not None:
                records.append(data['Value'])
        return records

    def get_records(self, relation_name):
        """Retrieve list of all records of a relation/table.

        Args:
            relation_name (str): Name of the relation/table

        Returns:
            list of all records in the relation.

        Raises:
            TypeError : If passed argument is not of 'string' type
        """
        if not isinstance(relation_name, basestring):
            raise TypeError

        # Find the primary index of the relation
        field = self._get_relation_index(relation_name, 'primary')

        # Prepare the prefix of the Consul key in the required format
        # e.g. policy/id/
        key = relation_name + '/' + field + '/'

        # Retrieve the list of all records from Consul
        # Note : 'recurse=True' option fetches all the record with the
        #   given key prefix
        consul_index, data = self.connection.kv.get(key, recurse=True)

        if data is None:
            return None

        # Prepare a list of all the Consul record 'Value' field
        records = [record['Value'] for record in data]

        return records

    def delete_record(self, relation_name, record):
        """Delete the given record.

        Args:
            relation_name (str): Name of the relation/table
            record (object) : Relation/Table record

        Returns:
            None

        Raises:
           RuntimeError : Fail to store data in Consul
           TypeError : If relation_name is not a 'string' type and/or
                record is None
        """
#        print("relation_name in delete_record:", relation_name)
#        print("record indelete_record:", record)
        return_value = False
        if not isinstance(relation_name, basestring) or (record is None):
            raise TypeError
        # Find the primary index of the relation
        primary_index = self._get_relation_index(relation_name, 'primary')

        # find dependency table list for the relation
        dependency_tables = self._get_relation_index(relation_name,
                                                     'DEPENDENCY')
        if dependency_tables:
            for dependency_table in dependency_tables:
                # check if any record exist in dependency table for
                # this record id
                return_value = self.check_dependency(relation_name,
                                                     getattr(record,
                                                             primary_index),
                                                     dependency_table)
                if return_value:
                    configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + " Record cannot be deleted as it is associated with another row")
                    raise RuntimeError
        # Prepare the key in the required format
        key = relation_name + '/' + primary_index + '/' + \
                  getattr(record, primary_index)
        # Delete the KV pair in Consul
        self.connection.kv.delete(key)

        index, data = self.connection.kv.get(key)
        if data is not None:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + ' unable to delete data based on primary key')
            raise RuntimeError

        # Also delete the secondary index(es) records from Consul
        secondary_index = self._get_relation_index(relation_name, 'secondary')
        for index in secondary_index:
            key_prefix = relation_name + '/' + index + '/' + \
                         getattr(record, index) + '/' + primary_index + '/' + \
                         getattr(record, primary_index)

            self.connection.kv.delete(key_prefix)
            si_value = getattr(record, index)
            sub_si_values = si_value.split(',')
            while len(sub_si_values):
                sub_si_value = sub_si_values.pop()
                key_prefix = relation_name + '/' + index + '/' + \
                    sub_si_value + '/' + primary_index + '/' + \
                    getattr(record, primary_index)

                self.connection.kv.delete(key_prefix)

            index, data = self.connection.kv.get(key_prefix)
            if data is not None:
                configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + " Unable to delete record based on secondary key")
                raise RuntimeError

    def check_dependency(self, relation_name, record_id, dependency_table):
        """Check if dependency exist in dependency_table for record_id.

        Args:
            relation_name (str): Name of the relation/table
            record_id (str): Value of secondary key(index)
            dependency_table (str): Name of dependency table

        Returns:
            (bool)

        """
        if 'collector' == relation_name:
            if dependency_table == 'collectorset':
                return self.check_dependency_in_collectorset(record_id)
            row_id = 'Collector:' + record_id
            secondary_index = 'collector_id'
        elif 'collectorset' == relation_name:
            row_id = 'Collectorset:' + record_id
            secondary_index = 'collector_id'
        else:
            row_id = record_id
            secondary_index = relation_name + '_id'
        data = self.get_records_by_secondary_index(dependency_table,
                                                   secondary_index, row_id)
        if data is None:
            configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + ' no dependency exist')
            return False
        else:
            return True

    def check_dependency_in_collectorset(self, record_id):
        """ 
        """
        records =  self.get_records('collectorset')
        if records is not None:
            for record in records:
                record_data = eval(record)
                collectors_data = ast.literal_eval(record_data['collector_ids'])
                for collector_data in collectors_data:
                    if collector_data['id'] == record_id:
                        return True
        configfile.logging_obj.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + ' no dependency exist in collectorset')
        return False

    def check_key(self, relation_name, primary_index_value):
        """Check if a value is primary index in the relation/table.

        Args:
            relation_name (str): Name of the relation/table
            primary_index_value (str): Value of primary key(index)

        Returns:
            (bool)

        Raises:
            TypeError : If passed argument is not of 'string' type
            ValueError : If index_type is not 'primary'
        """
        if not isinstance(relation_name, basestring) or \
                not isinstance(primary_index_value, basestring):
            raise TypeError

        # Find the primary index of the relation
        field = self._get_relation_index(relation_name, 'primary')

        # Prepare the prefix of the Consul key in the required format
        # e.g. policy/id/
        key = relation_name + '/' + field + '/' + primary_index_value

        # Check for the key in relation
        # Note : 'key=True' only fetches key without value
        consul_index, data = self.connection.kv.get(key, keys=True)

        if data is None:
            return False
        else:
            return True

    def put_kv(self, key, value=' '):
        """Store a Key/Value pair in Consul

        Args:
            key (str): Key
            value (str) : Value , Defaults to ' '.

        Returns:
            None

        Raises:
            TypeError : If Key or Value is not a 'string' type
            RuntimeError : Fail to store KV in Consul
        """
        if (not isinstance(key, six.string_types) or
                not isinstance(key, six.string_types)):
            raise TypeError

        rvalue = self.connection.kv.put(key, value)

        if rvalue is None:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + " Unable to store KV pair in Consul")
            raise RuntimeError

    def get_kv(self, key):
        """Fetch the Value for the  Key in Consul

        Args:
            key (str): Key

        Returns:
            None

        Raises:
            TypeError : If Key is not a 'string' type
            RuntimeError : Fail to get data from Consul
        """
        if not isinstance(key, six.string_types):
            raise TypeError

        consul_index, data = self.connection.kv.get(key)

        if data is None:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + " Unable to get Value for the Key in Consul")
            return None

        return data['Value']

    def delete_kv(self, key, recurse=False):
        """Delete the Key/Value pair for the  Key in Consul

        Args:
            key (str): Key
            recurse(bool): whether delete recursively for with the key prefix

        Returns:
            None

        Raises:
            TypeError : If Key is not a 'string' type
            RuntimeError : Fail to get data from Consul
        """
        if not isinstance(key, six.string_types):
            raise TypeError

        # Delete the KV pair in Consul
        self.connection.kv.delete(key, recurse=recurse)

        index, data = self.connection.kv.get(key, recurse=recurse)

        if data is not None:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + " Unable to delete record in Consul")
            raise RuntimeError

    def _store_record_in_consul(self, relation_name, record):
        """Store record in the Consul with primary index(primary_index) as the
        'key' and the record in JSON format as the 'value'.

        Args:
            relation_name (str): Name of the relation/table
            record (Any relation record object) : Relation/Table
                                                    record

        Returns:
            None

         Raises:
           RuntimeError : Fail to store data in Consul
        """
        # Find the primary index of the relation
        primary_index = self._get_relation_index(relation_name, 'primary')

        # Prepare the key in the required format
        # e.g. policy/id/fc5221be-b9d0-11e5-8338-005056b46cff
        key = relation_name + '/' + primary_index + '/' + \
            getattr(record, primary_index)

        # Convert the object into JSON(dict)
        value = str(record.__dict__)

        # Store secondary indexes in Consul
        self._prepare_secondary_indices(relation_name, record)
        # store tertiary indexes in consul
#        self._prepare_tertiary_indices(relation_name, record)
        # Store KV pair in Consul
        rvalue = self.connection.kv.put(key, value)
        if rvalue is None:
            configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) +  ' Unable to store record in Consul')
            raise RuntimeError

    def _prepare_secondary_indices(self, relation_name, record):
        """Store each secondary index of the relation/table along with
        primary index value for the record. The list of secondary
        index is present in the consul_config.

       Args:
           relation_name (str): Name of the relation/table
           record (Any relation record object) : Relation/Table record

       Returns:
           None

       Raises:
           RuntimeError : Fail to store data in Consul
       """
        # Find the primary index of the relation
        primary_index = self._get_relation_index(relation_name, 'primary')

        # Prepare the Consul value
        value = relation_name + '/' + primary_index + '/' + \
            getattr(record, primary_index)

        # Find the list of Secondary Index
        si_list = self._get_relation_index(relation_name, 'secondary')
        for secondary_index in si_list:
            # Adding primary index value to the key helps in storing
            # multiple values for same index.

            # For update(PUT/PATCH) operation of secondary index(es),
            # first delete the existing secondary index Consul record
            key_prefix = relation_name + '/' + secondary_index + '/'
            key_suffix = primary_index + '/' + getattr(record, primary_index)
            consul_index, data = self.connection.kv.get(key_prefix,
                                                        keys=True,
                                                        recurse=True)
            if data is not None:
                regex = key_prefix + '*' + '/' + key_suffix
                match_key = fnmatch.filter(data, regex)
                #LOG.debug(__file__ + ' ' + str(inspect.stack()[0][2]) + ' ' + match_key)
                if match_key:
                    self.connection.kv.delete(match_key[0])

            # Store secondary index in Consul
            si_value = getattr(record, secondary_index)
            key = key_prefix + str(si_value) + '/' + key_suffix
            rvalue = self.connection.kv.put(key, value)
            sub_si_values = si_value.split(',')
            while len(sub_si_values):
                sub_si_value = sub_si_values.pop()
                key = key_prefix + str(sub_si_value) + '/' + key_suffix
                rvalue = self.connection.kv.put(key, value)
            if rvalue is None:
                configfile.logging_obj.error(__file__ + ' ' + str(inspect.stack()[0][2]) + ' Unable to store secondary index in Consul')
                raise RuntimeError

    def _get_relation_index(self, relation_name, index_type):
        """Find the primary index or list of secondary index of
        relation from the consul_config.

        Args:
            relation_name (str): Name of the relation/table
            index_type (str): Type of index = 'primary' or 'secondary'

        Returns:
        Primary index or list of secondary index
        """
        relation_dict_name = self._relation_dict_from_config(relation_name)
        relation_dict = getattr(cfg, relation_dict_name)
        index = relation_dict[index_type.upper()]
        return index

    @staticmethod
    def _relation_dict_from_config(relation_name):
        """Prepare the relation dict name in the format specified in
        consul_config.

        Args:
            relation_name (str): Name of the relation/table

        Returns:
            Concatenation of RELATION_ and name of the relation
        """
        return 'RELATION_' + relation_name.upper()
