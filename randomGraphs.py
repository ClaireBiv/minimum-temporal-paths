import networkx as nx
import random

def assignLabels(G):
    labels = [i for i in range(1, len(list(G.edges))+1)]
    random.shuffle(labels)

    for (u,v) in G.edges:
        G.edges[u,v]['time'] = labels.pop()
        G.edges[u,v]['weight'] = 1

def er_randTempGraph(n,p):
    G = nx.gnp_random_graph(n,p)
    assignLabels(G)
    return G

def regular_randTempGraph(n,d):
    G = nx.random_regular_graph(d,n)
    assignLabels(G)
    return G