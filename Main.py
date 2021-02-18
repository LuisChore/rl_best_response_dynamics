from Graph import Graph
from BRD import BRD
from Utils import set_graph

agents, source, g = set_graph("example.txt")
brd = BRD(g,agents,source)
brd.plotProcess.plot_graph(agents,source)
brd()
brd.plot_metrics()
brd.plot_status()
