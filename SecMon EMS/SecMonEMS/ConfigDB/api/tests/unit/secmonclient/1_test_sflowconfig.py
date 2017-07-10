from unittest import TestCase
import argparse
import pdb
#sys.path.append(os.path.abspath('..'))
from secmonclient.v1_0.vpn import sflowconfig

class TestSflowconfig(TestCase):
    def setUp(self):
#        pdb.set_trace()
        self.commands = {
          'sflowconfig-create':
                sflowconfig.CreateSflowConfig,
          'sflowconfig-list':
                sflowconfig.ListSflowConfig,
          'sflowconfig-show':
                sflowconfig.ShowSflowConfig,
          'sflowconfig-update':
                sflowconfig.UpdateSflowConfig,
          'sflowconfig-delete':
                sflowconfig.DeleteSflowConfig
                 }

    def tearDown(self):
        pass

    def test_add_Argument_with_valid_parser(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('sflowconfig-create')
        parser = argparse.ArgumentParser(description='parser for sflowconfig arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.scope_id,None) 
        self.assertEqual(arg1.agent_ip,None)
        self.assertEqual(arg1.truncate_to_size,None)
        self.assertEqual(arg1.agent_subid,None)
        self.assertEqual(arg1.sampling_rate,None)

#    def test_add_Argument_with_invalid_parser(self):
#        """test case to test add_argument with invalid data
#        """
#        self.subcommand_class = self.commands.get('collector-create') 
#        parser = argparse.ArgumentParser(description='parser for collector arguments')
#        with self.assertRaises(argparse.ArgumentTypeError):
#            parser = self.subcommand_class().add_known_arguments(None)

    def test_add_argument_show(self):
        """test case to test add_argument in show with valid data
        """
        self.subcommand_class = self.commands.get('sflowconfig-show')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_argument_list(self):
        """test case to test add_argument in list with valid data
        """
        self.subcommand_class = self.commands.get('sflowconfig-list')
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
        self.subcommand_class = self.commands.get('sflowconfig-delete')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_Argument_with_valid_parser_update(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('sflowconfig-update')
        parser = argparse.ArgumentParser(description='parser for sflowconfig arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id,None)
        self.assertEqual(arg1.scope_id,None)
        self.assertEqual(arg1.agent_ip,None)
        self.assertEqual(arg1.truncate_to_size,None)
        self.assertEqual(arg1.agent_subid,None)
        self.assertEqual(arg1.sampling_rate,None)

