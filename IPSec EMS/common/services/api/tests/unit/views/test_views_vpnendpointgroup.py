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
from copy import deepcopy

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from services.api.serializers.serializers_vpnendpointgroup import (
    VPNEndpointGroup
)
from services.api.serializers.utils_serializers import generate_uuid
from services.api.serializers.utils_serializers import is_valid_uuid
from services.api.serializers.utils_serializers import unicode_to_ascii_dict
from services.api.tests.unit.views.common import COMMON_URL_PREFIX
from services.api.tests.unit.views.utils import Certificates

LOG = logging.getLogger(__name__)

# VPNEndpointGroup test record
VPNENDPOINTGROUP_RECORD = {
    # 'id':
    'name': 'group1',
    'description': 'mygroup1',
    # 'vpncertificate_id':
}


class TestVPNEndpointGroupCRUD(APITestCase):
    """Test case for CRUD operations on VPNEndpointGroup"""

    def setUp(self):
        self.data = deepcopy(VPNENDPOINTGROUP_RECORD)

        # Add vpncertificate id to test record
        self.certificates = Certificates()
        self.certificates.prepare_vpncertificate()
        self.data.update({'vpncertificate_id': self.certificates.cert_id})

        self.url_prefix = COMMON_URL_PREFIX + "vpnendpointgroups/"
        # Store the test record in storage
        if not self._testMethodName.startswith('test_post'):
            self.uuid = generate_uuid()  # Generate an id except for POST
            self.data.update({'id': self.uuid})
            self.vpnendpointgroup = VPNEndpointGroup(**self.data).save()

        # For POST & List,
        # Use the url with name 'vpnendpointgroups_list' in urls.py file
        if self._testMethodName.startswith('test_post') or \
                self._testMethodName.startswith('test_list'):
            self.url = reverse('vpnendpointgroups_list', kwargs={
                'version': 'v1',
                'namespace': 'main'
            })

    def tearDown(self):
        self.certificates.delete_vpncertificate()
        # Delete the test record in storage and revert storage to original
        # state.
        if self._testMethodName.startswith('test_post'):
            # Use 'id' of POST response
            VPNEndpointGroup.get(id=self.uuid).delete()
        else:
            self.vpnendpointgroup.delete()

    def test_post(self):
        """Test case to create an VPNEndpointGroup"""
        # No 'id' provided
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.uuid = response.data.pop('id')
        LOG.info(self.data)
        LOG.info(response.data)
        self.assertTrue(is_valid_uuid(self.uuid))

        self.assertEqual(unicode_to_ascii_dict(response.data),
                         unicode_to_ascii_dict(self.data))

    def test_post_id(self):
        # 'id' provided
        self.uuid = generate_uuid()
        self.data.update({'id': self.uuid})
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(unicode_to_ascii_dict(response.data),
                         unicode_to_ascii_dict(self.data))

    def test_list(self):
        """Test case to list all VPNEndpointGroups"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(unicode_to_ascii_dict(self.data) in
                        unicode_to_ascii_dict(response.data))

    def test_get(self):
        """Test case to get or show an VPNEndpointGroup."""
        self.url = self.url_prefix + self.uuid + '/'
        print(self.url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(unicode_to_ascii_dict(response.data),
                         unicode_to_ascii_dict(self.data))

    def test_delete(self):
        """Test case to delete an VPNEndpointGroup"""
        self.url = self.url_prefix + self.uuid + '/'
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put(self):
        """Test case to update an VPNEndpointGroup"""
        self.url = self.url_prefix + self.uuid + '/'
        self._update_values = [
            {'name': 'new_group1'},
            {'description': 'new_mygroup1'},
        ]

        for update_value in self._update_values:
            response = self.client.put(self.url, update_value, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.data.update(update_value)

            # Update the self.ikepolicy with the new attribute value
            for key, value in update_value.items():
                setattr(self.vpnendpointgroup, key, value)

            self.assertEqual(unicode_to_ascii_dict(response.data),
                             unicode_to_ascii_dict(self.data))


class TestVPNEndpointGroupNotFound(APITestCase):
    """Test case for GET, PUT & DELETE operations on VPNEndpointGroup with no
     record"""

    def setUp(self):
        self._uuid = generate_uuid()
        self._url = reverse('vpnendpointgroups_list', kwargs={
            'version': 'v1',
            'namespace': 'main'
        })
        self._url_prefix = COMMON_URL_PREFIX + "vpnendpointgroups/"

    def test_list_with_no_records(self):
        """Test case to list all VPNEndpointGroups with no records present."""
        response = self.client.get(self._url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_with_invalid_id(self):
        """Test case to show or get an VPNEndpointGroup with invalid id."""
        self._url = self._url_prefix + self._uuid + '/'
        response = self.client.get(self._url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_with_invalid_id(self):
        """Test case to update an VPNEndpointGroup with invalid id."""
        self._url = self._url_prefix + self._uuid + '/'
        self._update_value = {'description': 'mygroup2'}
        response = self.client.put(self._url, self._update_value,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_invalid_id(self):
        """Test case to delete an VPNEndpointGroup with invalid id."""
        self._url = self._url_prefix + self._uuid + '/'
        response = self.client.delete(self._url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestVPNEndpointGroupBadRequest(APITestCase):
    """Test case for POST & PUT operations on VPNEndpointGroup with invalid
     record"""

    def setUp(self):
        self._data = deepcopy(VPNENDPOINTGROUP_RECORD)
        self._uuid = generate_uuid()
        self._url = reverse('vpnendpointgroups_list', kwargs={
            'version': 'v1',
            'namespace': 'main'
        })
        self._url_prefix = COMMON_URL_PREFIX + "vpnendpointgroups/"
        if not self._testMethodName.startswith('test_post_'):
            self.uuid = generate_uuid()  # Generate an id except for POST
            self._data.update({'id': self.uuid})
            self.ikepolicy = VPNEndpointGroup(**self._data).save()

    def tearDown(self):
        # Delete the test record in storage and revert storage to original
        # state.
        if not self._testMethodName.startswith('test_post_'):
            self.ikepolicy.delete()

    def test_post_with_invalid_values(self):
        """Test case to create an VPNEndpointGroup with invalid values"""
        self._invalid_values = [
            {'name': ''},
            {'description': 1},
            {'vpncertificate_id': generate_uuid()},
        ]

        for update_value in self._invalid_values:
            self._data.update(update_value)
            response = self.client.post(self._url, update_value, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_post_with_multiple_encryption_algos_for_version_1(self):
    #     """Test case to create an VPNEndpointGroup"""
    #     self._data.update({'encryption_algorithm': ['aes128', 'aes256']})
    #     response = self.client.post(self._url, self._data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_post_with_multiple_integrity_algos_for_version_1(self):
    #     self._data.update({'integrity_algorithm': ['aes128', 'aes256']})
    #     response = self.client.post(self._url, self._data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_post_with_multiple_dh_groups_for_version_1(self):
    #     self._data.update({'dh_group': ['modp8192', 'modp1024s160']})
    #     response = self.client.post(self._url, self._data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_with_invalid_values(self):
        """Test case to update an VPNEndpointGroup with invalid value of
         attributes"""
        self.url = self._url_prefix + self.uuid + '/'
        self._invalid_values = [
            {'id': generate_uuid()},  # 'id' update not allowed
            {'name': ''},
            {'vpncertificate_id': generate_uuid()}
        ]

        for update_value in self._invalid_values:
            response = self.client.put(self.url, update_value, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            LOG.debug(unicode_to_ascii_dict(response.data))
            # TODO: If required, also check for http response message:
            # self.assertEqual(response.data,
            #                  {'pfs': ['"group1" is not a valid choice.']})
            # e.g. Some other responses would be like below:
            # {'auth_algorithm': ['"md5" is not a valid ''choice.']}
            # {'lifetime_value': ['A valid integer is required.']}
