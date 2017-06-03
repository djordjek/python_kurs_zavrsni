## @package graph
#  Create graph and extract graph path using dfs algorithm


## @brief Create dictionary with name of block as key and list of next blocks as value 
#
# @param nodes_dictionary dictionary created from xml file
# @param BLK_MAP Block types
# @return graph Return blocks with its next blocks
# @return input_block Name of input block in diagram
def create_graph(nodes_dictionary, BLK_MAP):
    '''
    Create dictionary with name of block as key and list of next blocks as value 
    :param nodes_dictionary: Dictionary created from xml file
    :param BLK_MAP: Block types
    '''
    graph = {}
    input_block = ""
    for key, value in nodes_dictionary.iteritems():
        block_type = value[2]
        
        if(block_type == BLK_MAP['trapezoid2']):
            input_block = key
        graph[key] = value[4]
        
    return (graph, input_block)

## @brief iterative depth first search from start 
#
# @param graph Graph path
# @param start Input block in diagram  
# @return graph Return graph path
def iterative_dfs(graph, start, path=[]):
    q=[start]
    while q:
        v=q.pop(0)
        if v not in path:
            path=path+[v]
            q=graph[v]+q
    return path

