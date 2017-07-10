from unittest import TestCase
import argparse
import pdb
#sys.path.append(os.path.abspath('..'))
from secmonclient.v1_0.vpn import collector

class TestCollector(TestCase):
    def setUp(self):
#        pdb.set_trace()
        self.commands = {
            'collector-create':
                collector.CreateCollector,
            'collector-list':
                collector.ListCollector,
            'collector-show':
                collector.ShowCollector,
            'collector-update':
                collector.UpdateCollector,
            'collector-delete':
                collector.DeleteCollector
                   }

        self.invalid_data = {'verbose_level': 1,
                     'name': 'collector1234',
                     'namespace': 'secmon',
                     'udp_port': '1234',
                     'ipsec_ems_fqdn': '10.42.0.113',
                     'col_type': 'col1',                   # invalid coltype
                     'ip_address': '10.42.0.164',
                     'encapsulation_protocol': 'udp'}
    
        self.valid_data = {'verbose_level': 1,
                     'name': 'collector1234',
                     'namespace': 'secmon',
                     'udp_port': '1234',
                     'ipsec_ems_fqdn': '10.42.0.113',
                     'col_type': 'sflow',                   # valid coltype
                     'ip_address': '10.42.0.164',
                     'encapsulation_protocol': 'udp'}
      
    
    def tearDown(self):
        pass

    def test_collector_verify_arguments_with_invalid_data(self):
        """test case to test verify_arguments function with invalid data
        """
        self.subcommand_class = self.commands.get('collector-create')
        with self.assertRaises(argparse.ArgumentTypeError):
#         self.assertEqual(True, isinstance(result, argparse.ArgumentParser))
            self.subcommand_class().verify_arguments(self.invalid_data)

    def test_collector_update_verify_arguments_with_invalid_date(self):
        """test case to verify verify_arguments for collector update with invalid data
        """
        self.subcommand_class = self.commands.get('collector-update')
        with self.assertRaises(argparse.ArgumentTypeError):
            self.subcommand_class().verify_arguments(self.invalid_data)

    def test_collector_verify_arguments_with_valid_data(self):
        """test case to test verify_arguments function with valid data
        """
        self.subcommand_class = self.commands.get('collector-create')
#        with self.assertRaises(argparse.ArgumentTypeError):
        result=self.subcommand_class().verify_arguments(self.valid_data)
        self.assertEqual(None, result)

    def test_collector_update_verify_arguments_with_valid_date(self):
        """test case to verify verify_arguments for collector update with valid data
        """
        self.subcommand_class = self.commands.get('collector-update')
        result= self.subcommand_class().verify_arguments(self.valid_data)
        self.assertEqual(None, result)

    def test_add_Argument_with_valid_parser(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('collector-create')
        parser = argparse.ArgumentParser(description='parser for collector arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
#        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.name,'test')
        self.assertEqual(arg1.col_type,None)
        self.assertEqual(arg1.encapsulation_protocol,None) 
        self.assertEqual(arg1.ip_address,None)
        self.assertEqual(arg1.udp_port,None)

#    def test_add_Argument_with_invalid_parser(self):
#        """test case to test add_argument with invalid data
#        """
#        self.subcommand_class = self.commands.get('collector-create') 
#        parser = argparse.ArgumentParser(description='parser for collector arguments')
#        with self.assertRaises(argparse.ArgumentTypeError):
#            parser = self.subcommand_class().add_known_arguments(None)

    def test_add_argument_show(self):
        #test case to test add_argument in show with valid data
        
        self.subcommand_class = self.commands.get('collector-show')
        parser =  argparse.ArgumentParser(description='parser for collector arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
#        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_argument_list(self):
       # test case to test add_argument in list with valid data
        
        self.subcommand_class = self.commands.get('collector-list')
        parser =  argparse.ArgumentParser(description='parser for collector arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
 #       args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.show_details,None)
        self.assertEqual(arg1.fields,None)
        self.assertEqual(arg1.sort_key,None)
        self.assertEqual(arg1.sort_direction,None)
#       self.assertEqual(arg1.format,None)

    def test_add_argument_delete(self):
        #test case to test add_argument in delete with valid data
        
        self.subcommand_class = self.commands.get('collector-delete')
        parser =  argparse.ArgumentParser(description='parser for collector arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
#        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)
    def test_add_Argument_with_valid_parser_update(self):
       # test case to test add_argument with valid data
        
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('collector-update')
        parser = argparse.ArgumentParser(description='parser for collector arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
#        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.name,'test')
        self.assertEqual(arg1.id,None)
        self.assertEqual(arg1.col_type,None)
        self.assertEqual(arg1.encapsulation_protocol,None)
        self.assertEqual(arg1.ip_address,None)
        self.assertEqual(arg1.udp_port,None)

    def validate_run(self):
       # test to validate run with valid data
        
        result = shell.run(self,self.commands)

