import json
import logging
from unittest import TestCase

from ConfigDB.api.exceptions import ResourceNotFound, IDUpdateNotPermitted
from ConfigDB.api.serializers.serializers_collectorset import CollectorSet
from ConfigDB.api.serializers.serializers_collectorset \
        import CollectorSetSerializer
from ConfigDB.api.utils import generate_uuid

logging.basicConfig(filename='ConfigAgent_log.log')
LOG = logging.getLogger('ConfigAgent_log')


class TestCollectorSetNoRecord(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_save_None_record(self):
        """Test case to save None record."""
        with self.assertRaises(TypeError):
            CollectorSet().save()

    def test_get_no_record(self):
        """Test case to fetch a CollectorSet with invalid id."""
        with self.assertRaises(ResourceNotFound):
            CollectorSet.get(generate_uuid())

    def test_get_all_no_record(self):
        """Test case to fetch all CollectorSet with no records present."""
        with self.assertRaises(ResourceNotFound):
            CollectorSet.get_all()

    def test_delete_no_record(self):
        """Test case to delete an invalid CollectorSet record."""
        with self.assertRaises(ResourceNotFound):
            CollectorSet().delete()


class TestCollectorSetSerializer(TestCase):

    def setUp(self):
        self.uuid = generate_uuid()   # Generate an id except for POST
        self.uuid1 = generate_uuid()  # Generate id for update

        self.data1 = [{'id': self.uuid1,
                      'name': 'collectorset1',
                      'collector_ids': "[{'id':'87a3f7c1-88bc-4a4e-ba12-b87bb6878fa0','weight':20}, {'id':'87a3f7c1-88bc-4a4e-ba12-b87bb6878fa0','weight':20}]",
                      'col_type': 'rawforward',
                      'lb_algo': 1,
                      }]

        self.data = [{'id': self.uuid,
                       'name': 'collectorset2',
                       'collector_ids': "[{'id':'8aefba80-e99d-4d9c-8b99-6c1a7049135b','weight':30}, {'id':'a016ff9e-2e6f-4db9-8ba4-cd0529407e7b','weight':40}]",
                       'col_type': 'netflow',
                       'lb_algo': 2,
                       }]
        self.data2 = [{'id': self.uuid,
                       'name': 'collectorset2',
                       'collector_ids': "[{'id':'87a3f7c1-88bc-4a4e-ba12-b87bb6878fa0','weight':20}, {'id':'87a3f7c1-88bc-4a4e-ba12-b87bb6878fa0','weight':20}]",
                       'col_type': 'rawforward',
                       'lb_algo': 0,
                       }]

        print("inside setup function")
        self.data3 = [{}]

        serializer_data = json.loads(json.dumps(self.data))
#        print("serializer_data:", serializer_data[0])
        serializer = CollectorSetSerializer(data=serializer_data[0])
#        print("serializer.data:", serializer.data)
        if serializer.valid(self.uuid):
#            print("serializer.data in setup:", serializer.data)
            serializer.create(serializer.data)
        else:
            print("serializer data is not valid")

    def tearDown(self):
        record = CollectorSet.get(self.uuid)
        record.delete()
        if self._testMethodName.startswith('test_post_data'):
            record1 = CollectorSet.get(self.uuid1)
            record1.delete()

    def test_post_data(self):
        """test case to test create function with valid data"""
#        print("inside test_post_data")
        serializer_data1 = json.loads(json.dumps(self.data1))
        serializer = CollectorSetSerializer(data=serializer_data1[0])
#        print("serializer.data in test_post_data:", serializer.data)
        if serializer.valid(self.uuid1):
            serializer.create(serializer.data)
        else:
            print("serializer data is not valid")
        self.assertEqual(serializer_data1[0], serializer.data)

    def test_post_with_invalid_data(self):
        """test case to test create function with invalid data"""
        serializer = CollectorSetSerializer(data=None)
        if serializer.valid(self.uuid):
            with self.assertRaises(TypeError):
                serializer.create(serializer.data)

    def test_update_id(self):
        """test case to test update function with id update"""
#        print("inside test_update_id")
        obj = CollectorSet.get(self.uuid)
        serializer_data1 = json.loads(json.dumps(self.data1))
        with self.assertRaises(IDUpdateNotPermitted):
            serializer = CollectorSetSerializer(obj,
                                                data=serializer_data1[0],
                                                partial=True,
                                                context={'pk': self.uuid1})
            serializer.update(obj, serializer_data1[0])

    def test_put_Data(self):
        """test case to test update function with valid data"""
        obj = CollectorSet.get(self.uuid)
        serializer_data2 = json.loads(json.dumps(self.data2))
        serializer = CollectorSetSerializer(obj,
                                            data=serializer_data2[0],
                                            partial=True,
                                            context={'pk': self.uuid})
        serializer.update(obj, serializer_data2[0])
        serializerdata2 = serializer_data2[0]
        serializerdata2['id'] = self.uuid
        self.assertEqual(serializerdata2, serializer.data)

    def test_valid_serializer(self):
        """test case to test valid function with valid serializer"""
#        print("inside test_valid_serializer")
        serializer_data1 = json.loads(json.dumps(self.data1))
        serializer = CollectorSetSerializer(data=serializer_data1[0])
        self.assertEqual(serializer.valid(self.uuid), True)

    def test_invalid_serializer_with_pk(self):
        """test case to test valid function with invalid serializer with pk"""
        record = CollectorSet.get(self.uuid)
        serializer = CollectorSetSerializer(record)
        self.assertEqual(serializer.valid(self.uuid), False)

    def test_invalid_serializer_without_pk(self):
        """test case to test valid function with invalid serializer without pk
        """
        record = CollectorSet.get(self.uuid)
        serializer = CollectorSetSerializer(record)
        self.assertEqual(serializer.valid(None), False)
