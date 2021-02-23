from Graph import Graph
from BRD import BRD
from Utils import set_graph,generate_12_8b,generate_12_10

#generate_12_8b("Examples/12.8b",0.5,5)
#generate_12_10("Examples/12.10",0.5,5)
agents, source, g = set_graph("Examples/12.10")
brd = BRD(g,agents,source)
#brd.plot_graph()
brd()
