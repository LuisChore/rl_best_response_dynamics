import matplotlib.pyplot as plt
from Agent import Agent
from Graph import Graph
from PlotProcess import PlotProcess
import queue
import time

class BRD:

    def __init__(self,environment,agents,target):
        self.agents = [ Agent(a) for a in agents]
        self.target = target
        self.environment = environment
        self.plotProcess = PlotProcess(environment,len(agents))
        self.total_cost = float("inf")
        self.plotProcess.draw_plot([],self.target,self.total_cost,title = "Original")
        self.Edges = self.initialize_edges(environment)
        #dictionary to know how many agents are using every edge



    def initialize_edges(self,environment):
        Edges = {}
        for u in range(environment.nodes):
            for v,w in environment.adj[u]:
                i = min(u,v)
                j = max(u,v)
                Edges[(i,j)] = (w,0)
        return Edges


    def process(self):
        found = True
        it = 1
        while found == True:
            found = False
            for u in self.agents:
                ok = self.find_path(u)
                if ok == True:
                    found = True
            self.evaluate_total_cost()
            title = "Iteration: " + str(it)
            self.plotProcess.draw_plot(self.agents,self.target,self.total_cost,title = title)
            it+=1
        for u in self.agents:
            print(u)
        print("Total cost: " + str(self.total_cost))


    def update_edges(self,agent,change):
        l = len(agent.path)
        for i in range(0,l-1):
            u = min(agent.path[i],agent.path[i + 1])
            v = max(agent.path[i],agent.path[i + 1])

            w,h = self.Edges[(u,v)]
            if change == -1:
                self.Edges[(u,v)] = (w,h-1)
                del agent.edges_used[(u,v)]
            else:
                self.Edges[(u,v)] = (w,h+1)
                agent.edges_used[(u,v)] = True

    def find_path(self,agent):
        index = agent.index
        prev_cost = agent.cost
        dist = [float("inf") for i in range(self.environment.nodes)]
        parent = [-1 for i in range(self.environment.nodes)]
        dist[self.target] = 0
        parent[self.target] = self.target
        PQ = queue.PriorityQueue()
        PQ.put((0,self.target))
        while PQ.empty() == False:
            w,u = PQ.get()
            if dist[u] < w:
                continue
            for v,c in self.environment.adj[u]:
                real_c = self.get_real_cost(u,v,agent.contain_edge(u,v))
                if dist[v] > dist[u] + real_c:
                    parent[v] = u
                    dist[v] = dist[u] + real_c
                    PQ.put((dist[v],v))

        if dist[index] >= prev_cost:
            return False
        new_path = []
        self.create_path(index,parent,new_path)
        self.update_edges(agent,-1)
        agent.path = new_path
        self.update_edges(agent,1)
        agent.cost = dist[index]
        return True


    def create_path(self,u,parent,new_path):
        if parent[u] == u:
            new_path.append(u)
            return
        new_path.append(u)
        self.create_path(parent[u],parent,new_path)

    def get_real_cost(self,u,v,contained):
        i = min(u,v)
        j = max(u,v)
        w,h = self.Edges[(i,j)]
        if contained:
            return (w/h)
        else:
            return (w/(h+1))

    def evaluate_total_cost(self):
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
    target = int(f.readline())
    brd = BRD(g,agent_list,target)
    brd.process()
    brd.plotProcess.draw_plot(brd.agents,brd.target,brd.total_cost,block = True)



if __name__ == "__main__":
    main()
