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


from services.api.serializers.serializers_vpnbind_group_to_group import (
    VPNBindGroupToGroup
)
from services.api.serializers.utils_serializers import generate_uuid
from services.api.serializers.utils_serializers import is_valid_uuid
from services.api.serializers.utils_serializers import unicode_to_ascii_dict
from services.api.tests.unit.views.common import COMMON_URL_PREFIX
from services.api.tests.unit.views.utils import (
    TempIKEPolicy, TempIPsecPolicy, TempVPNEndpointGroup
)

LOG = logging.getLogger(__name__)

# VPNBindGroupToGroup test record
VPNBINDGROUPGROUP_RECORD = {
    # 'id':
    'name': 'group1-group2',
    'description': 'group1-group2-vpnbind',
    # 'vpnendpointgroup_id':
    # 'peer_vpnendpointgroup_id':
    'admin_state_up': True,
    'dpd_action': 'restart',
    'dpd_interval': 2,
    'dpd_timeout': 30,
    'auth_mode': 'psk',
    'psk': 'P@ssw0rd',
    'initiator': 'response-only',
    # 'ikepolicy_id':
    # 'ipsecpolicy_id':
}


class TestVPNBindGroupGroupCRUD(APITestCase):
    """Test case for CRUD operations on VPNBindGroupToGroup"""

    def setUp(self):

        self.data = deepcopy(VPNBINDGROUPGROUP_RECORD)

        self._prepare_post_data()

        self.url_prefix = COMMON_URL_PREFIX + "vpnbindgrouptogroup/"
        # Store the test record in storage
        if not self._testMethodName.startswith('test_post'):
            self.uuid = generate_uuid()  # Generate an id except for POST
            self.data.update({'id': self.uuid})
            self.vpnbindgroupgroup = VPNBindGroupToGroup(**self.data).save()

        # For POST & List,
        # Use the url with name 'vpnbindgroupgroup_list' in urls.py file
        if self._testMethodName.startswith('test_post') or \
                self._testMethodName.startswith('test_list'):
            self.url = reverse('vpnbindgrouptogroup_list', kwargs={
                'version': 'v1',
                'namespace': 'main'
                })

    def tearDown(self):
        # Delete the test record in storage and revert storage to original
        # state.
        if self._testMethodName.startswith('test_post'):
            # Use 'id' of POST response
            VPNBindGroupToGroup.get(id=self.uuid).delete()
        else:
            self.vpnbindgroupgroup.delete()

        self._delete_post_record()

    def _prepare_post_data(self):

        # Add IKEPolicy id to test record
        self.ikepolicy = TempIKEPolicy()
        self.ikepolicy.create()
        self.data.update({'ikepolicy_id': self.ikepolicy.id})
        print(self.id)

        # Add IPsecPolicy id to test record
        self.ipsecpolicy = TempIPsecPolicy()
        self.ipsecpolicy.create()
        self.data.update({'ipsecpolicy_id': self.ipsecpolicy.id})

        # Add VPNEndpointGroup id to test record
        self.vpnendpointgroup = TempVPNEndpointGroup()
        self.vpnendpointgroup.create()
        self.data.update({'vpnendpointgroup_id': self.vpnendpointgroup.id})

        # Add Peer VPNEndpointGroup id to test record
        self.peer_vpnendpointgroup = TempVPNEndpointGroup()
        self.peer_vpnendpointgroup.create()
        self.data.update({
                'peer_vpnendpointgroup_id':
                self.peer_vpnendpointgroup.id})

    def _delete_post_record(self):
        self.ikepolicy.delete()
        self.ipsecpolicy.delete()
        self.vpnendpointgroup.delete()
        self.peer_vpnendpointgroup.delete()

    def test_post(self):
        """Test case to create an VPNBindGroupToGroup"""
        # No 'id' provided
        response = self.client.post(self.url, self.data, format='json')
        print(self.data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.uuid = response.data.pop('id')
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
        """Test case to list all VPNBindGroupToGroup(s)"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(unicode_to_ascii_dict(self.data) in
                        unicode_to_ascii_dict(response.data))

    def test_get(self):
        """Test case to get or show an VPNBindGroupToGroup"""
        self.url = self.url_prefix + self.uuid + '/'
        print(self.url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(unicode_to_ascii_dict(response.data),
                         unicode_to_ascii_dict(self.data))

    def test_delete(self):
        """Test case to delete an VPNBindGroupToGroup"""
        self.url = self.url_prefix + self.uuid + '/'
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put(self):
        """Test case to update an VPNBindGroupToGroup"""
        self.url = self.url_prefix + self.uuid + '/'
        self._update_values = [
            {'name': 'new_group1-group2'},
            {'description': 'new_group1-group2-vpnbind'},
            {'dpd_action': 'restart'},
            {'dpd_interval': 4},
            {'integrity_algorithm': ['sha1']},
            {'dh_group': ['modp2048']},
            {'phase1_negotiation_mode': 'main'},
            {'lifetime_value': 8100},
            {'lifetime_units': 'hours'},
            {'rekey': 'no'},
            {'reauth': 'yes'},
        ]

        for update_value in self._update_values:
            response = self.client.put(self.url, update_value, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.data.update(update_value)

            # Update the self.ikepolicy with the new attribute value
            for key, value in update_value.items():
                setattr(self.vpnbindgroupgroup, key, value)

            self.assertEqual(unicode_to_ascii_dict(response.data),
                             unicode_to_ascii_dict(self.data))


class TestVPNBindGroupGroupNotFound(APITestCase):
    """Test case for GET, PUT & DELETE operations on VPNBindGroupToGroup
     with no record"""

    def setUp(self):
        self._uuid = generate_uuid()
        self._url = reverse('vpnbindgrouptogroup_list', kwargs={
            'version': 'v1',
            'namespace': 'main'
            })
        self._url_prefix = COMMON_URL_PREFIX + 'vpnbindgrouptogroup/'

    def test_list_with_no_records(self):
        """Test case to list all VPNBindGroupToGroup(s) with no records
         present"""
        response = self.client.get(self._url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_with_invalid_id(self):
        """Test case to show or get an VPNBindGroupToGroup with invalid
         id"""
        self._url = self._url_prefix + self._uuid + '/'
        response = self.client.get(self._url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_with_invalid_id(self):
        """Test case to update an VPNBindGroupToGroup with invalid id"""
        self._url = self._url_prefix + self._uuid + '/'
        self._update_value = {'description': 'group1-group2 vpnbind2'}
        response = self.client.put(self._url, self._update_value,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_invalid_id(self):
        """Test case to delete an VPNBindGroupToGroup with invalid id"""
        self._url = self._url_prefix + self._uuid + '/'
        response = self.client.delete(self._url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class TestIKEPolicyBadRequest(APITestCase):
#     """Test case for POST & PUT operations on IKEPolicy with invalid record"""
#
#     def setUp(self):
#         self._data = deepcopy(IKEPOLICY_RECORD)
#         self._uuid = generate_uuid()
#         self._url = reverse('ikepolicies_list', kwargs={
#             'version': 'v1',
#             'namespace': 'main'
#             })
#         self._base_url = COMMON_URL_PREFIX + 'ikepolicies/'
#         if not self._testMethodName.startswith('test_post_'):
#             self.uuid = generate_uuid()  # Generate an id except for POST
#             self._data.update({'id': self.uuid})
#             self.ikepolicy = IKEPolicy(**self._data).save()
#
#     def tearDown(self):
#         # Delete the test record in storage and revert storage to original
#         # state.
#         if not self._testMethodName.startswith('test_post_'):
#             self.ikepolicy.delete()
#
#     def test_post_with_invalid_values(self):
#         """Test case to create an IKEpolicy with invalid values"""
#         self._invalid_values = [
#             {'integrity_algorithm': 'md5'},
#             {'encryption_algorithm': 'des'},
#             {'phase1_negotiation_mode': 'aggressive'},
#             {'ike_version': 'v6'},
#             {'dh_group': 'group1'},
#             {'lifetime_units': 'Megabytes'},
#             {'lifetime_value': -20},
#         ]
#
#         for update_value in self._invalid_values:
#             self._data.update(update_value)
#             response = self.client.post(self._url, update_value, format='json')
#             self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_post_with_multiple_encryption_algos_for_version_1(self):
#         """Test case to create an IKEpolicy"""
#         self._data.update({'encryption_algorithm': ['aes128', 'aes256']})
#         response = self.client.post(self._url, self._data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_post_with_multiple_integrity_algos_for_version_1(self):
#         self._data.update({'integrity_algorithm': ['aes128', 'aes256']})
#         response = self.client.post(self._url, self._data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_post_with_multiple_dh_groups_for_version_1(self):
#         self._data.update({'dh_group': ['modp8192', 'modp1024s160']})
#         response = self.client.post(self._url, self._data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_put_with_invalid_values(self):
#         """Test case to update an IKEpolicy with invalid value of attributes"""
#         self.url = self._base_url + self.uuid + '/'
#         self._invalid_values = [
#             {'id': generate_uuid()},  # 'id' update not allowed
#             {'integrity_algorithm': 'md5'},
#             {'integrity_algorithm': '200'},
#             {'encryption_algorithm': 'des'},
#             {'encryption_algorithm': '100'},
#             {'phase1_negotiation_mode': '100'},
#             {'ike_version': 'v6'},
#             {'ike_version': '500'},
#             {'dh_group': 'modp2000'},
#             {'dh_group': '120'},
#             {'lifetime_units': 'Megabytes'},
#             {'lifetime_units': '20000'},
#             {'lifetime_value': -20},
#             {'lifetime_value': 'Megabytes'}
#         ]
#
#         for update_value in self._invalid_values:
#             response = self.client.put(self.url, update_value, format='json')
#             self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#             LOG.debug(unicode_to_ascii_dict(response.data))
#             # TODO: If required, also check for http response message:
#             # self.assertEqual(response.data,
#             #                  {'pfs': ['"group1" is not a valid choice.']})
#             # e.g. Some other responses would be like below:
#             # {'auth_algorithm': ['"md5" is not a valid ''choice.']}
#             # {'lifetime_value': ['A valid integer is required.']}
