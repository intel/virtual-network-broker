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
import unittest
from unittest import TestCase

import consul
import ConfigDB.api.storage_plugin.consul_io.consul_config as cfg
from ConfigDB.api.storage_plugin.consul_io.consul_io import ConsulIO
from ConfigDB.api.utils import str_to_dict

import sys


class TestRecord(object):
    """Consul test record object"""

    def __init__(self, id, name, email, description):
        self.id = id
        self.name = name
        self.email = email
        self.description = description

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class TestRecord1(object):
    """Consul test record1 object"""

    def __init__(self, id, test_id):
        self.id = id
        self.test_id = test_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class TestRecordCollector(object):
    """Consul test record for collector object"""

    def __init__(self, id, name, ip_address, udp_port,
                 col_type, encapsulation_protocol):
        self.id = id
        self.name = name
        self.ip_address = ip_address
        self.udp_port = udp_port
        self.col_type = col_type
        self.encapsulation_protocol = encapsulation_protocol

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class TestRecordCollectorSet(object):
    """Consul test record1 object"""

    def __init__(self, id, name, collector_ids, col_type, association):
        self.id = id
        self.name = name
        self.collector_ids = collector_ids
        self.col_type = col_type
        self.association = association

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class TestRecordRawAssociation(object):
    """Consul test record association object"""

    def __init__(self, id, originator_vm_id, collector_id,
                 direction, policy_id, scope_id):
        self.id = id
        self.originator_vm_id = originator_vm_id
        self.collector_id = collector_id
        self.direction = direction
        self.policy_id = policy_id
        self.scope_id = scope_id


