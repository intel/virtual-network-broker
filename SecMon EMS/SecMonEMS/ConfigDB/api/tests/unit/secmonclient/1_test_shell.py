from unittest import TestCase
import argparse
import pdb
#sys.path.append(os.path.abspath('..'))
from secmonclient import shell as sh


class TestShell(TestCase):
    def setUp(self):
        self.IPSEC_EMS_API_VERSION = '1.0'

        self.argv = ['collectorset-create', 'rawcollectorset1', '--collector-ids', "[{'id':'762418c9-d2dc-4787-9593-d6ffcea4b66e','weight':20},{'id':'c6001fd6-0ee2-46c8-a1b9-73bf91de63d1','weight':30}]", '--col-type', 'rawforward', '--lb-algo', 'round_robin']

    def tearDown(self):
        pass

    def test_run_with_valid_data(self):
        """test case to test run function with valid data
        """
        result = sh.Shell(self.IPSEC_EMS_API_VERSION).run(self.argv)
        print("result in test_run_with_valid_data:", result)
