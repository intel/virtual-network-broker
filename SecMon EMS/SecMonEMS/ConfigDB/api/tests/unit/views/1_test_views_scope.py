import logging

from rest_framework import status
from rest_framework.test import APITestCase

from ConfigDB.api.serializers.serializers_scope import Scope
from ConfigDB.api.utils import generate_uuid

LOG = logging.getLogger(__name__)


class TestScope(APITestCase):
    """Test case for testing sk operations on Scope"""

    def setUp(self):
        # Scope test record
        self.data = {
                     'name': 'scope1',
                     'sflowstatus': 'enable',
                     'netflowstatus': 'disable',
                     'rawforwardstatus': 'disable',
                     }

        self.url_prefix = '/v1.0/secmon/scope/name/'
        # Store the test record in storage
        if not self._testMethodName.startswith('test_post_'):
            self.uuid = generate_uuid()  # Generate an id except for POST
            self.data.update({'id': self.uuid})
            self.scope = Scope(**self.data)
            self.scope.save()

    def tearDown(self):
        # Delete the test record in storage and revert storage to original
        # state.
        self.scope.delete()

    def test_scope_get_with_valid_sk(self):
        """test case to test scope for valid sk operation"""
        self.url = self.url_prefix + 'scope1/'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], self.data)

    def test_scope_get_with_invalid_sk(self):
        """test case to get none data for invalid get"""
        self.uuid1 = generate_uuid()
        self.url = self.url_prefix + 'scope2/'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
