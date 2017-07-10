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


from unittest import TestCase

import consul

import services.api.storage_plugin.consul_io.consul_config as cfg
from services.api.storage_plugin.consul_io.consul_io import ConsulIO


class TestRecord(object):
    """Consul test record object"""

    def __init__(self, id, name, email, description):
        self.id = id
        self.name = name
        self.email = email
        self.description = description

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ConsulTestCase(TestCase):
    """Test case for store, get, delete operations of Consul Plugin"""

    def setUp(self):
        self.c = consul.Consul(host=cfg.CONSUL_HOST, port=cfg.CONSUL_PORT,
                               consistency=cfg.CONSUL_CONSISTENCY)
        self.consul = ConsulIO()
        self.consul.relations = {
                'test': {
                    'primary_key': 'id',
                    'secondary_keys': ['name', 'email'],
                }
        }

        self.relation = 'test'
        self.test_record = TestRecord('732',
                                      'rec1',
                                      'rec1@consul.com',
                                      'Rec 1')

        self.primary_index_value = '732'
        self.primary_index = 'test/id/732'
        self.secondary_index_name = 'test/name/rec1/id/732'
        self.secondary_index_email = 'test/email/rec1@consul.com/id/732'

        # Store the test record in storage except for consul 'put' operation
        if not self._testMethodName.startswith('test_put'):
            self.c.kv.put(self.primary_index,
                          str(self.test_record.__dict__))
            self.c.kv.put(self.secondary_index_name, self.primary_index)
            self.c.kv.put(self.secondary_index_email, self.primary_index)

    def tearDown(self):
        # Delete the test record in consul and revert consul to original state.
        self.c.kv.delete(self.primary_index)
        self.c.kv.delete(self.secondary_index_name)
        self.c.kv.delete(self.secondary_index_email)

    def test_put_record(self):
        """Test case to store a consul record"""
        self.consul.put_record(self.relation, self.test_record)
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
        record_object = TestRecord(**record)
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
        records_obj = [TestRecord(**record) for record in records]
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
            record_object = TestRecord(**record)
            self.assertEqual(record_object, self.test_record)

        records = self.consul.get_records_by_secondary_index(
                self.relation,
                'email',
                self.test_record.email)

        for record in records:
            record_object = TestRecord(**record)
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
    # TODO: More test cases can be tried with other combination of arguments

    def test_delete_record(self):
        """Test case to delete a consul record with invalid id."""
        self.consul.delete_record(self.relation, self.test_record)

        index, primary_data = self.c.kv.get(self.primary_index)
        self.assertIsNone(primary_data)

        index, secondary_data_name = self.c.kv.get(self.secondary_index_name)
        self.assertIsNone(secondary_data_name)

        index, secondary_data_email = self.c.kv.get(self.secondary_index_email)
        self.assertIsNone(secondary_data_email)

    def test_delete_record_with_invalid_arguments(self):
        """Test case to delete a consul record with invalid arguments."""
        with self.assertRaises(TypeError):
            self.consul.delete_record(None, None)

        with self.assertRaises(TypeError):
            self.consul.delete_record(None, self.test_record)

        with self.assertRaises(TypeError):
            self.consul.delete_record(self.relation, None)

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
        self.consul.relations = {
                'test': {
                    'primary_key': 'id',
                    'secondary_keys': ['name', 'email'],
                }
        }
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
        self.assertFalse(record)  # Empty list evaluate to False

    def test_get_records_no_record(self):
        """Test case to get all consul records with no record present in the
        relation."""
        record = self.consul.get_records(self.relation)
        self.assertFalse(record)  # Empty list evaluate to False

