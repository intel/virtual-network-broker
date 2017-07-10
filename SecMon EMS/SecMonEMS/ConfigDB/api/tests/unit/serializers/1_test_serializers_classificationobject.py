import json
import logging
from unittest import TestCase

from ConfigDB.api.exceptions import ResourceNotFound, IDUpdateNotPermitted
from ConfigDB.api.serializers.serializers_classificationobject \
        import ClassificationObject
from ConfigDB.api.serializers.serializers_classificationobject \
        import ClassificationObjectSerializer
from ConfigDB.api.utils import generate_uuid

logging.basicConfig(filename='ConfigAgent_log.log')
LOG = logging.getLogger('ConfigAgent_log')


class TestClassificationObjectNoRecord(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_save_None_record(self):
        """Test case to save None record."""
        with self.assertRaises(TypeError):
            ClassificationObject().save()

    def test_get_no_record(self):
        """Test case to fetch a ClassificationObject with invalid id."""
        with self.assertRaises(ResourceNotFound):
            ClassificationObject.get(generate_uuid())

    def test_get_all_no_record(self):
        """Test case to fetch all ClassificationObject with no records present
        """
        with self.assertRaises(ResourceNotFound):
            ClassificationObject.get_all()

    def test_delete_no_record(self):
        """Test case to delete an invalid ClassificationObject record."""
        with self.assertRaises(ResourceNotFound):
            ClassificationObject().delete()


class TestClassificationObjectSerializer(TestCase):

    def setUp(self):
        self.uuid = generate_uuid()   # Generate an id except for POST
        self.uuid1 = generate_uuid()  # Generate id for update

        self.data = [{'id': self.uuid,
                      'name': 'classificationobject1',
                      'src_ip': '10.42.0.11',
                      'src_mac': '00:A0:C9:14:C8:29',
                      'src_ip_subnet': 24,
                      'minimum_src_port': 1,
                      'maximum_src_port': 30000,
                      'dst_ip': '10.42.0.15',
                      'dst_mac': '00:A0:C9:14:C8:45',
                      'dst_ip_subnet': 24,
                      'minimum_dst_port': 1,
                      'maximum_dst_port': 20000,
                      'protocol': 17,
                      }]

        self.data1 = [{'id': self.uuid1,
                       'name': 'classificationobject2',
                       'src_ip': '10.42.0.13',
                       'src_mac': '00:A0:C9:14:C8:18',
                       'src_ip_subnet': 24,
                       'minimum_src_port': 1,
                       'maximum_src_port': 25000,
                       'dst_ip': '10.42.0.14',
                       'dst_mac': '00:A0:C9:14:C8:d4',
                       'dst_ip_subnet': 24,
                       'minimum_dst_port': 1,
                       'maximum_dst_port': 35000,
                       'protocol': 17,
                       }]
        self.data2 = [{'id': self.uuid,
                       'name': 'classificationobject3',
                       'src_ip': '10.42..0.103',
                       'src_mac': '00:A0:C9:14:C8:2b',
                       'src_ip_subnet': 24,
                       'minimum_src_port': 1,
                       'maximum_src_port': 25000,
                       'dst_ip': '10.42.0.15',
                       'dst_mac': '00:A0:C9:14:C8:2c',
                       'dst_ip_subnet': 24,
                       'minimum_dst_port': 1,
                       'maximum_dst_port': 20000,
                       'protocol': 1,
                       }]

        self.data3 = [{}]

        serializer_data = json.loads(json.dumps(self.data))
        print("serializer_data in setup:", serializer_data)
#        for serializerdata in serializer_data:
        serializer = ClassificationObjectSerializer(data=serializer_data[0])
        if serializer.valid(self.uuid):
            serializer.create(serializer.data)

    def tearDown(self):
        record = ClassificationObject.get(self.uuid)
        record.delete()
        if self._testMethodName.startswith('test_post_data'):
            record1 = ClassificationObject.get(self.uuid1)
            record1.delete()

    def test_post_data(self):
        """test case to test create function with valid data"""
        serializer_data1 = json.loads(json.dumps(self.data1))
#        for serializerdata1 in serializer_data1:
        serializer = ClassificationObjectSerializer(data=serializer_data1[0])
        if serializer.valid(self.uuid1):
            serializer.create(serializer.data)
        else:
            print("serializer data is not valid")
        self.assertEqual(serializer_data1[0], serializer.data)

    def test_post_with_invalid_data(self):
        """test case to test create function with invalid data"""
#        serializer_data3 = json.loads(json.dumps(self.data3))
#        for serializerdata3 in serializer_data3:
        serializer = ClassificationObjectSerializer(data=None)
        if serializer.valid(self.uuid):
            with self.assertRaises(TypeError):
                serializer.create(serializer.data)
#        self.assertEqual(serializerdata1, serializer.data)

    def test_update_id(self):
        """test case to test update function with id update"""
        obj = ClassificationObject.get(self.uuid)
        serializer_data1 = json.loads(json.dumps(self.data1))
#        for serializerdata1 in serializer_data1:
        with self.assertRaises(IDUpdateNotPermitted):
            serializer = ClassificationObjectSerializer(
                                                    obj,
                                                    data=serializer_data1[0],
                                                    partial=True,
                                                    context={'pk': self.uuid1}
                                                        )
            serializer.update(obj, serializer_data1[0])

#    def test_put_with_invalid_Data(self):
#        obj = NetFlowConfig.get(self.uuid)
#        serializer_data3 = json.loads(json.dumps(self.data3))
#        for serializerdata3 in serializer_data3:
#            print("checking for exception")
#            with self.assertRaises(TypeError):
#                serializer = NetFlowConfigSerializer(obj,
#                                                    data=serializerdata3,
#                                                    partial=True,
#                                                    context={'pk': self.uuid})
#                serializer.update(obj, serializerdata3)

    def test_put_Data(self):
        """test case to test update function with valid data"""
        obj = ClassificationObject.get(self.uuid)
        serializer_data2 = json.loads(json.dumps(self.data2))
#        for serializerdata2 in serializer_data2:
        serializer = ClassificationObjectSerializer(obj,
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
        serializer = ClassificationObjectSerializer(data=serializer_data1[0])
        self.assertEqual(serializer.valid(self.uuid), True)

#        self.assertEqual(serializer.valid(self.uuid),True)

    def test_invalid_serializer_with_pk(self):
        """test case to test valid function with invalid serializer with pk"""
        record = ClassificationObject.get(self.uuid)
        serializer = ClassificationObjectSerializer(record)
        self.assertEqual(serializer.valid(self.uuid), False)

    def test_invalid_serializer_without_pk(self):
        """test case to test valid function with invalid serializer without pk
        """
        record = ClassificationObject.get(self.uuid)
        serializer = ClassificationObjectSerializer(record)
        self.assertEqual(serializer.valid(None), False)
