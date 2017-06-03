## @package test_graph
#  Test methods for graph

import unittest
from nose_parameterized import parameterized

from graph.graph import iterative_dfs, create_graph 

class TestUtils(unittest.TestCase):
    
    def setUp(self):
       
        self.BLK_MAP = {"trapezoid": "izlaz", "rectangle": "obrada", "trapezoid2": "ulaz"} 
    
    @parameterized.expand([
        ({'n0': ['n1'], 'n1': ['n2', 'n4', 'n3'], 'n2': ['n5'], 'n3': ['n7'], 'n4': [], 'n5': ['n6'], 'n6': [], 'n7': []},
          "n0",
          ['n0', 'n1', 'n2', 'n5', 'n6', 'n4', 'n3', 'n7']),
          
          ({'n0': ['n1'], 'n1': ['n2', 'n4', 'n3'], 'n2': ['n5', 'n8'], 'n3': ['n7'], 'n4': [], 'n5': ['n6'], 'n6': [], 'n7': [], 'n8': []},
          "n0",
          ['n0', 'n1', 'n2', 'n5', 'n6', 'n8', 'n4', 'n3', 'n7'])
    ])
    def test_iterative_dfs(self, graph, start, result_dfs):
        self.assertEqual(iterative_dfs(graph, start, path=[]), result_dfs)
        
    
    def test_create_graph(self):
        
        nodes_dictionary = {'n0': ['ulaz', None, 'ulaz', [], ['n1']],
                'n1': ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']],
                'n2': ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']], 
                'n3': ['blok_4', 'tanges', 'obrada', ['n1'], ['n7']],
                'n4': ['izlaz_3', None, 'izlaz',['n1'], []],
                'n5': ['blok_2', 'kosinus', 'obrada', ['n2'], ['n6']],
                'n6': ['izlaz_2', None, 'izlaz', ['n5'], []],
                'n7': ['izlaz_1',None, 'izlaz', ['n3'], []]}
        
        excepted_result = {'n0': ['n1'], 'n1': ['n2', 'n4', 'n3'], 'n2': ['n5'], 'n3': ['n7'], 'n4': [], 'n5': ['n6'], 'n6': [], 'n7': []};
        
        graph, input_block = create_graph(nodes_dictionary, self.BLK_MAP)
        self.assertEqual(graph, excepted_result)
        self.assertEqual(input_block, "n0")