from unittest import TestCase

from services.api.exceptions import ResourceNotFound
from services.api.serializers.serializers_ikepolicy import IKEPolicy
from services.api.serializers.utils_serializers import generate_uuid


class TestIKEPolicyNoRecord(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_save_None_record(self):
        """Test case to save None record."""
        with self.assertRaises(TypeError):
            IKEPolicy().save()

    def test_get_no_record(self):
        """Test case to fetch an IKEpolicy with invalid id."""
        with self.assertRaises(ResourceNotFound):
            IKEPolicy.get(id=generate_uuid())

    def test_get_all_no_record(self):
        """Test case to fetch all IKEpolicies with no records present."""
        with self.assertRaises(ResourceNotFound):
            IKEPolicy.all()

    def test_delete_no_record(self):
        """Test case to delete an invalid IKEPolicy record."""
        with self.assertRaises(ResourceNotFound):
            IKEPolicy().delete()

# class TestIKEPolicySerializer(TestCase):
#
#     def setUp(self):
#         self.data = {'name': 'ikepolicy1',
#                      'description': 'myikepolicy1',
#                      'pfs': 'group2',
#                      'encryption_algorithm': 'aes-128',
#                      'auth_algorithm': 'sha1',
#                      'phase1_negotiation_mode': 'main',
#                      'lifetime_value': 3600,
#                      'lifetime_units': 'seconds',
#                      'ike_version': 'v1'
#                      }
#
#         self.uuid = generate_uuid()  # Generate an id except for POST
#         self.data.update({'id': self.uuid})
#         self.ikepolicy = IKEPolicy(**self.data).save()
#
#     def tearDown(self):
#         IKEPolicy.get(self.uuid).delete()  # Use 'id' of POST response
#
#     # def test_update_id(self):
#     #     obj = IKEPolicy.get(self.uuid)
#     #     self.uuid = generate_uuid()
#     #     self.update_id({'id': self.uuid})
#     #     serializer = IKEPolicySerializer(self.data({'id': self.uuid}), obj)
#     #     print (serializer.data)
