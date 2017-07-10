from unittest import TestCase
import argparse
import pdb
#sys.path.append(os.path.abspath('..'))
from secmonclient.v1_0.vpn import utils_vpn as uv


class TestIntegerRange(TestCase):
    def setUp(self):
        self.valdata = 1234
        self.invadata = 70023
        self.nonedata= None

        self.data = {
                     'collector_ids': "[{'id':'762418c9-d2dc-4787-9593-d6ffcea4b66e','weight':20},{'id':'c6001fd6-0ee2-46c8-a1b9-73bf91de63d1','weight':30}]",
                     'verbose_level': 1,
                     'name': 'rawcollectorset12345',
                     'namespace': 'secmon',
                     'ipsec_ems_fqdn': '10.42.0.113',
                     'col_type': 'rawforward',
                     'lb_algo': 'round_robin'
                     }
        self.result = {
                       'collector_ids': "[{'id':'762418c9-d2dc-4787-9593-d6ffcea4b66e','weight':20},{'id':'c6001fd6-0ee2-46c8-a1b9-73bf91de63d1','weight':30}]",
                       'verbose_level': 1,
                       'name': 'rawcollectorset12345',
                       'namespace': 'secmon',
                       'ipsec_ems_fqdn': '10.42.0.113',
                       'col_type': 'rawforward',
                       'lb_algo': '1',
                       }

    def tearDown(self):
        pass

    def test_integer_range_with_valid_data(self):
        """test case to test check_integer_range with valid data
        """
        self.assertTrue(uv.check_integer_range(self.valdata))

    def test_integer_range_with_invalid_data(self):
        """test case to test check_integer_range with valid data
        """
#       pdb.set_trace()
 #      with self.assertRaises(argparse.ArgumentTypeError):
#           uv.check_integer_range(self.invadata)
        self.assertFalse(uv.check_integer_range(self.invadata))

    def test_integer_range_with_none_data(self):
        """test case to test check_integer_range function with none data
        """
        self.assertFalse(uv.check_integer_range(None))

    def test_string_to_integer_field_mapping_valid_data(self):
        """test case to test string_to_integer_field_mapping with valid dara
        """
        # pdb.set_trace()
        self.assertEqual(uv.string_to_integer_field_mapping(self.data), self.result)

    def test_integer_to_string_mapping_show_valid_data(self):
        """test case to test integer_to_string_mapping_show with valid dara
        """
        # pdb.set_trace()
        self.assertEqual(uv.integer_to_string_mapping_show(self.result), self.data)

