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

import logging

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ConfigDB.api.serializers.serializers_collector import Collector
from ConfigDB.api.serializers.serializers_notification import Notification
from ConfigDB.api.utils import generate_uuid
from ConfigDB.api.utils import is_valid_uuid
from ConfigDB.api.utils import unicode_to_ascii_dict

LOG = logging.getLogger(__name__)


class TestCollectorCRUD(APITestCase):
    """Test case for CRUD operations on Collector"""

    def setUp(self):
        # Collector test record
        self.data = {
                     'name': 'nfcol1',
                     'ip_address': '10.10.21.21',
                     'udp_port': 2055,
                     'col_type': 'rawforward',
                     'encapsulation_protocol': 'udp',
                     }

        self.url_prefix = '/v1.0/secmon/collector/'
        self.notification_url_prefix = '/v1.0/secmon/notification/'
        # Store the test record in storage
        if not self._testMethodName.startswith('test_post_'):
            self.uuid = generate_uuid()  # Generate an id except for POST
            self.uuid1 = generate_uuid()
            self.data.update({'id': self.uuid})
            self.collector = Collector(**self.data)
            self.collector.save()

        # For POST & List,
        # Use the url with name 'collector_list' in urls.py file
        if self._testMethodName.startswith('test_post_') or \
                self._testMethodName.startswith('test_list_'):
            self.url = reverse('collector_list', kwargs={'version': 'v1.0',
                                                         'namespace': 'secmon'
                                                         })

    def tearDown(self):
        # Delete the test record in storage and revert storage to original
        # state.
        if self._testMethodName.startswith('test_put_notification'):
            if not self._testMethodName.endswith('invalid_value'):
                Notification.get(self.uuid1).delete()
        if self._testMethodName.startswith('test_notification_post'):
            Notification.get(self.uuid).delete()
        if self._testMethodName.startswith('test_post_'):
            if not self._testMethodName.endswith('invalid_values'):
                Collector.get(self.uuid).delete()  # Use 'id' of POST response
        else:
            self.collector.delete()

    def test_post_collector(self):
        """Test case to create Collector."""
        # No 'id' provided
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.uuid = response.data.pop('id')
        self.assertTrue(is_valid_uuid(self.uuid))
        self.assertEqual(unicode_to_ascii_dict(response.data),
                         unicode_to_ascii_dict(self.data))

    def test_notification_post(self):
        """Test case to create notification without id provided"""
        self.url = self.notification_url_prefix
        self.notification_data = {
            'table_name': 'collector1',
            'row_id': '33eb67b8-df63-4af5-b04a-97577a2477c1',
            'operation': 'PUT',
                                 }

        response = self.client.post(self.url, self.notification_data,
                                   format='json')
