import matplotlib.pyplot as plt
import networkx as nx

class PlotProcess:

    def __init__(self,graph,number_of_agents):
        self.G = self.create_graph(graph)
        self.W,self.H,self.r,self.c = self.choose_figsize(number_of_agents)

    def plot_graph(self,agents,source):
        plt.ioff()
        self.fig = plt.figure(figsize = (6,5))
        label = '\n'.join(("Agents: " + str(agents), "Source: " + str(source)))
        self.fig.canvas.set_window_title('Graph')
        self.fig.text(0.01,0.90, label)
        pos = nx.planar_layout(self.G)
        nx.draw(self.G,pos,with_labels = True)
        labels = nx.get_edge_attributes(self.G,'weight')
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels = labels)
        plt.show()

    def choose_figsize(self,number_of_agents):
        if number_of_agents == 1:
            return 8,4,1,2
        elif number_of_agents == 2:
            return 12,4,1,3
        elif number_of_agents == 3:
            return 4,4,2,2
        elif number_of_agents <= 5:
            return 12,8,2,3
        else:
            return 12,8,3,3

    def create_graph(self,graph):
        G = nx.DiGraph()
        for i in range(graph.nodes):
            G.add_node(i)
        for u in range(graph.nodes):
            for v,w in graph.adj[u]:
                G.add_edge(u,v,weight = w)
        return G

    def set_plot(self):
        self.fig = plt.figure(figsize = (self.W,self.H))

    def plot_metrics(self,agent_list,source,costs):
        plt.ioff()
        self.set_plot()
        self.fig.canvas.set_window_title('Costs by iteration')
        number_of_agents = len(agent_list)
        # plot system cost
        g = self.fig.add_subplot(self.r,self.c,1)
        g.set_ylabel('Cost')
        g.title.set_text("Source: " + str(source) + ", Total cost: "+ str(costs[-1]))
        plt.plot(costs)

        #plot agents costs
        for i,ag in zip(range(2,2 + number_of_agents),agent_list):
            gi = self.fig.add_subplot(self.r,self.c,i)
            gi.set_ylabel('Cost')
            title = "Agent Index: " + str(ag.get_index()) + ", Cost: " + str(ag.get_cost())
            gi.title.set_text(title)
            plt.plot(ag.cost_by_iteration)

        plt.show()

    def draw_plot(self,agent_list,source,total_cost,block = False, sleep = 2,title = "Nash Equilibrium"):
        if block == True:
            self.set_plot()
            plt.ioff()
        else:
            plt.ion()

        self.fig.canvas.set_window_title(title)
        number_of_agents = len(agent_list)
        # plot original
        pos = nx.planar_layout(self.G)
        g = self.fig.add_subplot(self.r,self.c,1)
        g.title.set_text("Source: " + str(source) + ", Total cost: "+ str(total_cost))
        nx.draw(self.G,pos,with_labels = True)
        labels = nx.get_edge_attributes(self.G,'weight')
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels = labels)

        #plot agents
        for i,ag in zip(range(2,2 + number_of_agents),agent_list):
            Gi = self.G
            posi = nx.planar_layout(Gi)
            gi = self.fig.add_subplot(self.r,self.c,i)
            title = "Agent Index: " + str(ag.get_index()) + ", Cost: " + str(ag.get_cost())
            gi.title.set_text(title)
            nx.draw(Gi,posi,with_labels=True)
            labeli = nx.get_edge_attributes(Gi,'weight')
            nx.draw_networkx_edge_labels(Gi,posi,edge_labels = labeli)
            nx.draw_networkx_edges(Gi, posi,edgelist = ag.get_path(),width=6, alpha=0.5, edge_color='r', style='dashed')

        plt.show()
        if block == False:
            plt.pause(sleep)
            plt.clf()
