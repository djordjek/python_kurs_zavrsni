import os
import time

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from code_generation.settings import DESTINATION, TEMPLATES_ROOT
from utils.utils import iterative_dfs
from utils.utils import create_graph

from code_generation.parse_xml_file import ParseXMLFile
from code_generation.exceptions import CustomException

class CodeGen(object):
    
    ## @brief Constructor
    #
    # @param author Author of project
    # @param _BLK_MAP Block types (input, output and process block)
    def __init__(self, author, BLK_MAP):                     
        
        self._author = author 
        self._BLK_MAP = BLK_MAP
        self.parseXmlFile = ParseXMLFile(self._BLK_MAP)
    
    ##  @brief Activates code generation   
    #
    # @param input_file Name of xml file
    # @param output_file Name of a generated file 
    # @return True, if code is successfully generated, False otherwise
    def generate(self, input_file, output_file):
        
        try:

            ## Generate tree from input xml file
            tree = self.parseXmlFile.generate_tree(input_file)
            
            ## Generate dictionary from tree
            nodes_dictionary = self.parseXmlFile.generate_dictionary(tree)
            
            ## Generate dictionary from tree
            self.parseXmlFile.validate_xml_file(nodes_dictionary)
            
            ## Creating graph and creating path from graph using dfs
            graph, input_block = create_graph(nodes_dictionary, self._BLK_MAP)  
            graph_path = iterative_dfs(graph, input_block)
            
            statements = self.generate_statements(nodes_dictionary, graph_path)
            
            users_functions = self.generate_list_of_user_function(nodes_dictionary)
            
            ## Loader for templates from disk    
            file_system_loader = FileSystemLoader([TEMPLATES_ROOT])                       
            
            destination_path = os.path.join(DESTINATION, output_file)                                   
                             
            ## Setting environment for code generation                       
            env=Environment(loader=file_system_loader, trim_blocks = True)
                    
            ## Getting main template                 
            template = env.get_template("main.template")
                            
            ## Dictionary for passing data to code generator                        
            data = {}
            data["author"] = self._author
            data["date"] = time.strftime("%d.%m.%Y %H:%M:%S")
            data["statements"] = statements
            data["nodes"] = nodes_dictionary
            data["users_functions"] = users_functions
            data["user_functions_exist"] = False 
            
            ## Generate user files   
            self.generate_user_files(users_functions, data, env)
            
            ## Generate 'main.c' file        
            template.stream(data).dump(os.path.join(destination_path))  

        except CustomException as err:
            print(err.message)
            return False
        
        return True
    
    ## Generate user files which contains user functions
    def generate_user_files(self, users_functions, data, env):
        
        ## Check if exists any user function in xml file
        if(len(users_functions) > 0):
            
            file_name_of_user_function = "user_function";
            
            h_file_of_user_func = file_name_of_user_function + ".h"
            c_file_of_user_func = file_name_of_user_function + ".c"
            
            data["user_functions_exist"] = True
            data["user_function_name"] = file_name_of_user_function
            
            if not(os.path.exists(os.path.join(DESTINATION, h_file_of_user_func))):
                  
                template_prototypes = env.get_template("user_function_prototypes.template")
                template_prototypes.stream(data).dump(DESTINATION + os.sep + h_file_of_user_func)
                
            if not(os.path.exists(os.path.join(DESTINATION, c_file_of_user_func))):    
                data["func_body"] = "return 0;" 
                template_functions = env.get_template("user_function.template")
                template_functions.stream(data).dump(DESTINATION + os.sep + c_file_of_user_func)
        
    
    ## Generate list of user function names      
    def generate_list_of_user_function(self, nodes_dictionary):
        
        users_functions = []
            
        for node_name in nodes_dictionary:
            
            data_value = nodes_dictionary[node_name]
            
            block_type = data_value[2]
            
            if (block_type == self._BLK_MAP['rectangle']):
                function_name = data_value[1]
                if (function_name != "sinus" and function_name != "tanges" and function_name != "kosinus"):
                    users_functions.append(function_name)
        
        return users_functions
               
    ## Generate call to functions in main.c
    def generate_statements(self, data, graph):        
        statements = []
        
        for node_name in graph:
            
            data_value = data[node_name]
            block_type = data_value[2]
            
            ## Generate statement for input block
            if(block_type == 'ulaz'):
                statements.append(data_value[2] + "_var = " + data_value[2] + "();")
                continue
            
            ## Generate statements for process blocks
            prev_block = data_value[3][0];
            if(block_type == 'obrada'):
                variable = data_value[0] + "_var";
                function_name = data_value[1]
                
                for key in data.keys():
                    if(key == prev_block):
                        arg = data[key][0] + "_var";
                        statements.append(variable + " = " + function_name + "(" + arg + ");")
                        break
            
            ## Generate statements for output blocks
            else:
                for key in data.keys():
                    if(key == prev_block):
                        arg = data[key][0] + "_var";
                        function_name = data_value[2]
                        statements.append(function_name + "(" + arg + ");")
                        break
             
        return statements