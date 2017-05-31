import os
import time
from collections import OrderedDict

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from code_generation.settings import DESTINATION, TEMPLATES_ROOT


from lxml import objectify

class CodeGen(object):
    
    ## @brief Constructor
    #
    # @param author Author of project
    # @param BLK_MAP Block types (input, output and process block)
    def __init__(self, author, BLK_MAP):                     
        
        self._author = author 
        self.BLK_MAP = BLK_MAP
    
    ##  @brief Activates code generation   
    #
    # @param input_file Name of xml file
    # @param output_file Name of a generated file 
    # @return True, if code is successfully generated, False otherwise
    def generate(self, input_file, output_file):
        
        try:
            
            tree = self.generate_tree(input_file)
        
            nodes_dictionary = self.generate_dictionary(tree)
            
            self.validate_xml_file(nodes_dictionary)
            
            statements = self.generate_statements(nodes_dictionary)
            
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

        except:
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
        
    
    ## Open xml file, generate tree and close xml file    
    def generate_tree(self, input_file):
             
        try:      
            with open(input_file, 'rb') as graphml_file:     
                tree = objectify.parse(graphml_file)
            
            return tree 
        except:
            return None
    
    ## Generate list of user function names      
    def generate_list_of_user_function(self, nodes_dictionary):
        
        users_functions = []
            
        for node_name in nodes_dictionary:
            
            data_value = nodes_dictionary[node_name]
            
            block_type = data_value[2]
            
            if (block_type == self.BLK_MAP['rectangle']):
                function_name = data_value[1]
                if (function_name != "sinus" and function_name != "tanges" and function_name != "kosinus"):
                    users_functions.append(function_name)
        
        return users_functions
        
    ## Generate dictionary from 'node' and 'edge' tags
    def generate_dictionary(self, tree):
        
        
        """
        n0: ['ulaz', 'undefined_function', 'ulaz', [], ['n1']]
        n1: ['blok_1', 'sinus', 'obrada', ['n0'], ['n2', 'n4', 'n3']]
        n2: ['blok_3', 'korisnicka1', 'obrada', ['n1'], ['n5']]
        n3: ['blok_4', 'tanges', 'obrada', ['n1'], ['n7']]
        n4: ['izlaz_3', 'undefined_function', 'izlaz', ['n1'], []]
        n5: ['blok_2', 'kosinus', 'obrada', ['n2'], ['n6']]
        n6: ['izlaz_2', 'undefined_function', 'izlaz', ['n5'], []]
        n7: ['izlaz_1', 'undefined_function', 'izlaz', ['n3'], []]

        """
 
        ## Get root tag in xml file
        root = tree.getroot()

        data = OrderedDict()
        next_blocks = []
        prev_state_of_cur_node = "";
        
        ## List of 'target' attribute values from xml file
        targets = []
        
        ## Extract 'edge' tags
        link_elements = root.findall(".//{*}edge")

        ## Extract 'node' tags
        node_elements = root.findall(".//{*}node")

        ## Navigate through all 'node' tags
        for node in node_elements:
            
            ## Get id of node
            node_id = node.attrib['id']
            
            ## Get block type
            bl_type_el = node.find(".//{*}Shape")
            block_type = bl_type_el.attrib['type']
            
            ## Get function name
            fn_type_el = node.find('.//{*}data[@key="d5"]')
            
            ## Get block name
            block_name = node.find(".//{*}NodeLabel").text
            block_name = block_name.replace(" ", "_")
            
            ## Create dictionary
            data[node_id] = [block_name, fn_type_el, self.BLK_MAP[block_type], [], []]
            
        ## Navigate through all 'edge' tags
        for link in link_elements:
            current_node = link.attrib['source']
            next_node = link.attrib['target']
            
            
            ## Example:
            ## <edge id="e1" source="n1" target="n2">
            ## <edge id="e1" source="n3" target="n2">
            
            ## Check if blocks have more than one input and check if loops are detected
            if(next_node in targets):
                raise Exception("Block : " + str(next_node) + " has more than one input!")
            targets.append(next_node)
            
            ## Example: <edge id="e1" source="n1" target="n1"></edge>
            if(current_node == next_node):
                raise Exception("Cycle structure detected!")
            
            ## Check if current 'source' attribute value different than previously remembered 'source' attribute value
            if(current_node != prev_state_of_cur_node):
                next_blocks = []
            
            ## Set next blocks of current block
            next_blocks.append(next_node)
            data[current_node][4] = next_blocks
            
            ## Set previous blocks of current block
            prev_blocks = []
            prev_blocks.append(current_node)
            data[next_node][3] = prev_blocks
            
            ## Remember 'source' attribute value
            prev_state_of_cur_node = current_node; 
            
        return data    
            
    ## Validate diagram         
    def validate_xml_file(self, data): 
 
        ## Diagram must have only one input block and more than one output block 
        inputs = 0
        number_empty_prev_blocks = 0
        
        outputs = 0
        number_empty_next_blocks = 0

        for node_name in data:
            data_value = data[node_name]
            
            block_type = data_value[2]
            prev_blocks = data_value[3]
            next_blocks = data_value[4]
            
            if(block_type == 'ulaz'):
                inputs += 1
                
                
            if(block_type == 'ulaz' and (len(prev_blocks) == 0)):
                number_empty_prev_blocks += 1
                
            if(block_type == 'izlaz'):
                outputs += 1
                
            if(block_type == 'izlaz' and (len(next_blocks) == 0)):
                number_empty_next_blocks += 1
                
        
        if (inputs > 1 or number_empty_prev_blocks > 1):
            raise Exception("Detected more than one input block")
        
        if (outputs == 0 or number_empty_next_blocks == 0):
            raise Exception("Zero output blocks detected")
            
        
        ## All blocks must be connected
        for node_name in data:
            data_value = data[node_name]
            
            block_type = data_value[2]
            prev_blocks = data_value[3]
            next_blocks = data_value[4]
            
            if(block_type == 'ulaz'):
                if(len(next_blocks) == 0):
                    raise Exception("Input block is not connected to any other block")
                
            if(block_type == 'izlaz'):
                if(len(prev_blocks) == 0):
                    raise Exception("Output block is not connected to any other block")
                
            if(block_type == 'obrada'):
                if (len(prev_blocks) == 0):
                    raise Exception("Process block doesn't have input")
                if (len(next_blocks) == 0):
                    raise Exception("Process block doesn't have output")
                
               
    ## Generate call to functions in main.c
    def generate_statements(self, data):        
        statements = []
        
        for node_name in data:
            
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