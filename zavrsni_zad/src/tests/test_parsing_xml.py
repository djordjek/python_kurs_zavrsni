## @package test_parsing_xml
#  Test methods for parsing xml file

import unittest

from parse_and_validate_xml_file.parse_validate_xml_file import ParseXMLFile
from utils.settings import RESOURCES
from utils.exceptions import CustomException

class TestParseXML(unittest.TestCase):

    def setUp(self):
       
        BLK_MAP = {"trapezoid": "izlaz", "rectangle": "obrada", "trapezoid2": "ulaz"} 
        self.parse_xml = ParseXMLFile(BLK_MAP)


    def test_generate_tree(self):  
         
        self.assertEqual(self.parse_xml.generate_tree(RESOURCES + "zad.graphml"), None)
    
        
    def test_generate_dictionary(self):  
        
        data = {'n0': ['ulaz', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']], 
                'n3': ['blok_4', 'tanges', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'izlaz',['n1'], []],
                'n5': ['blok_2', 'kosinus', 'obrada', ['n2'], ['n6']],
                'n6': ['izlaz_2', None, 'izlaz', ['n5'], []],
                'n7': ['izlaz_1',None, 'izlaz', ['n3'], []]}
        
        tree = self.parse_xml.generate_tree(RESOURCES + 'zadatak.graphml')
        self.assertEqual(self.parse_xml.parse_xml_file_and_generate_dictionary(tree), data, "Generated dictionary is valid")
        
    
    def test_invalid_input_generate_dictionary(self):  
        
        data = {'n0': ['ulaz11', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']], 
                'n3': ['blok_4', 'tanges', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'izlaz',['n1'], []],
                'n5': ['blok_2', 'kosinus', 'obrada', ['n2'], ['n6']],
                'n6': ['izlaz_2', None, 'izlaz', ['n5'], []],
                'n7': ['izlaz_1',None, 'izlaz', ['n3'], []]}
        
        tree = self.parse_xml.generate_tree(RESOURCES + 'zadatak.graphml')
        self.assertNotEqual(self.parse_xml.parse_xml_file_and_generate_dictionary(tree), data, "Generated dictionary is not valid")
  
        
    def test_validate_xml_file(self):
        
        data = {'n0': ['ulaz', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']], 
                'n3': ['blok_4', 'tanges', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'izlaz',['n1'], []],
                'n5': ['blok_2', 'kosinus', 'obrada', ['n2'], ['n6']],
                'n6': ['izlaz_2', None, 'izlaz', ['n5'], []],
                'n7': ['izlaz_1',None, 'izlaz', ['n3'], []]}
        
        
        self.assertEqual(self.parse_xml.validate_xml_file(data), True)
        
        
    def test_validate_xml_file_more_than_one_inputs(self):
        
        data = {'n0': ['ulaz', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']], 
                'n3': ['blok_4', 'tanges', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'izlaz',['n1'], []],
                'n5': ['blok_2', 'kosinus', 'obrada', [], ['n1']],
                'n6': ['izlaz_2', None, 'izlaz', ['n5'], []],
                'n7': ['izlaz_1',None, 'izlaz', ['n3'], []]}
        
        
        self.assertRaises(CustomException, self.parse_xml.validate_xml_file, data)
        
    def test_validate_xml_file_two_input_blocks(self):
        
        data = {'n0': ['ulaz', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']], 
                'n3': ['blok_4', 'ulaz', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'izlaz',['n1'], []],
                'n5': ['blok_2', 'kosinus', 'obrada', [], ['n1']],
                'n6': ['izlaz_2', None, 'izlaz', ['n5'], []],
                'n7': ['izlaz_1',None, 'izlaz', ['n3'], []]}
        
        
        self.assertRaises(CustomException, self.parse_xml.validate_xml_file, data)
        
    def test_validate_xml_file_no_output_block(self):
        
        data = {'n0': ['ulaz', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']], 
                'n3': ['blok_4', 'ulaz', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'obrada',['n1'], []]}
        
        
        self.assertRaises(CustomException, self.parse_xml.validate_xml_file, data)
        
    def test_validate_xml_file_blocks_not_connected(self):
        
        data = {'n0': ['ulaz', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', [], ['n5']], 
                'n3': ['blok_4', 'ulaz', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'obrada',['n1'], []]}
        
        
        self.assertRaises(CustomException, self.parse_xml.validate_xml_file, data)

