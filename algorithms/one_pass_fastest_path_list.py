import networkx as _
import math
from sortedcollections import SortedList

# One-Pass Algorithm for computing single-source fastest paths with sorted lists
def fastestPathList(G, edgeStream, x, t_alpha, t_omega):

    # Init sorted list and fastest path duration for each node 
    L = [SortedList(key=lambda x: x[1]) for _ in G.nodes]
    fastest_paths = [math.inf for _ in G.nodes]
    fastest_paths[x] = 0

    # Computing fastest path duration for each node
    for (u, v, t, w) in edgeStream:
        if t >= t_alpha and (t + w) <= t_omega:
            
            if u == x:
                if (t,t) not in L[x]:
                   L[x].add((t,t))

            # Search element
            i_u = L[u].bisect_key_right(t) - 1
            if i_u >= 0:
                # Create element
                (s_u, a_u) = L[u][i_u]
                (s_v, a_v) = (s_u, t + w)

                # Insert element in sorted list if not dominated
                present = False
                for i, (s,a) in enumerate(L[v]):
                    if s == s_v:
                        if a > a_v:
                            L[v].pop(i)
                        else:
                            present = True
                        break
                if not present:
                    i_v = L[v].bisect((s_v, a_v))
                    if i_v == 0 or s_v > L[v][i_v-1][0]:
                        L[v].add((s_v, a_v))
                
                # Remove dominated elements
                for _ in range(i_v+1, len(L[v])):
                    if L[v][i_v][0] >= L[v][i_v+1][0]:
                        L[v].pop(i_v+1)
                    else:
                        break

                # Update fastest path duration
                if (a_v - s_v) < fastest_paths[v]:
                    fastest_paths[v] = a_v - s_v
        elif t >= t_omega:
            break

    return fastest_paths
