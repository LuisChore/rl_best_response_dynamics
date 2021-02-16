import matplotlib.pyplot as plt
from Agent import Agent
from Graph import Graph
from PlotProcess import PlotProcess
import queue
import time

class BRD:

    def __init__(self,graph,agents,source):
        self.agents = [ Agent(a) for a in agents]
        self.source = source
        self.graph = graph
        self.plotProcess = PlotProcess(graph,len(agents))
        self.total_cost = float("inf")
        self.plotProcess.draw_plot([],self.source,self.total_cost,title = "Original")
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
        find_better_path = True
        it = 1
        while find_better_path == True:
            find_better_path = False
            for u in self.agents:
                find = self.find_path(u)
                if find == True:
                    find_better_path = True
            self.evaluate_totalcost()
            title = "Iteration: " + str(it)
            self.plotProcess.draw_plot(self.agents,self.source,self.total_cost,title = title)
            it+=1
        for u in self.agents:
            print(u)
        print("Total cost: " + str(self.total_cost))

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

def main():
    f = open("example.txt", "r")
    nodes,edges = f.readline().split()
    g = Graph(int(nodes),True)
    for i in range(int(edges)):
        u,v,w = f.readline().split()
        g.add_edge(int(u),int(v),int(w))
    agent_list = [int(x) for x in f.readline().split()]
    source = int(f.readline())
    brd = BRD(g,agent_list,source)
    brd()
    brd.plotProcess.draw_plot(brd.agents,brd.source,brd.total_cost,block = True)

if __name__ == "__main__":
    main()
