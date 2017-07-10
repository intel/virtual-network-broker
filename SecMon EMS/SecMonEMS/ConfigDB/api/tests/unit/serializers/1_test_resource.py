import json
import logging
from unittest import TestCase

from ConfigDB.api.exceptions import ResourceNotFound, IDUpdateNotPermitted
from ConfigDB.api.utils import generate_uuid
from ConfigDB.api.serializers.serializers_collector import Collector
from ConfigDB.api.serializers.serializers_collector import CollectorSerializer

logging.basicConfig(filename='ConfigAgent_log.log')
LOG = logging.getLogger('ConfigAgent_log')


class TestCollectorNoRecord(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_save_None_record(self):
        """Test case to save None record."""
        with self.assertRaises(TypeError):
            Collector().save()

    def test_get_no_record(self):
        """Test case to fetch a Collector with invalid record"""
        with self.assertRaises(ResourceNotFound):
            Collector.get(None)

    def test_get_all_no_record(self):
        """Test case to fetch all Collector with no records present."""
        with self.assertRaises(ResourceNotFound):
            Collector.get_all()

    def test_delete_no_record(self):
        """Test case to delete an invalid Collector record."""
        with self.assertRaises(ResourceNotFound):
            Collector().delete()


class TestCollectorRecord(TestCase):

    def setUp(self):

        self.uuid = generate_uuid()  # Generate an id except for POST
        self.uuid1 = generate_uuid()  # Generate id for update

        self.data = {'id': self.uuid,
                     'name': u'nfcol1',
                     'ip_address': u'10.10.21.21',
                     'udp_port': 2055,
                     'col_type': u'netflow',
                     'encapsulation_protocol': u'',
                     }

        collector = Collector(**self.data)
        collector.save()

        self.data1 = {'id': self.uuid1,
                      'name': u'nfcol2',
                      'ip_address': u'10.10.21.21',
                      'udp_port': 2055,
                      'col_type': u'rawforward',
                      'encapsulation_protocol': u'udp',
                      }

        self.data2 = {}

        self.data3 = {'id': self.uuid,
                      'name': u'nfcol3',
                      'ip_address': u'10.42.0.21',
                      'udp_port': 6343,
                      'col_type': u'sflow',
                      'encapsulation_protocol': u'',
                      }

        self.listdata = []

    def tearDown(self):
        if not self._testMethodName.startswith('test_delete_valid'):
            record = Collector.get(self.uuid)
            record.delete()
        if self._testMethodName.startswith('test_save_valid'):
            record = Collector.get(self.uuid1)
            record.delete()
        if self._testMethodName.startswith('test_valid_serializer_create') or \
           self._testMethodName.startswith('test_valid_get_records'):
            record = Collector.get(self.uuid1)
            record.delete()

    def test_save_valid_record(self):
        """test case to save valid record"""
        collector = Collector(**self.data1)
        collector.save()
        record = Collector.get(self.uuid1)
        serializer = CollectorSerializer(record)
        self.assertEqual(self.data1, serializer.data)

    def test_save_invalid_record(self):
        """test case to test save with invalid record"""
        with self.assertRaises(TypeError):
            collector = Collector(**self.data2)
            collector.save()

    def test_update_valid_record(self):
        """test case to test update with valid record"""

    def test_delete_valid_record(self):
        """test case to test delete with valid record"""
        record2 = Collector.get(self.uuid)
        record2.delete()
        with self.assertRaises(ResourceNotFound):
            Collector.get(self.uuid)

    def test_delete_invalid_record(self):
        """test case to test delete with invalid record"""
        collector = Collector(**self.data2)
        with self.assertRaises(ResourceNotFound):
            collector.delete()

    def test_valid_get_record(self):
        """test case to test with valid record"""
        record = Collector.get(self.uuid)
        serializer = CollectorSerializer(record)
        self.assertEqual(self.data, serializer.data)

    def test_invalid_get_record(self):
        """test case to test get for invalid id"""
        with self.assertRaises(ResourceNotFound):
            Collector.get(generate_uuid())

    def test_valid_get_all_record(self):
        """test case to test get_all with valid record"""
        record = Collector.get_all()
        serializer = CollectorSerializer(record)
        self.listdata.append(self.data)
        self.assertEqual(self.listdata, serializer.data)

    def test_valid_get_records_by_secondary_index(self):
        """test case to test get records by secondary index with valid data"""
        collector = Collector(**self.data1)
        collector.save()
        records = collector.get_all_records_by_secondary_index('col_type',
                                                               'rawforward')
        serializer = CollectorSerializer(records)
        self.listdata.append(self.data1)
        self.assertEqual(self.listdata, serializer.data)

    def test_get_all_records_by_secondary_index_with_none_record(self):
        """test case to test get records by secondary index with None data"""
        collector = Collector(**self.data1)
        with self.assertRaises(TypeError):
            records = collector.get_all_records_by_secondary_index(None,
                                                                   'rawforward'
                                                                   )

        with self.assertRaises(TypeError):
            records = collector.get_all_records_by_secondary_index(None, None)

        with self.assertRaises(TypeError):
            records = collector.get_all_records_by_secondary_index('col_type',
                                                                   None)

    def test_invalid_get_all_records_by_secondary_index(self):
        """test case to test get records by secondary index with invalid data
        """
        collector = Collector(**self.data1)
        with self.assertRaises(ResourceNotFound):
            records = collector.get_all_records_by_secondary_index('name',
                                                                   'rawforward'
                                                                   )
#        self.assertEqual(records, None)
        with self.assertRaises(ResourceNotFound):
            records = collector.get_all_records_by_secondary_index('col_type',
                                                                   'col1')
#        self.assertEqual(records, None)
        with self.assertRaises(ResourceNotFound):
            records = collector.get_all_records_by_secondary_index('name',
                                                                   'col1')
#        self.assertEqual(records, None)

    def test_valid_serializer_create(self):
        """test case to test serializer_create with valid record"""
        record = Collector.serializer_create(self.data1)
        serializer = CollectorSerializer(record)
        self.assertEqual(self.data1, serializer.data)

    def test_invalid_serializer_create(self):
        """test case to test serializer_create with invalid record"""
        with self.assertRaises(TypeError):
            Collector.serializer_create(None)

    def test_valid_serializer_update(self):
        """test case to test serializer_update with valid record"""
        record = Collector.get(self.uuid)
        serializer = CollectorSerializer(record,
                                         data=self.data3,
                                         partial=True,
                                         context={'pk': self.uuid})
        Collector.serializer_update(serializer, record, self.data3)

        updated_data = Collector.get(self.uuid)
        updated_serializer = CollectorSerializer(updated_data)
        self.data3['id'] = self.uuid
        self.assertEqual(self.data3, updated_serializer.data)

    def test_invalid_serializer_update(self):
        """test case to test serializer_update with invalid record"""
        collector = Collector.get(self.uuid)
        with self.assertRaises(IDUpdateNotPermitted):
            serializer = CollectorSerializer(collector)
            record = Collector.serializer_update(serializer,
                                                 collector,
                                                 self.data1)

        with self.assertRaises(TypeError):
            record = Collector.serializer_update(serializer,
                                                 collector,
                                                 None)

    def test_valid_serializer(self):
        """test case to test serializer_valid with valid record"""
        serializer = CollectorSerializer(data=self.data3)
        return_value = Collector.serializer_valid(serializer,
                                                  self.uuid)
        self.assertEqual(return_value, True)

    def test_invalid_serializer(self):
        """test case to test serializer_valid"""
        serializer = CollectorSerializer(data=None)
        print("test case to test serializer_valid")
        return_value = Collector.serializer_valid(serializer,
                                                  None)
        self.assertEqual(return_value, False)

        return_value1 = Collector.serializer_valid(serializer,
                                                   self.uuid1)
        self.assertEqual(return_value1, False)
