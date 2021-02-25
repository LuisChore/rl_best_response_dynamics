from Graph import Graph
from BRD import BRD
from Utils import *

#generate_12_8b("Examples/12.8b",0.5,5)
#generate_12_10("Examples/12.10_paths",0.5,5,paths = True)
agents, source, g = set_graph("Examples/12.8a",paths = True)
brd = BRD(g,agents,source)
#brd.plot_graph()
brd()
