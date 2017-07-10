from unittest import TestCase
import argparse
#import pdb
#sys.path.append(os.path.abspath('..'))
from secmonclient.v1_0.vpn import netflowassociation

class TestNetflowassociation(TestCase):
    def setUp(self):
#        pdb.set_trace()
        self.commands = {
            'netflowassociation-create':
                netflowassociation.CreateNetFlowAssociation,
            'netflowassociation-list':
                netflowassociation.ListNetFlowAssociation,
            'netflowassociation-show':
                netflowassociation.ShowNetFlowAssociation,
            'netflowassociation-update':
                netflowassociation.UpdateNetFlowAssociation,
            'netflowassociation-delete':
                netflowassociation.DeleteNetFlowAssociation
                   }

        self.invalid_data = {'verbose_level': 1,
                     'namespace': 'secmon',
                     'originator_vm_id': '9662b088-74b4-40df-9769-c8f435d7f16f', 
                     'ipsec_ems_fqdn': '10.42.0.113',
                     'direction': 'front',                   # invalid direction
                     'collector_id': 'Collector:33264640-302f-456c-ac0e-f06cc13a6a47',
                     'policy_id': '5eaa8aa0-fad2-4dc0-bfcf-df7985d97ebf', 
                     'scope_id': '04df6a37-cf8e-4511-9387-f78325336776'}

        self.valid_data = {'verbose_level': 1,
                     'namespace': 'secmon',
                     'originator_vm_id': '9662b088-74b4-40df-9769-c8f435d7f16f',
                     'ipsec_ems_fqdn': '10.42.0.113',
                     'direction': 'BOTH',                   # valid direction
                     'collector_id': 'Collector:33264640-302f-456c-ac0e-f06cc13a6a47',
                     'policy_id': '5eaa8aa0-fad2-4dc0-bfcf-df7985d97ebf',
                     'scope_id': '04df6a37-cf8e-4511-9387-f78325336776'}          

    
    def tearDown(self):
        pass

    def test_netflowassociation_create_verify_arguments_with_invalid_data(self):
        """test case to test verify_arguments function with invalid data
        """
        self.subcommand_class = self.commands.get('netflowassociation-create')
        with self.assertRaises(argparse.ArgumentTypeError):
            self.subcommand_class().verify_arguments(self.invalid_data)

    def test_netflowassociation_update_verify_arguments_with_invalid_data(self):
        """test case to verify verify_arguments for collector update with invalid data
        """
        self.subcommandupdate_class = self.commands.get('netflowassociation-update')
        with self.assertRaises(argparse.ArgumentTypeError):
            self.subcommandupdate_class().verify_arguments(self.invalid_data)

    def test_netflowassociation_create_verify_arguments_with_valid_data(self):
        """test case to test verify_arguments function with valid data
        """
        self.subcommand_class = self.commands.get('netflowassociation-create')
        result=self.subcommand_class().verify_arguments(self.valid_data)
        self.assertEqual(None, result)

    def test_netflowassociation_update_verify_arguments_with_valid_data(self):
        """test case to verify verify_arguments for collector update with valid data
        """
        self.subcommandupdate_class = self.commands.get('netflowassociation-update')
        result= self.subcommandupdate_class().verify_arguments(self.valid_data)
        self.assertEqual(None, result)


    def test_add_Argument_with_valid_parser(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('netflowassociation-create')
        parser = argparse.ArgumentParser(description='parser for netflowassociation arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.direction,None)
        self.assertEqual(arg1.collector_id,None)
        self.assertEqual(arg1.originator_vm_id,None)
        self.assertEqual(arg1.policy_id,None)
        self.assertEqual(arg1.scope_id,None)

    def test_add_argument_show(self):
        """test case to test add_argument in show with valid data
        """
        self.subcommand_class = self.commands.get('netflowassociation-show')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_argument_list(self):
        """test case to test add_argument in list with valid data
        """
        self.subcommand_class = self.commands.get('netflowassociation-list')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.show_details,None)
        self.assertEqual(arg1.fields,None)
        self.assertEqual(arg1.sort_key,None)
        self.assertEqual(arg1.sort_direction,None)
#       self.assertEqual(arg1.format,None)

    def test_add_argument_delete(self):
        """test case to test add_argument in delete with valid data
        """
        self.subcommand_class = self.commands.get('netflowassociation-delete')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_Argument_with_valid_parser_update(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('netflowassociation-update')
        parser = argparse.ArgumentParser(description='parser for netflowassociation arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id,None)
        self.assertEqual(arg1.direction,None)
        self.assertEqual(arg1.collector_id,None)
        self.assertEqual(arg1.originator_vm_id,None)
        self.assertEqual(arg1.policy_id,None)
        self.assertEqual(arg1.scope_id,None)

