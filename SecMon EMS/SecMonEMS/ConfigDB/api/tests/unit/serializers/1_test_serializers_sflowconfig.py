import json
import logging
from unittest import TestCase

from ConfigDB.api.exceptions import ResourceNotFound, IDUpdateNotPermitted
from ConfigDB.api.serializers.serializers_sflowconfig import SflowConfig
from ConfigDB.api.serializers.serializers_sflowconfig \
         import SflowConfigSerializer
from ConfigDB.api.utils import generate_uuid

logging.basicConfig(filename='ConfigAgent_log.log')
LOG = logging.getLogger('ConfigAgent_log')


class TestSflowConfigRecord(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_save_None_record(self):
        """Test case to save None record."""
        with self.assertRaises(TypeError):
            SflowConfig().save()

    def test_get_no_record(self):
        """Test case to fetch a SlowConfig with invalid id."""
        with self.assertRaises(ResourceNotFound):
            SflowConfig.get(generate_uuid())

    def test_get_all_no_record(self):
        """Test case to fetch all SFlowConfig with no records present."""
        with self.assertRaises(ResourceNotFound):
            SflowConfig.get_all()

    def test_delete_no_record(self):
        """Test case to delete an invalid SlowConfig record."""
        with self.assertRaises(ResourceNotFound):
            SflowConfig().delete()


class TestSflowConfigSerializer(TestCase):

    def setUp(self):

        self.uuid = generate_uuid()   # Generate an id except for POST
        self.uuid1 = generate_uuid()  # Generate id for update

        self.data = [{'id': self.uuid,
                      'scope_id': '04df6a37-cf8e-4511-9387-f78325336776',
                      'agent_ip': '10.204.21.91',
                      'agent_subid': 0,
                      'sampling_rate': 20,
                      'truncate_to_size': 128,
                      }]

        self.data1 = [{'id': self.uuid1,
                       'scope_id': '04df6a37-cf8e-4511-9387-f78325336776',
                       'agent_ip': '10.204.21.19',
                       'agent_subid': 0,
                       'sampling_rate': 30,
                       'truncate_to_size': 320,
                       }]

        self.data2 = [{'id': self.uuid,
                       'scope_id': '04df6a37-cf8e-4511-9387-f78325336776',
                       'agent_ip': '10.204.21.96',
                       'agent_subid': 1,
                       'sampling_rate': 40,
                       'truncate_to_size': 128,
                       }]

        self.data3 = [{}]

        serializer_data = json.loads(json.dumps(self.data))
#        for serializerdata in serializer_data:
        serializer = SflowConfigSerializer(data=serializer_data[0])
        if serializer.valid(self.uuid):
            serializer.create(serializer.data)

    def tearDown(self):
        record = SflowConfig.get(self.uuid)
        record.delete()
        if self._testMethodName.startswith('test_post_data'):
            record1 = SflowConfig.get(self.uuid1)
            record1.delete()

    def test_post_data(self):
        """test case to test create function with valid data"""
        serializer_data1 = json.loads(json.dumps(self.data1))
#        for serializerdata1 in serializer_data1:
        serializer = SflowConfigSerializer(data=serializer_data1[0])
        if serializer.valid(self.uuid1):
            serializer.create(serializer.data)
        else:
            print("serializer data is not valid")
        self.assertEqual(serializer_data1[0], serializer.data)

    def test_post_with_invalid_data(self):
        """test case to test create function with invalid data"""
#        serializer_data3 = json.loads(json.dumps(self.data3))
#        for serializerdata3 in serializer_data3:
        serializer = SflowConfigSerializer(data=None)
        if serializer.valid(self.uuid):
            with self.assertRaises(TypeError):
                serializer.create(serializer.data)
#        self.assertEqual(serializerdata1, serializer.data)

    def test_update_id(self):
        """test case to test update function with id update"""
        obj = SflowConfig.get(self.uuid)
        serializer_data1 = json.loads(json.dumps(self.data1))
#        for serializerdata1 in serializer_data1:
        with self.assertRaises(IDUpdateNotPermitted):
            serializer = SflowConfigSerializer(obj,
                                               data=serializer_data1[0],
                                               partial=True,
                                               context={'pk': self.uuid1})
            serializer.update(obj, serializer_data1[0])

#    def test_put_with_invalid_Data(self):
#        obj = SflowConfig.get(self.uuid)
#        serializer_data3 = json.loads(json.dumps(self.data3))
#        for serializerdata3 in serializer_data3:
#            print("checking for exception")
#            with self.assertRaises(TypeError):
#                serializer = SflowConfigSerializer(obj,
#                                                   data=serializerdata3,
#                                                   partial=True,
#                                                   context={'pk': self.uuid})
#                serializer.update(obj, serializerdata3)

    def test_put_Data(self):
        """test case to test update function with valid data"""
        obj = SflowConfig.get(self.uuid)
        serializer_data2 = json.loads(json.dumps(self.data2))
#        for serializerdata2 in serializer_data2:
        serializer = SflowConfigSerializer(obj,
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
#        for serializerdata1 in serializer_data1:
        serializer = SflowConfigSerializer(data=serializer_data1[0])
        self.assertEqual(serializer.valid(self.uuid), True)

#        self.assertEqual(serializer.valid(self.uuid),True)

    def test_invalid_serializer_with_pk(self):
        """test case to test valid function with invalid serializer with pk"""
        record = SflowConfig.get(self.uuid)
        serializer = SflowConfigSerializer(record)
        self.assertEqual(serializer.valid(self.uuid), False)

    def test_invalid_serializer_without_pk(self):
        """test case to test valid function with invalid serializer without pk
        """
        record = SflowConfig.get(self.uuid)
        serializer = SflowConfigSerializer(record)
        self.assertEqual(serializer.valid(None), False)
