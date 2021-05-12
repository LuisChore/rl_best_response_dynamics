import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import networkx as nx
import numpy as np
from Agent import Agent
from Graph import Graph
import queue

class BRD:
    def __init__(self,graph,agents,source):
        self.nash_eq = False
        self.W,self.H = 12,8
        colors = ['blue','red','green','orange','cyan','black','pink','magenta']
        self.cost_by_iteration = []
        self.total_cost = float("inf")
        self.source = source
        # initialize agents
        self.agents = agents
        iterator = 0
        for ag in self.agents:
            ag.set_color(colors[iterator])
            iterator = (iterator + 1) % len(colors)
        #initialize graph
        self.graph = graph
        self.graphx = self.create_graph(graph)
        #Edges: dictionary to know how many agents are using every edge
        self.Edges = self.initialize_edges(graph)
        self.initialize_agents()

    def initialize_agents(self):
        for ag in self.agents:
            l = len(ag.path)
            for i in range(0,l-1):
                u = min(ag.path[i],ag.path[i + 1])
                v = max(ag.path[i],ag.path[i + 1])
                w,h = self.Edges[(u,v)]
                self.Edges[(u,v)] = (w,h+1)
                ag.edges_used[(u,v)] = True

        for ag in self.agents:
            l = len(ag.path)
            if l > 0 or ag.index == self.source:
                #if it's in the source it doesn't need a path
                ag.update_agent_cost(self.Edges)
        self.evaluate_totalcost()

    def create_graph(self,graph):
        G = nx.DiGraph()
        for i in range(graph.nodes):
            G.add_node(i)
        for u in range(graph.nodes):
            for v,w in graph.adj[u]:
                G.add_edge(u,v,weight = w)
        return G

    def initialize_edges(self,graph):
        Edges = {}
        for u in range(graph.nodes):
            for v,w in graph.adj[u]:
                i = min(u,v)
                j = max(u,v)
                Edges[(i,j)] = (w,0)
        return Edges

    def plot_graph(self):
        plt.ioff()
        self.fig = plt.figure(figsize = (6,5))
        label = '\n'.join(("Agents: " + str([ag.index for ag in self.agents]), "Source: " + str(self.source)))
        self.fig.canvas.set_window_title('Graph')
        self.fig.text(0.01,0.90, label)
        pos = nx.planar_layout(self.graphx)
        nx.draw(self.graphx,pos,with_labels = True)
        edge_labels = dict([((u,v,), f"{d['weight']:.2f}") for u,v,d in self.graphx.edges(data=True)])
        #edge_labels = nx.get_edge_attributes(self.graphx,'weight')
        nx.draw_networkx_edge_labels(self.graphx,pos,edge_labels = edge_labels)
        plt.show()

    def next_function(self,event):
        self.nash_eq = True
        for ag in self.agents:
            find = self.find_path(ag)
            if find == True:
                self.nash_eq = False
        for ag in self.agents:
            ag.update_agent_cost(self.Edges)
            ag.add_cost()
        self.evaluate_totalcost()
        self.cost_by_iteration.append(self.total_cost)

        plt.clf()
        self.plot_button()
        self.plot_paths()
        self.plot_total_cost()
        self.plot_costs()
        plt.draw()

    def plot_button(self):
        axnext = plt.axes([0.82, 0.01, 0.1, 0.065])
        message = "Nash Equilibrium" if self.nash_eq else "Next Step"
        self.bnext = Button(axnext, message)
        self.bnext.on_clicked(self.next_function)

    def plot_paths(self):
        fgraph = self.fig.add_subplot(self.gs[0:2,:])
        pos = nx.planar_layout(self.graphx)
        title = "Source: " + str(self.source) + ", Total cost: " + str(round(self.total_cost,2))
        fgraph.title.set_text(title)
        nx.draw(self.graphx,pos,with_labels = True)
        edge_labels = dict([((u,v,), f"{d['weight']:.2f}") for u,v,d in self.graphx.edges(data=True)])
        #edge_labels = nx.get_edge_attributes(self.graphx,'weight')
        nx.draw_networkx_edge_labels(self.graphx,pos,edge_labels = edge_labels)

        for ag in self.agents:
            nx.draw_networkx_edges(self.graphx, pos,edgelist = ag.get_path(),width=4,
            alpha=0.5, edge_color=ag.color, style='dashed',label = ag.index)

    def plot_total_cost(self):
        fmetrics = self.fig.add_subplot(self.gs[2,0])
        fmetrics.set_ylabel('Total cost')
        fmetrics.set_xlabel('Iterations')
        fmetrics.title.set_text("Total cost: " + str(round(self.total_cost,2)))
        fmetrics.plot(self.cost_by_iteration)

    def plot_costs(self):
        fagents = self.fig.add_subplot(self.gs[2,1])
        fagents.set_ylabel('Cost')
        fagents.set_xlabel('Iterations')
        fagents.title.set_text("Cost by agent")
        for ag in self.agents:
            label  = str(ag.index) + ": " +  str(round(ag.cost, 2))
            fagents.plot(ag.cost_by_iteration, color = ag.color, label = label)
            fagents.legend()

    def __call__(self):
        self.fig = plt.figure(figsize = (self.W,self.H))
        self.fig.canvas.set_window_title("BRD")
        self.gs = self.fig.add_gridspec(3, 2)
        self.cost_by_iteration.append(self.total_cost)
        for ag in self.agents:
            ag.add_cost()

        self.plot_button()
        self.plot_paths()
        self.plot_total_cost()
        self.plot_costs()

        plt.show()

    def update_edges(self,agent,change = True):
        l = len(agent.path)
        for i in range(0,l-1):
            u = min(agent.path[i],agent.path[i + 1])
            v = max(agent.path[i],agent.path[i + 1])

            w,h = self.Edges[(u,v)]
            if change == False:
                self.Edges[(u,v)] = (w,h-1)
                del agent.edges_used[(u,v)]
            else:
                self.Edges[(u,v)] = (w,h+1)
                agent.edges_used[(u,v)] = True

    def find_path(self,agent):
        index = agent.index
        prev_cost = agent.cost
        dist = [float("inf") for i in range(self.graph.nodes)]
        parent = [-1 for i in range(self.graph.nodes)]
        dist[self.source] = 0
        parent[self.source] = self.source
        PQ = queue.PriorityQueue()
        PQ.put((0,self.source))
        while PQ.empty() == False:
            w,u = PQ.get()
            if dist[u] < w:
                continue
            for v,c in self.graph.adj[u]:
                realcost = self.get_realcost(u,v,agent.contain_edge(u,v))
                if dist[v] > dist[u] + realcost:
                    parent[v] = u
                    dist[v] = dist[u] + realcost
                    PQ.put((dist[v],v))

        if dist[index] >= prev_cost:
            return False

        new_path = []
        self.create_path(index,parent,new_path)
        self.update_edges(agent,False)
        agent.path = new_path
        self.update_edges(agent,True)
        agent.cost = dist[index]
        return True

    def create_path(self,u,parent,new_path):
        if parent[u] == u:
            new_path.append(u)
            return
        new_path.append(u)
        self.create_path(parent[u],parent,new_path)

    def get_realcost(self,u,v,contained):
        i = min(u,v)
        j = max(u,v)
        w,h = self.Edges[(i,j)]
        if contained:
            return (w/h)
        else:
            return (w/(h+1))

    def evaluate_totalcost(self):
        ans = 0
        for ag in self.agents:
            ans += ag.cost
        self.total_cost = ans