#        self.uuid1 = response.data.pop('id')
#        self.assertEqual(self.uuid1, '1')
        self.uuid = response.data.pop('id')
        self.assertTrue(is_valid_uuid(self.uuid))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.notification_data['row_data'] = None
        self.assertEqual(response.data,
                         self.notification_data)

    def test_put_notification_with_id(self):
        """Test case to create notification with id provided"""
        self.url = self.notification_url_prefix + self.uuid1 + '/'
        self.notification_data = {
            'id': self.uuid1,
            'table_name': 'collector2',
            'row_id': '33eb67b8-df63-4af5-b04a-97577a2477c1',
            'operation': 'PUT',
                                  }

        response = self.client.put(self.url, self.notification_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.notification_data['row_data'] = None
        self.notification_data['id'] = '1'
        self.uuid1 = '1'
        self.assertEqual(response.data,
                         self.notification_data)

    def test_put_notification_with_invalid_value(self):
        """Test case to test notification with invalid values"""
        self.url = self.notification_url_prefix + self.uuid + '/'
        self.notification_data = {
                                  'table_name': 'collector3',
                                  'row_id': '',
                                  'operation': 'PUT',
                                  }
        response = self.client.put(self.url, self.notification_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_notification_with_valid_id(self):
        """Test case to test delete notification with valid id"""
        # post notification before deleting 
        self.url = self.notification_url_prefix + '1/'
        self.notification_data = {
            'table_name': 'collector4',
            'row_id': '33eb67b8-df63-4af5-b04a-97577a2477c1',
            'operation': 'PUT',
                                 }
        response = self.client.put(self.url, self.notification_data,
                                   format='json')

        # delete notification
        self.url = self.notification_url_prefix + '1/'
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_notification_with_invalid_id(self):
        """Test case to test delete notification with invalid id"""
        self.url = self.notification_url_prefix + self.uuid + '/'
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_collector_with_id(self):
        # 'id' provided
        self.uuid = generate_uuid()
        self.data.update({'id': self.uuid})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(unicode_to_ascii_dict(response.data),
                         unicode_to_ascii_dict(self.data))

    def test_post_collector_with_invalid_values(self):
        """Test case to create Collector with invalid values"""
        self._invalid_values = {
                                'name': 'collector2',
                                'ip_address': '10.42.0.12',
                                'udp_port': '80000',
                                'col_type': 'rawforward',
                                'encapsulation_protocol': 'sflow',
                               }

#        for update_value in self._invalid_values:
        self.data.update(self._invalid_values)
        response = self.client.post(self.url, self._invalid_values,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        LOG.debug(unicode_to_ascii_dict(response.data))

    def test_get_collector_from_valid_pk(self):
        """Test case to get collector from secondary key value"""
        self.test_response = []
        self.url = self.url_prefix + 'rawforward/'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_response.append(self.data)
        self.assertEqual(self.test_response, response.data)

    def test_get_collector_from_invalid_pk(self):
        """Test case to get collector from secondary key value"""
        self.url = self.url_prefix + 'sflow/'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_collector(self):
        """Test case to list all Collector."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(unicode_to_ascii_dict(self.data) in
                        unicode_to_ascii_dict(response.data))

    def test_get_collector(self):
        """Test case to get or show Collector."""
        self.url = self.url_prefix + self.uuid + '/'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(unicode_to_ascii_dict(response.data),
                         unicode_to_ascii_dict(self.data))

    def test_delete_collector(self):
        """Test case to delete Collector."""
        self.url = self.url_prefix + self.uuid + '/'
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_collector(self):
        """Test case to update Collector."""
        self.url = self.url_prefix + self.uuid + '/'
        self._update_values = {
            'id': self.uuid,
            'name': 'new_collector1',
            'ip_address': '10.42.0.12',
            'udp_port': 2055,
            'col_type': 'netflow',
            'encapsulation_protocol': '',
        }

        response = self.client.put(self.url, self._update_values,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.data.update(self._update_values)
# Update the self.collector with the new attribute value
        for key, value in self._update_values.items():
            setattr(self.collector, key, value)

        self.assertEqual(unicode_to_ascii_dict(response.data),
                         unicode_to_ascii_dict(self.data))

    def test_put_collector_with_invalid_values(self):
        """Test case to update a Collector with invalid value of attributes"""
        self.url = self.url_prefix + self.uuid + '/'
        self._invalid_values = {
            'id': generate_uuid(),  # 'id' update not allowed
            'name': 'new_collector1',
            'ip_address': '10.42.0.12',
            'udp_port': 70000,
            'col_type': 'netflow',
            'encapsulation_protocol': '',
            }

        response = self.client.put(self.url, self._invalid_values,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        LOG.debug(unicode_to_ascii_dict(response.data))


class TestCollectorNotFound(APITestCase):
    """Test case for GET, PUT & DELETE operations on
       Collector with no record
    """

    def setUp(self):
        self._uuid = generate_uuid()
        self._url = reverse('collector_list', kwargs={'version': 'v1.0',
                                                      'namespace': 'secmon'})

        self.uuid1 = generate_uuid()
        self._url_prefix = '/v1.0/secmon/collector/'

    def tearDown(self):
        pass

    def test_list_collector_with_no_records(self):
        """Test case to list all Collector with no records present."""
        response = self.client.get(self._url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_collector_with_invalid_id(self):
        """Test case to show or get Collector with invalid id."""
        self._url = self._url_prefix + self._uuid + '/'
        response = self.client.get(self._url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_collector_with_invalid_id(self):
        """Test case to update Collector with invalid id."""
        self._url = self._url_prefix + self._uuid + '/'
        self._update_value = {'id': self.uuid1}
        response = self.client.put(self._url, self._update_value,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_collector_with_None_value(self):
        """Test case to update Collector with None value."""
        self._url = self._url_prefix + self._uuid + '/'
        response = self.client.put(self._url, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_collector_with_invalid_id(self):
        """Test case to delete Collector with invalid id."""
        self._url = self._url_prefix + self._uuid + '/'
        response = self.client.delete(self._url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_collector_with_None_value(self):
        """Test case to create Collector with None value"""
        response = self.client.post(self._url, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
