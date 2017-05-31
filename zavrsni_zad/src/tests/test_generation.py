import unittest
from nose_parameterized import parameterized

from code_generation.generator import CodeGen

class TestCodeGen(unittest.TestCase):
    

    def setUp(self):
       
        author = "Djordje Kovacevic"
        BLK_MAP = {"trapezoid": "izlaz", "rectangle": "obrada", "trapezoid2": "ulaz"} 
        
        self.code_gen = CodeGen(author, BLK_MAP)
        
    def test_valid_graph_user_function_generate (self):
       
        generated = self.code_gen.generate("zadatak_korisnicka.graphml", "main.c") 
        self.assertEqual(generated, True)
    """    
    def test_valid_graph_generate (self):
       
        generated = self.code_gen.generate("zadatak.graphml", "main.c") 
        self.assertEqual(generated, True)
        
     
    def test_valid_simple_graph_generate (self):
       
        generated = self.code_gen.generate("simple.graphml", "simple.c") 
        self.assertEqual(generated, True)
        
      
    @parameterized.expand([
        ("zadatak_2_inputs.graphml", "main.c"),
        ("zadatak_circular.graphml", "main.c")
    ])       
    def test_invalid_graph_generate (self, input_file, expected_file):
       
        generated = self.code_gen.generate(input_file, expected_file) 
        self.assertEqual(generated, False)
            
    
    def test_generate_tree(self):  
         
        self.assertEqual(self.code_gen.generate_tree("zad.graphml"), None)
    """