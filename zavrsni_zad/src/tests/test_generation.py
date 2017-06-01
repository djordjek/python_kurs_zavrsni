import unittest
from nose_parameterized import parameterized

from code_generation.generator import CodeGen
from code_generation.settings import RESOURCES

class TestCodeGen(unittest.TestCase):

    def setUp(self):
       
        author = "Djordje Kovacevic"
        BLK_MAP = {"trapezoid": "izlaz", "rectangle": "obrada", "trapezoid2": "ulaz"} 
        
        self.code_gen = CodeGen(author, BLK_MAP)
       
        
    def test_valid_graph_user_functions_generate (self):
       
        generated = self.code_gen.generate(RESOURCES + "zadatak_korisnicka.graphml", "main_user_functions.c") 
        self.assertEqual(generated, True)
      
      
    def test_valid_graph_generate (self):
       
        generated = self.code_gen.generate(RESOURCES + "zadatak.graphml", "main_user_function.c") 
        self.assertEqual(generated, True)
        
     
    def test_valid_simple_graph_generate (self):
       
        generated = self.code_gen.generate(RESOURCES + "simple.graphml", "simple.c") 
        self.assertEqual(generated, True)
        
      
    @parameterized.expand([
        (RESOURCES + "zadatak_2_inputs.graphml", "main.c"),
        (RESOURCES + "zadatak_circular.graphml", "main.c")
    ])       
    def test_invalid_graph_generate (self, input_file, expected_file):
       
        generated = self.code_gen.generate(input_file, expected_file) 
        self.assertEqual(generated, False)
            
    