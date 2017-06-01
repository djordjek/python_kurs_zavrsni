
import unittest

from code_generation.parse_xml_file import ParseXMLFile
from code_generation.settings import RESOURCES
from code_generation.exceptions import CustomException

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
        self.assertEqual(self.parse_xml.generate_dictionary(tree), data, "Generated dictionary is valid")
        
    
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
        self.assertNotEqual(self.parse_xml.generate_dictionary(tree), data, "Generated dictionary is not valid")
  
        
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
        
        
    def test_validate_xml_file_invalid_input(self):
        
        data = {'n0': ['ulaz', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']], 
                'n3': ['blok_4', 'tanges', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'izlaz',['n1'], []],
                'n5': ['blok_2', 'kosinus', 'obrada', [], ['n1']],
                'n6': ['izlaz_2', None, 'izlaz', ['n5'], []],
                'n7': ['izlaz_1',None, 'izlaz', ['n3'], []]}
        
        
        self.assertRaises(CustomException, self.parse_xml.validate_xml_file, data)

