from Graph import Graph
from BRD import BRD
from Utils import set_graph

agents, source, g = set_graph("example.txt")
brd = BRD(g,agents,source)
brd.plotProcess.plot_graph()
brd()
brd.plotProcess.plot_metrics(brd.agents,brd.source,brd.cost_by_iteration)
brd.plotProcess.draw_plot(brd.agents,brd.source,brd.total_cost,block = True)