class ConsulTestCase(TestCase):
    """Test case for store, get, delete operations of Consul Plugin"""

    def setUp(self):
        self.c = consul.Consul(host=cfg.CONSUL_HOST, port=cfg.CONSUL_PORT,
                               consistency=cfg.CONSUL_CONSISTENCY)
        self.consul = ConsulIO()

        self.relation = 'test'
        self.test_record = TestRecord('732',
                                      'rec1',
                                      'rec1@consul.com',
                                      'Rec 1')
        self.relation1 = 'test1'
        self.test_record1 = TestRecord1('123',
                                        '732')

        self.relationcollector = 'collector'
        self.test_recordcollector = TestRecordCollector('1234',
                                                        'col',
                                                        '10.204.0.11',
                                                        2055,
                                                        'rawforward',
                                                        'udp')

        self.relationassociation = 'rawforwardassociation'
        self.test_recordrawassociation = TestRecordRawAssociation(
                                                              '543',
                                                              '423',
                                                              'Collector:1234',
                                                              'INGRESS',
                                                              '785',
                                                              '243')

        self.primary_index_value = '732'
        self.primary_index = 'test/id/732'
        self.secondary_index_name = 'test/name/rec1/id/732'
        self.secondary_index_email = 'test/email/rec1@consul.com/id/732'

        self.primary_index_value_col = '1234'
        self.primary_index_col = 'collector/id/1234'
        self.secondary_index_col_type = 'collector/col_type/rawforward/id/1234'

        self.primary_index_value_raw = '543'
        self.primary_index_raw = 'rawforwardassociation/id/543'
        self.secondary_index_scope_id = 'rawforwardassociation/scope_id/243/id/543'
        self.secondary_index_collector_id = 'rawforwardassociation/collector_id/Collector:1234/id/543'
        self.secondary_index_policy_id = 'rawforwardassociation/policy_id/785/id/543'

        self.primary_index_value1 = '123'
        self.primary_index1 = 'test1/id/123'
        self.secondary_index_test_id = 'test1/test_id/732/id/123'

        # Store the test record in storage except for consul 'put' operation
        if not self._testMethodName.startswith('test_put'):
            self.c.kv.put(self.primary_index,
                          str(self.test_record.__dict__))
            self.c.kv.put(self.secondary_index_name, self.primary_index)
            self.c.kv.put(self.secondary_index_email, self.primary_index)

            self.c.kv.put(self.primary_index1,
                          str(self.test_record1.__dict__))
            self.c.kv.put(self.secondary_index_test_id, self.primary_index1)

            self.c.kv.put(self.primary_index_col,
                          str(self.test_recordcollector.__dict__))
            self.c.kv.put(self.secondary_index_col_type,
                          self.primary_index_col)

            self.c.kv.put(self.primary_index_raw,
                          str(self.test_recordrawassociation.__dict__))
            self.c.kv.put(self.secondary_index_scope_id,
                          self.primary_index_raw)
            self.c.kv.put(self.secondary_index_policy_id,
                          self.primary_index_raw)
            self.c.kv.put(self.secondary_index_collector_id,
                          self.primary_index_raw)

    def tearDown(self):
        # Delete the test record in consul and revert consul to original state
        self.c.kv.delete(self.primary_index1)
        self.c.kv.delete(self.secondary_index_test_id)

        self.c.kv.delete(self.primary_index_col)
        self.c.kv.delete(self.secondary_index_col_type)

        self.c.kv.delete(self.primary_index_raw)
        self.c.kv.delete(self.secondary_index_scope_id)
        self.c.kv.delete(self.secondary_index_policy_id)
        self.c.kv.delete(self.secondary_index_collector_id)

        self.c.kv.delete(self.primary_index)
        self.c.kv.delete(self.secondary_index_name)
        self.c.kv.delete(self.secondary_index_email)

    def test_put_record(self):
        """Test case to store a consul record"""
        self.consul.put_record(self.relation, self.test_record)
        self.consul.put_record(self.relation1, self.test_record1)
        index, primary_data = self.c.kv.get(self.primary_index)
        self.assertEqual(primary_data['Value'], str(self.test_record.__dict__))

        index, secondary_data_name = self.c.kv.get(self.secondary_index_name)
        self.assertEqual(secondary_data_name['Value'], self.primary_index)

        index, secondary_data_email = self.c.kv.get(self.secondary_index_email)
        self.assertEqual(secondary_data_email['Value'], self.primary_index)

    def test_put_record_with_invalid_arguments(self):
        """Test case to store a consul record with invalid arguments"""
        with self.assertRaises(TypeError):
            self.consul.put_record(None, None)

        with self.assertRaises(TypeError):
            self.consul.put_record(None, self.test_record)

        with self.assertRaises(TypeError):
            self.consul.put_record(self.relation, None)

    def test_get_record(self):
        """Test case to get a consul record by primary index"""
        record = self.consul.get_record(self.relation, self.test_record.id)
        record_object = TestRecord(**str_to_dict(record))
        self.assertEqual(record_object, self.test_record)

    def test_get_record_with_invalid_arguments(self):
        """Test case to get a consul record by primary index with invalid
        arguments"""
        with self.assertRaises(TypeError):
            self.consul.get_record(None, None)

        with self.assertRaises(TypeError):
            self.consul.get_record(None, self.primary_index)

        with self.assertRaises(TypeError):
            self.consul.get_record(self.relation, None)

    def test_get_records(self):
        """Test case to get consul records by primary index"""
        records = self.consul.get_records(self.relation)
        records_obj = [TestRecord(**str_to_dict(record)) for record in records]
        self.assertTrue(self.test_record in records_obj)

    def test_get_records_with_invalid_arguments(self):
        """Test case to get consul records by primary index with invalid
        arguments"""
        with self.assertRaises(TypeError):
            self.consul.get_records(None)

    def test_get_records_by_secondary_index(self):
        """Test case to get consul records by secondary index"""
        records = self.consul.get_records_by_secondary_index(
                self.relation,
                'name',
                self.test_record.name)

        for record in records:
            record_object = TestRecord(**str_to_dict(record))
            self.assertEqual(record_object, self.test_record)

        records = self.consul.get_records_by_secondary_index(
                self.relation,
                'email',
                self.test_record.email)

        for record in records:
            record_object = TestRecord(**str_to_dict(record))
            self.assertEqual(record_object, self.test_record)

    def test_get_records_by_secondary_index_with_invalid_arguments(self):
        """Test case to get consul records by secondary index with invalid
        arguments."""

        with self.assertRaises(TypeError):
            self.consul.get_records_by_secondary_index(None, None, None)

        with self.assertRaises(TypeError):
            self.consul.get_records_by_secondary_index(self.relation, None,
                                                       None)

        with self.assertRaises(TypeError):
            self.consul.get_records_by_secondary_index(None, 'name', None)

        with self.assertRaises(TypeError):
            self.consul.get_records_by_secondary_index(
                                                      self.relation,
                                                      None,
                                                      self.primary_index_value)
            # TODO: More test cases can be tried with other
            # combination of arguments

    def test_delete_record(self):
        """Test case to delete a consul record with invalid id."""
        self.consul.delete_record(self.relation1, self.test_record1)

        index, primary_data = self.c.kv.get(self.primary_index1)
        self.assertIsNone(primary_data)

        index, secondary_data_test_id = self.c.kv.get(
                                                  self.secondary_index_test_id)
        self.assertIsNone(secondary_data_test_id)

