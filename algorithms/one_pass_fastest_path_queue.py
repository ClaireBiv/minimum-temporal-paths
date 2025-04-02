import networkx as _
import math
from collections import deque

# One-Pass Algorithm for computing single-source fastest paths with queue
def fastestPathQueue(G, edgeStream, x, t_alpha, t_omega):

    # Init queue and fastest path duration for each node
    Q = [deque() for _ in G.nodes]
    fastest_paths = [math.inf for _ in G.nodes]
    fastest_paths[x] = 0
    
    # Computing fastest path duration for each node
    for (u, v, t, w) in edgeStream:
        if t >= t_alpha and (t + w) <= t_omega:
            
            if u == x:
                if (t,t) not in Q[x]:
                   Q[x].append((t,t))

            if Q[u] and Q[u][0][1] <= t:
                # Search element
                for _ in range(len(Q[u])-1):
                    if Q[u][1][1] <= t:
                        Q[u].popleft()
                    else:
                        break
                        
                # Create element
                (s_u, a_u) = Q[u][0]
                (s_v, a_v) = (s_u, t + w)

                # Append element in queue if not dominated
                if Q[v]:
                    (s_vi, a_vi) = Q[v][-1]
                    if s_vi < s_v:
                        if a_vi == a_v:
                            Q[v].pop()
                        Q[v].append((s_v,a_v))
                else:
                    Q[v].append((s_v,a_v))
                
                # Update fastest path duration
                if (a_v - s_v) < fastest_paths[v]:
                    fastest_paths[v] = a_v - s_v
        elif t >= t_omega:
            break

    return fastest_paths
