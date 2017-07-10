from unittest import TestCase
import argparse
import pdb
#sys.path.append(os.path.abspath('..'))
from secmonclient.v1_0.vpn import netflowconfig

class TestNetflowconfig(TestCase):
    def setUp(self):
#        pdb.set_trace()
        self.commands = {
            'netflowconfig-create':
                netflowconfig.CreateNetFlowConfig,
            'netflowconfig-list':
                netflowconfig.ListNetFlowConfig,
            'netflowconfig-show':
                netflowconfig.ShowNetFlowConfig,
            'netflowconfig-update':
                netflowconfig.UpdateNetFlowConfig,
            'netflowconfig-delete':
                netflowconfig.DeleteNetFlowConfig
                   }

    
    def tearDown(self):
        pass

    def test_add_Argument_with_valid_parser(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('netflowconfig-create')
        parser = argparse.ArgumentParser(description='parser for netflowconfig arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.scope_id,None)
        self.assertEqual(arg1.active_timeout,None) 
        self.assertEqual(arg1.inactive_timeout,None)
        self.assertEqual(arg1.refresh_rate,None)
        self.assertEqual(arg1.timeout_rate,None)
        self.assertEqual(arg1.maxflows,None)

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
        self.subcommand_class = self.commands.get('netflowconfig-show')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_argument_list(self):
        """test case to test add_argument in list with valid data
        """
        self.subcommand_class = self.commands.get('netflowconfig-list')
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
        self.subcommand_class = self.commands.get('netflowconfig-delete')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_Argument_with_valid_parser_update(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('netflowconfig-create')
        parser = argparse.ArgumentParser(description='parser for netflowconfig arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id,None)
        self.assertEqual(arg1.scope_id,None)
        self.assertEqual(arg1.active_timeout,None)
        self.assertEqual(arg1.inactive_timeout,None)
        self.assertEqual(arg1.refresh_rate,None)
        self.assertEqual(arg1.timeout_rate,None)
        self.assertEqual(arg1.maxflows,None)


