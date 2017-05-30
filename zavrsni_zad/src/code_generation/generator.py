
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from code_generation.settings import DESTINATION, TEMPLATES_ROOT

import os
import time
from collections import OrderedDict

from lxml import objectify

class CodeGen(object):
    """
    CodeGen example no. 1: using static text and variables
    """
    
    def __init__(self, author):
        """
        Constructor        
         
        Args:
            author: author name          
        """                        
        self._author = author 
        self.BLK_MAP = {"trapezoid": "izlaz", "rectangle": "obrada", "trapezoid2": "ulaz"} 
        self.file_name_of_user_function = "user_function";
        
    def generate(self, input_file, output_file):
        """
        Activates code generation
        
        Args:
            file_name: name of a generated file 
        Returns: 
            True, if code is successfully generated, None otherwise
        """

        
        try:
            
            tree = self.generate_tree(input_file)
        
            nodes_dictionary = self.generate_dictionary(tree)
            
            statements = self.generate_statements(nodes_dictionary)
            
            users_functions = self.generate_korisnicka_function(nodes_dictionary)
            
            #loader for templates from disk:
            #file_system_loader = FileSystemLoader([path1, path2, path3....])
                    
            file_system_loader = FileSystemLoader([TEMPLATES_ROOT])                       
            
            destination_path = os.path.join(DESTINATION, output_file)                                   
                             
            # setting environment for code generation:                         
            env=Environment(loader=file_system_loader, trim_blocks = True)
                    
            # getting main template                 
            template = env.get_template("main.template")
                            
            # dictionary for passing data to code generator:                        
            data = {}
           
            data["author"] = self._author
            data["date"] = time.strftime("%d.%m.%Y %H:%M:%S")
            data["statements"] = statements
            data["nodes"] = nodes_dictionary
            data["users_functions"] = users_functions
            
            
            ## Check if exists any user function in xml file
            if(len(users_functions) > 0):
                
                h_file_of_user_func = self.file_name_of_user_function + ".h"
                c_file_of_user_func = self.file_name_of_user_function + ".c"
                
                data["user_function_name"] = self.file_name_of_user_function
                
                if not(os.path.exists(os.path.join(DESTINATION, h_file_of_user_func))):
                      
                    template_prototypes = env.get_template("user_function_prototypes.template")
                    template_prototypes.stream(data).dump(DESTINATION + os.sep + h_file_of_user_func)
                    
                if not(os.path.exists(os.path.join(DESTINATION, c_file_of_user_func))):    
                    data["func_body"] = "return 0;" 
                    template_functions = env.get_template("user_function.template")
                    template_functions.stream(data).dump(DESTINATION + os.sep + c_file_of_user_func)
                    
            ## Generate 'main.c' file        
            template.stream(data).dump(os.path.join(destination_path))  

        except Exception as e:
            print (e.message)
            return False
        
        return True
    
    ## Open xml file, generate tree and close xml file    
    def generate_tree(self, xml_file):
              
        try:
            graphml_file = open(xml_file, 'rb')
            tree = objectify.parse(graphml_file)
            
            return tree 
        except:
            return None
        finally:
            graphml_file.close()
            
    def generate_korisnicka_function(self, nodes_dictionary):
        
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
 
        ## Get root tag in xml file
        root = tree.getroot()
        
        
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

        data = OrderedDict()

        next_blocks = []
        
        prev_state_of_cur_node = "";

        targets = []
        
        ## Extract needed data from edge tag
        link_elements = root.findall(".//{*}edge")

        ## Extract needed data from node tag
        node_elements = root.findall(".//{*}node")
        
        
        
        for node in node_elements:
            ## Get id of node
            node_id = node.attrib['id']
            
            bl_type_el = node.find(".//{*}Shape")
            block_type = bl_type_el.attrib['type']
            
            fn_type_el = node.find('.//{*}data[@key="d5"]')
            
            block_name = node.find(".//{*}NodeLabel").text
            
            data[node_id] = [block_name, fn_type_el, self.BLK_MAP[block_type], [], []]
            
        
        for link in link_elements:
            current_node = link.attrib['source']
            next_node = link.attrib['target']
            
            ## Example:
            ## <edge id="e1" source="n1" target="n2">
            ## <edge id="e1" source="n3" target="n2">
            if(next_node in targets):
                raise Exception("Block : " + str(next_node) + " has more than one input!")
            targets.append(next_node)
            
            ## Example: <edge id="e1" source="n1" target="n1"></edge>
            if(current_node == next_node):
                raise Exception("Cycle structure detected!")
            
            ## Set next blocks of current blocks
            if(current_node != prev_state_of_cur_node):
                next_blocks = []
            next_blocks.append(next_node)
            data[current_node][4] = next_blocks
            
            ## Set previous blocks of current blocks
            prev_blocks = []
            prev_blocks.append(current_node)
            data[next_node][3] = prev_blocks
            
            
            prev_state_of_cur_node = current_node; 
        
        #################################################
        ### Cycle structure
        ################################################
        ## Already covered with above code:
        ##
        ## Example:
            ## <edge id="e1" source="n1" target="n2">
            ## <edge id="e1" source="n3" target="n2">
            
            
        """
        node_counter = 0;  
        for node_name in data:
            data_value = data[node_name]
            next_blocks = data_value[4]
            for next in next_blocks: 
                counter = 0
                for key in data:  
                    if(counter == node_counter):
                        break
                                 
                    if(key == next):
                        raise Exception("Cycle structure detected!")
                    counter += 1
                    
            node_counter += 1
        """    
            
            
        
        ############################################################################
        # Sema/dijagram mora imati samo jedan ulazni blok i najmanje jedan izlazni
        ###########################################################################
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
            
        ################################################################################   
        ####  Svi blokovi moraju biti povezani
        #####################################################################
    
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
                
        return data           
    #####################################
    ## Generate call to functions in main.c
    ######################################
    
    def generate_statements(self, data):        
        statements = []
        
        for node_name in data:
            
            data_value = data[node_name]
            block_type = data_value[2]
            
            data_value[0] = data_value[0].replace(" ", "_")
            
            if(block_type == 'ulaz'):
                statements.append(data_value[2] + "_var = " + data_value[2] + "()")
                continue
            
            prev_block = data_value[3][0];
            if(block_type == 'obrada'):
                variable = data_value[0] + "_var";
                function_name = data_value[1]
                
                for key in data.keys():
                    if(key == prev_block):
                        arg = data[key][0] + "_var";
                        statements.append(variable + " = " + function_name + "(" + arg + ")")
                        break
            
            ## Output block
            else:
                for key in data.keys():
                    if(key == prev_block):
                        arg = data[key][0] + "_var";
                        function_name = data_value[2]
                        statements.append(function_name + "(" + arg + ")")
                        break
             
        return statements
        
        
         
        
        """
        for link in link_elements:
            current_node = link.attrib['source']
            node_ids.append(current_node)
            if(current_node != temp):
                next_blocks = []
            temp = current_node; 
            next_node = link.attrib['target']
            
            next_blocks.append(next_node)
            data_prev_next[current_node] = [prev_blocks, next_blocks]
            #(data[current_node]).append(next_blocks);
            
        print(data)  
        
        for link in link_elements:
            next_node = link.attrib['target']
            
            ## <edge id="e1" source="n1" target="n2">
            ## <edge id="e1" source="n3" target="n2">
            if(next_node in targets):
                raise Exception("BLock id: " + str(next_node) + " has more than one input!")
            targets.append(next_node)
            
            current_node = link.attrib['source']
            
            ## Example: <edge id="e1" source="n1" target="n1"></edge>
            if(current_node == next_node):
                raise Exception("Cycle structure detected!")

            prev_blocks = []
            prev_blocks.append(current_node)
            if not(next_node in node_ids):
                data_prev_next[next_node] = [prev_blocks, []]
            else:
                data_prev_next[next_node] = [prev_blocks, data_prev_next[next_node][1]]
       
        """    
        print(data)

        