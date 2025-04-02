import networkx as _
import math

# One-Pass Algorithm for computing single-source earliest-arrival paths
def earliestArrivalPath(G, edgeStream, x, t_alpha, t_omega):
    
    # Init earliest-arrival time for each node
    earliest_paths = [math.inf for _ in G.nodes]
    earliest_paths[x] = t_alpha

    # Computing earliest-arrival time for each node
    for (u, v, t, w) in edgeStream:
        if (t + w) <= t_omega and t >= earliest_paths[u]:
            # Update earliest-arrival time
            if (t + w) < earliest_paths[v]:
                earliest_paths[v] = t + w
        elif t >= t_omega:
            break
    
    return earliest_paths
