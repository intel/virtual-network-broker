from unittest import TestCase
import argparse
#import pdb
#sys.path.append(os.path.abspath('..'))
from secmonclient.v1_0.vpn import sflowassociation

class TestSflowassociation(TestCase):
    def setUp(self):
#        pdb.set_trace()
        self.commands = {
            'sflowassociation-create':
                sflowassociation.CreateSFlowAssociation,
            'sflowassociation-list':
                sflowassociation.ListSFlowAssociation,
            'sflowassociation-show':
                sflowassociation.ShowSFlowAssociation,
            'sflowassociation-update':
                sflowassociation.UpdateSFlowAssociation,
            'sflowassociation-delete':
                sflowassociation.DeleteSFlowAssociation
                   }

        self.invalid_data = {'verbose_level': 1,
                     'namespace': 'secmon',
                     'originator_vm_id': '9662b088-74b4-40df-9769-c8f435d7f16f', 
                     'ipsec_ems_fqdn': '10.42.0.113',
                     'direction': 'front',                   # invalid direction
                     'collector_id': 'Collector:33264640-302f-456c-ac0e-f06cc13a6a47',
                     'policy_id': '72231461-aae9-4059-a5f1-7934ba969d3c', 
                     'scope_id': '04df6a37-cf8e-4511-9387-f78325336776'}

        self.valid_data = {'verbose_level': 1,
                     'namespace': 'secmon',
                     'originator_vm_id': '9662b088-74b4-40df-9769-c8f435d7f16f',
                     'ipsec_ems_fqdn': '10.42.0.113',
                     'direction': 'BOTH',                   # valid direction
                     'collector_id': 'Collector:33264640-302f-456c-ac0e-f06cc13a6a47',
                     'policy_id': '72231461-aae9-4059-a5f1-7934ba969d3c',
                     'scope_id': '04df6a37-cf8e-4511-9387-f78325336776'}

    
    def tearDown(self):
        pass

    def test_sflowassociation_create_verify_arguments_with_invalid_data(self):
        """test case to test verify_arguments function with invalid data
        """
        self.subcommand_class = self.commands.get('sflowassociation-create')
        with self.assertRaises(argparse.ArgumentTypeError):
            self.subcommand_class().verify_arguments(self.invalid_data)

    def test_sflowassociation_update_verify_arguments_with_invalid_data(self):
        """test case to verify verify_arguments for collector update with invalid data
        """
        self.subcommandupdate_class = self.commands.get('sflowassociation-update')
        with self.assertRaises(argparse.ArgumentTypeError):
            self.subcommandupdate_class().verify_arguments(self.invalid_data)

    def test_sflowassociation_update_verify_arguments_with_valid_data(self):
        """test case to test verify_arguments function with valid data
        """
        self.subcommand_class = self.commands.get('sflowassociation-create')
        result=self.subcommand_class().verify_arguments(self.valid_data)
        self.assertEqual(None, result)

    def test_sflowassociation_update_verify_arguments_with_valid_data(self):
        """test case to verify verify_arguments for collector update with valid data
        """
        self.subcommandupdate_class = self.commands.get('sflowassociation-update')
        result= self.subcommandupdate_class().verify_arguments(self.valid_data)
        self.assertEqual(None, result)

    def test_add_Argument_with_valid_parser(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('sflowassociation-create')
        parser = argparse.ArgumentParser(description='parser for sflowassociation arguments')
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
        self.subcommand_class = self.commands.get('sflowassociation-show')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_argument_list(self):
        """test case to test add_argument in list with valid data
        """
        self.subcommand_class = self.commands.get('sflowassociation-list')
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
        self.subcommand_class = self.commands.get('sflowassociation-delete')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_Argument_with_valid_parser_update(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('sflowassociation-update')
        parser = argparse.ArgumentParser(description='parser for sflowassociation arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.direction,None)
        self.assertEqual(arg1.id,None)
        self.assertEqual(arg1.collector_id,None)
        self.assertEqual(arg1.originator_vm_id,None)
        self.assertEqual(arg1.policy_id,None)
        self.assertEqual(arg1.scope_id,None)