#       index, secondary_data_email = self.c.kv.get(self.secondary_index_email)
#       self.assertIsNone(secondary_data_email)

    def test_delete_record_with_invalid_arguments(self):
        """Test case to delete a consul record with invalid arguments."""
        with self.assertRaises(TypeError):
            self.consul.delete_record(None, None)

        with self.assertRaises(TypeError):
            self.consul.delete_record(None, self.test_record)

        with self.assertRaises(TypeError):
            self.consul.delete_record(self.relation, None)

    def test_delete_record_with_dependency(self):
        """test case to delete a record with existing dependency
        """
        with self.assertRaises(RuntimeError):
            self.consul.delete_record(self.relation, self.test_record)

#        with self.assertRaises(RuntimeError):
#            self.consul.delete_record(self.relationcollector,
#                                      self.test_recordcollector)

    def test_check_key(self):
        """Test case to check a primary key belongs to the relation"""
        self.assertTrue(self.consul.check_key(self.relation,
                                              self.primary_index_value))
        self.assertFalse(self.consul.check_key(self.relation,
                                               '123'))

    def test_check_key_with_invalid_arguments(self):
        """Test case to check a primary key exists in the relation
        with invalid arguments."""
        with self.assertRaises(TypeError):
            self.consul.check_key(None, None)

        with self.assertRaises(TypeError):
            self.consul.check_key(None, self.id)

        with self.assertRaises(TypeError):
            self.consul.check_key(self.relation, None)


class ConsulTestCaseNoRecord(TestCase):
    """Test case for get & delete operations on consul record(s) with no
    record present in the relation"""

    def setUp(self):
        self.c = consul.Consul()
        self.consul = ConsulIO()

        self.relation = 'test'
        self.test_record = TestRecord('732',
                                      'rec1',
                                      'rec1@consul.com',
                                      'Rec 1')
        self.primary_index = 'test/id/732'
        self.secondary_index_name = 'test/name/rec1/id/732'
        self.secondary_index_email = 'test/email/rec1@consul.com/id/732'

    def tearDown(self):
        pass

    def test_get_record_no_record(self):
        """Test case to get a consul record with invalid id."""
        record = self.consul.get_record(self.relation, self.test_record.id)
        self.assertIsNone(record)

    def test_get_records_no_record(self):
        """Test case to get all consul records with no record present in the
        relation."""
        record = self.consul.get_records(self.relation)
        self.assertIsNone(record)

if __name__ == '__main__':
    print(sys.path)
    unittest.main()
