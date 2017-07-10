from unittest import TestCase
import argparse
import pdb
#sys.path.append(os.path.abspath('..'))
from secmonclient.v1_0.vpn import classificationobject

class TestClassificationObject(TestCase):
    def setUp(self):
#        pdb.set_trace()
        self.commands = {
            'classificationobject-create':
                classificationobject.CreateClassificationObject,
            'classifictaionobject-list':
                classificationobject.ListClassificationObject,
            'classificationobject-show':
                classificationobject.ShowClassificationObject,
            'classificationobject-update':
                classificationobject.UpdateClassificationObject,
            'classificationobject-delete':
                classificationobject.DeleteClassificationObject
                   }

    
    def tearDown(self):
        pass

    def test_add_Argument_with_valid_parser(self):
        """test case to test add_argument with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('classificationobject-create')
        parser = argparse.ArgumentParser(description='parser for classificationobject arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        print("arg1 in test_add_Argument_with_valid_parser:", arg1)
        self.assertEqual(arg1.name,'test')
        self.assertEqual(arg1.src_ip,None)
        self.assertEqual(arg1.src_mac,None) 
        self.assertEqual(arg1.src_ip_subnet,None)
        self.assertEqual(arg1.minimum_src_port,None)
        self.assertEqual(arg1.maximum_src_port,None)
        self.assertEqual(arg1.dst_ip,None)
        self.assertEqual(arg1.dst_mac,None)
        self.assertEqual(arg1.dst_ip_subnet,None)
        self.assertEqual(arg1.minimum_dst_port,None)
        self.assertEqual(arg1.maximum_dst_port,None)
        self.assertEqual(arg1.protocol,None)

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
        self.subcommand_class = self.commands.get('classificationobject-show')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.id, None)

    def test_add_argument_list(self):
        """test case to test add_argument in list with valid data
        """
        self.subcommand_class = self.commands.get('classificationobject-list')
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
        self.subcommand_class = self.commands.get('classificationobject-delete')
        parser =  argparse.ArgumentParser(description='parser for arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        print("parser in test_add_argument_delete:", parser)
        args = parser.parse_known_args()
        print("args in test_add_argument_delete:", args)
        arg1 = parser.parse_args()
        print("arg1 in test_add_argument_delete:", arg1)
        self.assertEqual(arg1.id, None)

    def test_add_Argument_with_valid_parser_update(self):
        """test case to test add_argument in update with valid data
        """
#        pdb.set_trace()
        self.subcommand_class = self.commands.get('classificationobject-update')
        parser = argparse.ArgumentParser(description='parser for classificationobject arguments')
        parser = self.subcommand_class().add_known_arguments(parser)
        args = parser.parse_known_args()
        arg1 = parser.parse_args()
        self.assertEqual(arg1.name,'test')
        self.assertEqual(arg1.src_ip,None)
        self.assertEqual(arg1.src_mac,None)
        self.assertEqual(arg1.id,None)
        self.assertEqual(arg1.src_ip_subnet,None)
        self.assertEqual(arg1.minimum_src_port,None)
        self.assertEqual(arg1.maximum_src_port,None)
        self.assertEqual(arg1.dst_ip,None)
        self.assertEqual(arg1.dst_mac,None)
        self.assertEqual(arg1.dst_ip_subnet,None)
        self.assertEqual(arg1.minimum_dst_port,None)
        self.assertEqual(arg1.maximum_dst_port,None)
        self.assertEqual(arg1.protocol,None)

