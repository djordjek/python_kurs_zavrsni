## @briefCreate graph in form of dictionary
#
# @param nodes_dictionary dictionary created from xml file
# @param BLK_MAP Block types
def create_graph(nodes_dictionary, BLK_MAP):
    graph = {}
    input_block = ""
    for key, value in nodes_dictionary.iteritems():
        block_type = value[2]
        
        if(block_type == BLK_MAP['trapezoid2']):
            input_block = key
        graph[key] = value[4]
        
    return (graph, input_block)

## iterative depth first search from start  
def iterative_dfs(graph, start, path=[]):
    q=[start]
    while q:
        v=q.pop(0)
        if v not in path:
            path=path+[v]
            q=graph[v]+q
    return path

