import unittest
from nose_parameterized import parameterized

from utils.utils import iterative_dfs 

class TestUtils(unittest.TestCase):
    
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