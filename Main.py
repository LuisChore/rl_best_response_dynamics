from Graph import Graph
from BRD import BRD
from Utils import set_graph

agents, source, g = set_graph("Examples/12.8a")
brd = BRD(g,agents,source)
#brd.plot_graph()
brd()
