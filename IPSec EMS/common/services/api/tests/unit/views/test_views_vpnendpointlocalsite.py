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

from services.api.serializers.serializers_vpnendpointlocalsite import (
    VPNEndpointLocalSite
)
from services.api.serializers.utils_serializers import generate_uuid
from services.api.serializers.utils_serializers import is_valid_uuid
from services.api.serializers.utils_serializers import unicode_to_ascii_dict
from services.api.tests.unit.views.common import COMMON_URL_PREFIX
from services.api.tests.unit.views.utils import Certificates

LOG = logging.getLogger(__name__)

# VPNEndpointLocalSite test record
VPNENDPOINTLOCALSITE_RECORD = {
    # 'id':
    'name': 'localsite1',
    'description': 'mylocalsite1',
    'cidrs': ['10.1.65.0/24'],
    # 'vpncertificate_id':
}


class TestVPNEndpointLocalSiteCRUD(APITestCase):
    """Test case for CRUD operations on VPNEndpointLocalSite"""

    def setUp(self):

        self.data = deepcopy(VPNENDPOINTLOCALSITE_RECORD)

        # Add vpncertificate id to test record
        self.certificates = Certificates()
        self.certificates.prepare_vpncertificate()
        self.data.update({'vpncertificate_id': self.certificates.cert_id})

        self.url_prefix = COMMON_URL_PREFIX + "vpnendpointlocalsites/"
        # Store the test record in storage
        if not self._testMethodName.startswith('test_post'):
            self.uuid = generate_uuid()  # Generate an id except for POST
            self.data.update({'id': self.uuid})
            self.vpnendpointlocalsite = VPNEndpointLocalSite(**self.data).save()

        # For POST & List,
        # Use the url with name 'vpnendpointlocalsites_list' in urls.py file
        if self._testMethodName.startswith('test_post') or \
                self._testMethodName.startswith('test_list'):
            self.url = reverse('vpnendpointlocalsites_list', kwargs={
                'version': 'v1',
                'namespace': 'main'
                })

    def tearDown(self):
        self.certificates.delete_vpncertificate()

        # Delete the test record in storage and revert storage to original
        # state.
        if self._testMethodName.startswith('test_post'):
            # Use 'id' of POST response
            VPNEndpointLocalSite.get(id=self.uuid).delete()
        else:
            self.vpnendpointlocalsite.delete()

    def test_post(self):
        """Test case to create an VPNEndpointLocalSite"""
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
        """Test case to list all VPNEndpointLocalSites"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(unicode_to_ascii_dict(self.data) in
                        unicode_to_ascii_dict(response.data))

    def test_get(self):
        """Test case to get or show an VPNEndpointLocalSite"""
        self.url = self.url_prefix + self.uuid + '/'
        print(self.url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(unicode_to_ascii_dict(response.data),
                         unicode_to_ascii_dict(self.data))

    def test_delete(self):
        """Test case to delete an VPNEndpointLocalSite"""
        self.url = self.url_prefix + self.uuid + '/'
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put(self):
        """Test case to update an VPNEndpointLocalSite"""
        self.url = self.url_prefix + self.uuid + '/'
        self._update_values = [
            {'name': 'new_localsite1'},
            {'description': 'new_mylocasite1'},
        ]

        for update_value in self._update_values:
            response = self.client.put(self.url, update_value, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.data.update(update_value)

            # Update the self.ikepolicy with the new attribute value
            for key, value in update_value.items():
                setattr(self.vpnendpointlocalsite, key, value)

            self.assertEqual(unicode_to_ascii_dict(response.data),
                             unicode_to_ascii_dict(self.data))


class TestVPNEndpointLocalSiteNotFound(APITestCase):
    """Test case for GET, PUT & DELETE operations on
     VPNEndpointLocalSite with no record"""

    def setUp(self):
        self._uuid = generate_uuid()
        self._url = reverse('vpnendpointlocalsites_list', kwargs={
            'version': 'v1',
            'namespace': 'main'
            })
        self._url_prefix = COMMON_URL_PREFIX + "vpnendpointlocalsites/"

    def test_list_with_no_records(self):
        """Test case to list all VPNEndpointLocalSite with no records
         present."""
        response = self.client.get(self._url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_with_invalid_id(self):
        """Test case to show or get an VPNEndpointLocalSite with invalid id"""
        self._url = self._url_prefix + self._uuid + '/'
        response = self.client.get(self._url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_with_invalid_id(self):
        """Test case to update an VPNEndpointLocalSite with invalid id"""
        self._url = self._url_prefix + self._uuid + '/'
        self._update_value = {'description': 'mylocalsite2'}
        response = self.client.put(self._url, self._update_value,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_invalid_id(self):
        """Test case to delete an VPNEndpointLocalSite with invalid id"""
        self._url = self._url_prefix + self._uuid + '/'
        response = self.client.delete(self._url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestVPNEndpointLocalSiteBadRequest(APITestCase):
    """Test case for POST & PUT operations on VPNEndpointLocalSite with invalid
     record"""

    def setUp(self):
        self._data = deepcopy(VPNENDPOINTLOCALSITE_RECORD)
        self._uuid = generate_uuid()
        self._url = reverse('vpnendpointlocalsites_list', kwargs={
            'version': 'v1',
            'namespace': 'main'
            })
        self._url_prefix = COMMON_URL_PREFIX + "vpnendpointlocalsites/"
        if not self._testMethodName.startswith('test_post_'):
            self.uuid = generate_uuid()  # Generate an id except for POST
            self._data.update({'id': self.uuid})
            self.vpnendpointlocalsite = (
                VPNEndpointLocalSite(**self._data).save())

    def tearDown(self):
        # Delete the test record in storage and revert storage to original
        # state.
        if not self._testMethodName.startswith('test_post_'):
            self.vpnendpointlocalsite.delete()

    def test_post_with_invalid_values(self):
        """Test case to create an VPNEndpointLocalSite with invalid values"""
        self._invalid_values = [
            {'name': ''},
            {'description': 1},
            {'peer_address': '10.1.63.259'},
            {'peer_cidrs': ['10.1.65.4/24']},
            {'vpncertificate_id': generate_uuid()}
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
        """Test case to update an VPNEndpointLocalSite with invalid value of
         attributes"""
        self.url = self._url_prefix + self.uuid + '/'
        self._invalid_values = [
            {'id': generate_uuid()},  # 'id' update not allowed
            {'name': ''},
            {'cidrs': ''},
            {'cidrs': '10.1.23.45/24'},
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
