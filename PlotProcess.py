import matplotlib.pyplot as plt
import networkx as nx



class PlotProcess:


    def __init__(self,environment,W,H):
        self.G = self.create_graph(environment)
        self.fig = plt.figure(figsize = (W,H))
        self.fig = plt.gcf()


    def create_graph(self,environment):
        G = nx.DiGraph()
        for i in range(environment.nodes):
            G.add_node(i)
        for u in range(environment.nodes):
            for v,w in environment.adj[u]:
                G.add_edge(u,v,weight = w)
        return G

    def draw_plot(self,agent_list,target,total_cost,block = False, sleep = 2,title = "Nash Equilibrium"):
        self.fig.canvas.set_window_title(title)


        number_of_agents = len(agent_list)
        ## original
        pos = nx.planar_layout(self.G)
        g = self.fig.add_subplot(3,3,1)
        g.title.set_text("Target: " + str(target) + ", Total cost: "+ str(total_cost))
        nx.draw(self.G,pos,with_labels = True)
        labels = nx.get_edge_attributes(self.G,'weight')
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels = labels)

        for i,ag in zip(range(2,2 + number_of_agents),agent_list):
            Gi = self.G
            posi = nx.planar_layout(Gi)
            gi = self.fig.add_subplot(3,3,i)
            title = "Agent Index: " + str(ag.get_index()) + ", Cost: " + str(ag.get_cost())
            gi.title.set_text(title)
            nx.draw(Gi,posi,with_labels=True)
            labeli = nx.get_edge_attributes(Gi,'weight')
            nx.draw_networkx_edge_labels(Gi,posi,edge_labels = labeli)
            nx.draw_networkx_edges(Gi, posi,edgelist = ag.get_path(),width=6, alpha=0.5, edge_color='r', style='dashed')


        plt.show(block)
        if block == False:
            plt.pause(sleep)
            plt.clf()
