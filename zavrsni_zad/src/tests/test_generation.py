
import unittest
from code_generation.generator import CodeGen

class TestCodeGen(unittest.TestCase):
    

    def setUp(self):
        """
        Setting up test
        """
        self.code_gen = CodeGen("Djordje Kovacevic")
        

    def test_generate (self):
        """
        Testing code generation
        """    
        generated = self.code_gen.generate("zadatak_korisnicka.graphml", "main.c") 
        self.assertEqual(generated, True)      