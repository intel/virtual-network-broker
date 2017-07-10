from unittest import TestCase
import argparse
#import pdb
#sys.path.append(os.path.abspath('..'))
from secmonclient.v1_0.vpn import secmondetails

class TestSecmondetails(TestCase):
    def setUp(self):
#        pdb.set_trace()
        self.commands = {
          'secmondetails-create':
            secmondetails.CreateSecmonDetails,
          'secmondetails-list':
            secmondetails.ListSecmonDetails,
          'secmondetails-show':
            secmondetails.ShowSecmonDetails,
          'secmondetails-update':
            secmondetails.UpdateSecmonDetails,
          'secmondetails-delete':
            secmondetails.DeleteSecmonDetails,
           }

    def tearDown(self):
        pass

    def test_add_Argument_with_valid_parser(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('secmondetails-create')
        parser = argparse.ArgumentParser(description='parser for secmondetails arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.scope_name,'test')
        self.assertEqual(arg1.mac_address,None)
        self.assertEqual(arg1.ip_address,None)
        self.assertEqual(arg1.port,None)

    def test_add_argument_show(self):
        """test case to test add_argument in show with valid data
        """
        self.subcommand_class = self.commands.get('secmondetails-show')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_argument_list(self):
        """test case to test add_argument in list with valid data
        """
        self.subcommand_class = self.commands.get('secmondetails-list')
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
        self.subcommand_class = self.commands.get('secmondetails-delete')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_Argument_with_valid_parser_update(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('secmondetails-update')
        parser = argparse.ArgumentParser(description='parser for secmondetails arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.scope_name,'test')
        self.assertEqual(arg1.id,None)
        self.assertEqual(arg1.mac_address,None)
        self.assertEqual(arg1.ip_address,None)
        self.assertEqual(arg1.port,None)
