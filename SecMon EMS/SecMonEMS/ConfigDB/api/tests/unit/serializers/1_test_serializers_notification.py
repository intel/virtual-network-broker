import json
import logging
from unittest import TestCase

from ConfigDB.api.exceptions import ResourceNotFound, IDUpdateNotPermitted
from ConfigDB.api.serializers.serializers_notification import Notification
from ConfigDB.api.serializers.serializers_notification \
        import NotificationSerializer
from ConfigDB.api.utils import generate_uuid

logging.basicConfig(filename='ConfigAgent_log.log')
LOG = logging.getLogger('ConfigAgent_log')


class TestNotificationNoRecord(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_save_None_record(self):
        """Test case to save None record."""
        with self.assertRaises(TypeError):
            Notification().save()

    def test_get_no_record(self):
        """Test case to fetch a  Notification with invalid id."""
        with self.assertRaises(ResourceNotFound):
            Notification.get(generate_uuid())

    def test_get_all_no_record(self):
        """Test case to fetch all  Notification with no records present."""
#        print("inside test_get_all_no_record:", Notification.get_all())
        with self.assertRaises(ResourceNotFound):
            Notification.get_all()

    def test_delete_no_record(self):
        """Test case to delete an invalid  Notification record."""
        with self.assertRaises(ResourceNotFound):
            Notification().delete()


class TestNotificationSerializer(TestCase):

    def setUp(self):
        self.uuid = generate_uuid()   # Generate an id except for POST
        self.uuid1 = generate_uuid()  # Generate id for update

        self.data = [{'id': self.uuid,
                      'table_name': 'netflowconfig',
                      'row_id': '72231461-aae9-4059-a5f1-7934ba969d3c',
                      'operation': 'PUT',
                      }]

        self.data1 = [{'id': self.uuid1,
                       'table_name': 'netflowconfig',
                       'row_id': '04df6a37-cf8e-4511-9387-f78325336776',
                       'operation': 'PUT',
                       }]
        self.data2 = [{'id': self.uuid,
                       'table_name': 'collector',
                       'row_id': '33264640-302f-456c-ac0e-f06cc13a6a47',
                       'operation': 'DELETE',
                       'row_data': {
                           u'name': u'nfcol2', u'udp_port': 2055,
                           u'encapsulation_protocol': u'',
                           u'col_type': u'netflow',
                           u'ip_address': u'172.16.98.11',
                           u'id': u'be2e94b6-9a36-4ec4-a763-87bb486f06b8'},
                       }]

        self.data3 = [{}]
#        print("inside notification setup:", Notification.get_all())
        serializer_data = json.loads(json.dumps(self.data))
#        for serializerdata in serializer_data:
        serializer = NotificationSerializer(data=serializer_data[0])
        if serializer.valid(self.uuid):
            serializer.create(serializer.data)

    def tearDown(self):
        record = Notification.get(self.uuid)
        record.delete()
        if self._testMethodName.startswith('test_post_data'):
            record1 = Notification.get(self.uuid1)
            record1.delete()

    def test_post_data(self):
        """test case to test create function with valid data"""
        serializer_data1 = json.loads(json.dumps(self.data1))
#        for serializerdata1 in serializer_data1:
        serializer = NotificationSerializer(data=serializer_data1[0])
        if serializer.valid(self.uuid1):
            serializer.create(serializer.data)
        else:
            print("serializer data is not valid")
        serializer_data1[0]['row_data'] = None
        self.assertEqual(serializer_data1[0], serializer.data)

    def test_post_with_invalid_data(self):
        """test case to test create function with invalid data"""
#        serializer_data3 = json.loads(json.dumps(self.data3))
#        for serializerdata3 in serializer_data3:
        serializer = NotificationSerializer(data=None)
        if serializer.valid(self.uuid):
            with self.assertRaises(TypeError):
                serializer.create(serializer.data)
#        self.assertEqual(serializerdata1, serializer.data)

    def test_update_id(self):
        """test case to test update function with id update"""
        obj = Notification.get(self.uuid)
        serializer_data1 = json.loads(json.dumps(self.data1))
#        for serializerdata1 in serializer_data1:
        with self.assertRaises(IDUpdateNotPermitted):
            serializer = NotificationSerializer(obj,
                                                data=serializer_data1[0],
                                                partial=True,
                                                context={'pk': self.uuid1})
            serializer.update(obj, serializer_data1[0])

#    def test_put_with_invalid_Data(self):
#        obj =  Notification.get(self.uuid)
#        serializer_data3 = json.loads(json.dumps(self.data3))
#        for serializerdata3 in serializer_data3:
#            print("checking for exception")
#            with self.assertRaises(TypeError):
#                serializer = NotificationSerializer(obj,
#            data=serializerdata3, partial=True, context={'pk': self.uuid})
#            serializer.update(obj, serializerdata3)

    def test_put_Data(self):
        """test case to test update function with valid data"""
        obj = Notification.get(self.uuid)
        serializer_data2 = json.loads(json.dumps(self.data2))
#        for serializerdata2 in serializer_data2:
        serializer = NotificationSerializer(obj,
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
        serializer = NotificationSerializer(data=serializer_data1[0])
        self.assertEqual(serializer.valid(self.uuid), True)

#        self.assertEqual(serializer.valid(self.uuid),True)

    def test_invalid_serializer_with_pk(self):
        """test case to test valid function with invalid serializer with pk"""
        record = Notification.get(self.uuid)
        serializer = NotificationSerializer(record)
        self.assertEqual(serializer.valid(self.uuid), False)

    def test_invalid_serializer_without_pk(self):
        """test case to test valid function with invalid serializer without pk
        """
        record = Notification.get(self.uuid)
        serializer = NotificationSerializer(record)
        self.assertEqual(serializer.valid(None), False)
