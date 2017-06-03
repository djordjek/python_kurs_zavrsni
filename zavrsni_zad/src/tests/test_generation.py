## @package test_generation
#  Test methods for code generation

import unittest
from nose_parameterized import parameterized

from code_generation.generator import CodeGen
from utils.settings import RESOURCES

class TestCodeGen(unittest.TestCase):

    def setUp(self):
       
        author = "Djordje Kovacevic"
        BLK_MAP = {"trapezoid": "izlaz", "rectangle": "obrada", "trapezoid2": "ulaz"} 
        
        self.code_gen = CodeGen(author, BLK_MAP)
       
        
    def test_graph_user_functions_generate (self):
       
        generated = self.code_gen.generate(RESOURCES + "zadatak_korisnicka.graphml", "main.c") 
        self.assertEqual(generated, True)
        
     
    def test_simple_graph_generate (self):
       
        generated = self.code_gen.generate(RESOURCES + "simple.graphml", "simple.c") 
        self.assertEqual(generated, True)
        
      
    @parameterized.expand([
        (RESOURCES + "zadatak_2_inputs.graphml", "main.c"),
        (RESOURCES + "zadatak_circular.graphml", "main.c")
    ])       
    def test_graph_generate_invalid_input(self, input_file, expected_file):
       
        generated = self.code_gen.generate(input_file, expected_file) 
        self.assertEqual(generated, False)
        
    def test_generate_list_of_user_function_names(self):
        
        nodes_dictionary = {'n0': ['ulaz', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']], 
                'n3': ['blok_4', 'tanges', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'izlaz',['n1'], []],
                'n5': ['blok_2', 'kosinus', 'obrada', ['n2'], ['n6']],
                'n6': ['izlaz_2', None, 'izlaz', ['n5'], []],
                'n7': ['izlaz_1',None, 'izlaz', ['n3'], []]}
        
        actual_result = self.code_gen.generate_list_of_user_function_names(nodes_dictionary)
        expected_result = ['korisnicka1']
        
        self.assertEqual(actual_result, expected_result)
        
        
    def test_generate_statements(self):       
        
        data = {'n0': ['ulaz', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']], 
                'n3': ['blok_4', 'tanges', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'izlaz',['n1'], []],
                'n5': ['blok_2', 'kosinus', 'obrada', ['n2'], ['n6']],
                'n6': ['izlaz_2', None, 'izlaz', ['n5'], []],
                'n7': ['izlaz_1',None, 'izlaz', ['n3'], []]} 
        
        graph = {'n0': ['n1'], 'n1': ['n2', 'n4', 'n3'], 'n2': ['n5'], 'n3': ['n7'], 'n4': [], 'n5': ['n6'], 'n6': [], 'n7': []}
        
        actual_result = self.code_gen.generate_statements(data, graph)
        expected_result =     ["ulaz_var = ulaz();",
                                 "blok_1_var = sinus(ulaz_var);",
                                 "blok_3_var = korisnicka1(blok_1_var);",
                                 "blok_4_var = tanges(blok_1_var);",
                                 "izlaz(blok_1_var);",
                                 "blok_2_var = kosinus(blok_3_var);",
                                 "izlaz(blok_2_var);",
                                 "izlaz(blok_4_var);"]
        
        self.assertEqual(actual_result, expected_result)
        
    