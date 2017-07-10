import json
import logging
from unittest import TestCase

from ConfigDB.api.exceptions import ResourceNotFound, IDUpdateNotPermitted
from ConfigDB.api.serializers.serializers_collector import Collector
from ConfigDB.api.serializers.serializers_collector import CollectorSerializer
from ConfigDB.api.utils import generate_uuid

logging.basicConfig(filename='ConfigAgent_log.log')
LOG = logging.getLogger('ConfigAgent_log')


class TestCollectorNoRecord(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_None_record(self):
        """Test case to create None record."""
        serializer = CollectorSerializer(data=None)
        with self.assertRaises(TypeError):
            serializer.create(None)

    def test_update_no_record(self):
        """Test case to update a Collector with None record."""
        serializer = CollectorSerializer(data=None)
        collector = Collector()
        with self.assertRaises(TypeError):
            serializer.update(collector, None)


class TestCollectorSerializer(TestCase):

    def setUp(self):

        self.uuid = generate_uuid()  # Generate an id except for POST
        self.uuid1 = generate_uuid()  # Generate id for update

        self.data = [{'id': self.uuid,
                      'name': 'collector1',
                      'ip_address': '10.42.0.11',
                      'udp_port': 2055,
                      'col_type': 'rawforward',
                      'encapsulation_protocol': 'udp',
                      }]

        self.data1 = [{'id': self.uuid1,
                       'name': 'collector2',
                       'ip_address': '10.42.0.12',
                       'udp_port': 2056,
                       'col_type': 'netflow',
                       }]
        self.data2 = [{'id': self.uuid,
                       'name': 'collector2',
                       'ip_address': '10.42.0.12',
                       'udp_port': 2057,
                       'col_type': 'rawforward',
                       'encapsulation_protocol': 'udp',
                       }]

        self.data3 = [{}]

        serializer_data = json.loads(json.dumps(self.data))
#        for serializerdata in serializer_data:
        serializer = CollectorSerializer(data=serializer_data[0])
        if serializer.valid(self.uuid):
            serializer.create(serializer.data)

    def tearDown(self):
        record = Collector.get(self.uuid)
        record.delete()
        if self._testMethodName.startswith('test_post_data'):
            record1 = Collector.get(self.uuid1)
            record1.delete()

    def test_post_data(self):
        """test case to test create function with valid data"""
        serializer_data1 = json.loads(json.dumps(self.data1))
        serializerdata1 = serializer_data1[0]
        serializer = CollectorSerializer(data=serializerdata1)
        if serializer.valid(self.uuid1):
            serializer.create(serializer.data)
        else:
            print("serializer data is not valid")
        serializerdata1['encapsulation_protocol'] = ''
        self.assertEqual(serializerdata1, serializer.data)

    def test_post_with_invalid_data(self):
        """test case to test create function with invalid data"""
        serializer_data1 = json.loads(json.dumps(self.data1))
        serializer = CollectorSerializer(data=serializer_data1[0])
        if serializer.valid(self.uuid):
            with self.assertRaises(TypeError):
                serializer.create(None)

    def test_update_id(self):
        """test case to test update function with id update"""
        obj = Collector.get(self.uuid)
        serializer_data1 = json.loads(json.dumps(self.data1))
        with self.assertRaises(IDUpdateNotPermitted):
            serializer = CollectorSerializer(obj,
                                             data=serializer_data1[0],
                                             partial=True,
                                             context={'pk': self.uuid1})
            serializer.update(obj, serializer_data1[0])

    def test_put_with_invalid_Data(self):
        obj = Collector.get(self.uuid)
        serializer_data3 = json.loads(json.dumps(self.data3))
        serializer = CollectorSerializer(obj,
                                         data=serializer_data3[0],
                                         partial=True,
                                         context={'pk': self.uuid})
        with self.assertRaises(TypeError):
            serializer.update(obj, None)

    def test_put_Data(self):
        """test case to test update function with valid data"""
        obj = Collector.get(self.uuid)
        serializer_data2 = json.loads(json.dumps(self.data2))
        serializer = CollectorSerializer(obj,
                                         data=serializer_data2[0],
                                         partial=True,
                                         context={'pk': self.uuid})
        serializer.update(obj, serializer_data2[0])
        serializerdata2 = serializer_data2[0]
        serializerdata2['id'] = self.uuid
        self.assertEqual(serializerdata2, serializer.data)

    def test_valid_serializer(self):
        """test case to test valid function with valid serializer"""
        serializer_data1 = json.loads(json.dumps(self.data1))
        serializer = CollectorSerializer(data=serializer_data1[0])
        self.assertEqual(serializer.valid(self.uuid), True)

    def test_invalid_serializer_with_pk(self):
        """test case to test valid function with invalid serializer with pk"""
        record = Collector.get(self.uuid)
        serializer = CollectorSerializer(record)
        self.assertEqual(serializer.valid(self.uuid), False)

    def test_invalid_serializer_without_pk(self):
        """test case to test valid function with invalid serializer without pk
        """
        record = Collector.get(self.uuid)
        serializer = CollectorSerializer(record)
        self.assertEqual(serializer.valid(None), False)
