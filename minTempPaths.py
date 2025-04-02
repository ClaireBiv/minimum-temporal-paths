import networkx as _
import math
from sortedcollections import SortedList
from collections import deque

def earliestArrivalPath(G, edgeStream, x, t_alpha, t_omega):
    
    #Inizializza earliest-arrival time per ogni nodo 
    earliest_paths = [math.inf for _ in G.nodes]
    earliest_paths[x] = t_alpha

    for (u, v, t, w) in edgeStream:
        if (t + w) <= t_omega and t >= earliest_paths[u]:
            if (t + w) < earliest_paths[v]:
                earliest_paths[v] = t + w
        elif t >= t_omega:
            break
    
    return earliest_paths

def fastestPathList(G, edgeStream, x, t_alpha, t_omega):

    #Inizializza liste ordinate e fastest path duration per ogni nodo 
    L = [SortedList(key=lambda x: x[1]) for _ in G.nodes]
    fastest_paths = [math.inf for _ in G.nodes]
    fastest_paths[x] = 0

    for (u, v, t, w) in edgeStream:
        if t >= t_alpha and (t + w) <= t_omega:
            
            if u == x:
                if (t,t) not in L[x]:
                   #Inserisce la coppia (t,t)
                   L[x].add((t,t))
            
            #Cerca la coppia in S[u] con a_u massimo minore di t
            i_u = L[u].bisect_key_right(t) - 1

            if i_u >= 0:
                #Crea la coppia per S[v]
                (s_u, a_u) = L[u][i_u]
                (s_v, a_v) = (s_u, t + w)

                #Inserisce o aggiorna la coppia in S[v] (controlla che non sia dominata)
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
                
                #Rimuove elementi dominati
                for _ in range(i_v+1, len(L[v])):
                    if L[v][i_v][0] >= L[v][i_v+1][0]:
                        L[v].pop(i_v+1)
                    else:
                        break

                #Aggiorna le fastest path duration
                if (a_v - s_v) < fastest_paths[v]:
                    fastest_paths[v] = a_v - s_v

        elif t >= t_omega:
            break

    return fastest_paths

def fastestPathQueue(G, edgeStream, x, t_alpha, t_omega):

    #Inizializza liste e fastest path duration per ogni nodo 
    Q = [deque() for _ in G.nodes]
    fastest_paths = [math.inf for _ in G.nodes]
    fastest_paths[x] = 0

    for (u, v, t, w) in edgeStream:
        if t >= t_alpha and (t + w) <= t_omega:
            
            if u == x:
                if (t,t) not in Q[x]:
                   #Inserisce la coppia (t,t)
                   Q[x].append((t,t))

            #Cerca la coppia in Q[u] con a_u massimo minore di t

            if Q[u] and Q[u][0][1] <= t:
                for _ in range(len(Q[u])-1):
                    if Q[u][1][1] <= t:
                        Q[u].popleft()
                    else:
                        break

                #Crea la coppia per Q[v]
                (s_u, a_u) = Q[u][0]
                (s_v, a_v) = (s_u, t + w)

                #Inserisce la coppia in Q[v] se non è dominata
                if Q[v]:
                    (s_vi, a_vi) = Q[v][-1]
                    if s_vi < s_v:
                        if a_vi == a_v:
                            Q[v].pop()
                        Q[v].append((s_v,a_v))
                else:
                    Q[v].append((s_v,a_v))
                
                #Aggiorna le fastest path duration
                if (a_v - s_v) < fastest_paths[v]:
                    fastest_paths[v] = a_v - s_v
        elif t >= t_omega:
            break

    return fastest_paths