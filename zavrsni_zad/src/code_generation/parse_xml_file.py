from lxml import objectify

from code_generation.exceptions import CustomException

class ParseXMLFile(object):

    def __init__(self, block_type):
        self.BLK_MAP = block_type

    ## Open xml file, generate tree and close xml file    
    def generate_tree(self, input_file):
             
        try:      
            with open(input_file, 'rb') as graphml_file:     
                tree = objectify.parse(graphml_file)
            
            return tree 
        except:
            return None
        
        
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

        data = {}
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
                raise CustomException("Block : " + str(next_node) + " has more than one input!")
            targets.append(next_node)
            
            ## Example: <edge id="e1" source="n1" target="n1"></edge>
            if(current_node == next_node):
                raise CustomException("Cycle structure detected!")
            
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
            raise CustomException("Detected more than one input block")
        
        if (outputs == 0 or number_empty_next_blocks == 0):
            raise CustomException("Zero output blocks detected")
            
        
        ## All blocks must be connected
        for node_name in data:
            data_value = data[node_name]
            
            block_type = data_value[2]
            prev_blocks = data_value[3]
            next_blocks = data_value[4]
            
            if(block_type == 'ulaz'):
                if(len(next_blocks) == 0):
                    raise CustomException("Input block is not connected to any other block")
                
            if(block_type == 'izlaz'):
                if(len(prev_blocks) == 0):
                    raise CustomException("Output block is not connected to any other block")
                
            if(block_type == 'obrada'):
                if (len(prev_blocks) == 0):
                    raise CustomException("Process block doesn't have input")
                if (len(next_blocks) == 0):
                    raise CustomException("Process block doesn't have output")
        return True