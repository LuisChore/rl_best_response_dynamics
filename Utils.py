from Graph import Graph

def set_graph(file_name):
    f = open(file_name, "r")
    nodes,edges = f.readline().split()
    g = Graph(int(nodes),True)
    for i in range(int(edges)):
        u,v,w = f.readline().split()
        g.add_edge(int(u),int(v),int(w))
    agents = [int(x) for x in f.readline().split()]
    source = int(f.readline())
    return  agents,source,g
