import matplotlib.pyplot as plt
from Agent import Agent
from Graph import Graph
from PlotProcess import PlotProcess
import queue
import time

class BRD:

    def __init__(self,graph,agents,source):
        self.agents = [ Agent(a) for a in agents]
        self.cost_by_iteration = []
        self.graph = graph
        self.plotProcess = PlotProcess(graph,len(agents))
        self.total_cost = float("inf")
        self.source = source
        self.Edges = self.initialize_edges(graph)
        #dictionary to know how many agents are using every edge

    def initialize_edges(self,graph):
        Edges = {}
        for u in range(graph.nodes):
            for v,w in graph.adj[u]:
                i = min(u,v)
                j = max(u,v)
                Edges[(i,j)] = (w,0)
        return Edges

    def __call__(self):
        self.plotProcess.set_plot()
        find_better_path = True
        self.plotProcess.draw_plot([],self.source,self.total_cost,title = "Original")
        it = 1
        while find_better_path == True:
            find_better_path = False
            for u in self.agents:
                find = self.find_path(u)
                u.add_cost()
                if find == True:
                    find_better_path = True
            if find == False:
                break
            for u in self.agents:
                u.update_agent_cost(self.Edges)
            self.evaluate_totalcost()
            self.cost_by_iteration.append(self.total_cost);
            title = "Iteration: " + str(it)
            self.plotProcess.draw_plot(self.agents,self.source,self.total_cost,title = title)
            it+=1

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
        for key in self.Edges:
            w,h = self.Edges[key]
            if h > 0:
                ans += w
        self.total_cost = ans
        return ans

    def plot_metrics(self):
        self.plotProcess.plot_metrics(self.agents,self.source,self.cost_by_iteration)

    def plot_status(self):
        self.plotProcess.draw_plot(self.agents,self.source,self.total_cost,block = True)
