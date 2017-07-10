from unittest import TestCase
import argparse
#import pdb
#sys.path.append(os.path.abspath('..'))
from secmonclient.v1_0.vpn import collectorset

class TestCollectorset(TestCase):
    def setUp(self):
#        pdb.set_trace()
        self.commands = {
            'collectorset-create':
                collectorset.CreateCollectorset,
            'collectorset-list':
                collectorset.ListCollectorset,
            'collectorset-show':
                collectorset.ShowCollectorset,
            'collectorset-update':
                collectorset.UpdateCollectorset,
            'collectorset-delete':
                collectorset.DeleteCollectorset
                   }
        self.valid_data = {'verbose_level': 1,
                     'name': 'collector1234',
                     'namespace': 'secmon',
                     'ipsec_ems_fqdn': '10.42.0.113',
                     'col_type': 'sflow',                   # valid coltype
                     'collector_ids': '233bfdbb-322d-4f75-957b-e77e75a03f63',
                     'lb_algo': 'session_based'}

        self.invalid_data = {'verbose_level': 1,
                     'name': 'collector1234',
                     'namespace': 'secmon',
                     'ipsec_ems_fqdn': '10.42.0.113',
                     'col_type': 'col1',                   # invalid coltype
                     'collector_ids': '233bfdbb-322d-4f75-957b-e77e75a03f63',
                     'lb_algo': 'round_robin'}
          
    
    def tearDown(self):
        pass

    def test_collectorset_create_verify_arguments_with_invalid_data(self):
        """test case to test verify_arguments for collectorset create with invalid data
        """
        self.subcommand_class = self.commands.get('collectorset-create')
        with self.assertRaises(argparse.ArgumentTypeError):
            self.subcommand_class().verify_arguments(self.invalid_data)

    def test_collectorset_update_verify_arguments_with_invalid_date(self):
        """test case to test verify_arguments for collector update with invalid data
        """
        self.subcommandupdate_class = self.commands.get('collectorset-update')
        with self.assertRaises(argparse.ArgumentTypeError):
            self.subcommandupdate_class().verify_arguments(self.invalid_data)

    def test_collectorset_create_verify_arguments_with_valid_data(self):
        """test case to test verify_arguments for collectorset create with valid data
        """
        self.subcommand_class = self.commands.get('collectorset-create')
        result= self.subcommand_class().verify_arguments(self.valid_data)
        self.assertEqual(None, result)

    def test_collectorset_update_verify_arguments_with_valid_date(self):
        """test case to test verify_arguments for collector update with valid data
        """
        self.subcommandupdate_class = self.commands.get('collectorset-update')
        result = self.subcommandupdate_class().verify_arguments(self.valid_data)
        self.assertEqual(None, result)

    def test_add_Argument_with_valid_parser_create(self):
        """test case to test add_argument with valid data
        """
        self.subcommand_class = self.commands.get('collectorset-create')
        parser = argparse.ArgumentParser(description='parser for collectorset arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.name,'test')
        self.assertEqual(arg1.col_type,None)
        self.assertEqual(arg1.collector_ids,None)
        self.assertEqual(arg1.lb_algo,None)
'''
    def test_add_argument_show(self):
        #test case to test add_argument in show with valid data
        
        self.subcommand_class = self.commands.get('collectorset-show')
        parser =  argparse.ArgumentParser(description='parser for collectorset arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_argument_list(self):
        """test case to test add_argument in list with valid data
        """
        self.subcommand_class = self.commands.get('collectorset-list')
        parser =  argparse.ArgumentParser(description='parser for collectorset arguments')
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
        self.subcommand_class = self.commands.get('collectorset-delete')
        parser =  argparse.ArgumentParser(description='parser for collectorset arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_Argument_with_valid_parser_update(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('collectorset-update')
        parser = argparse.ArgumentParser(description='parser for collectorset arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.name,'test')
        self.assertEqual(arg1.id,None)
        self.assertEqual(arg1.col_type,None)
        self.assertEqual(arg1.collector_ids,None)
        self.assertEqual(arg1.lb_algo,None)
'''
