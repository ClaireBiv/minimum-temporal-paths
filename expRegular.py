import math
import concurrent.futures
import randomGraphs as rg
import minTempPaths as mtp
import networkx as nx

def expEAP(n,d):
    #Genera grafo random connesso
    G = rg.regular_randTempGraph(n,d)
    while not nx.is_connected(G):
        G = rg.regular_randTempGraph(n,d)
    '''
    pos = nx.kamada_kawai_layout(G)
    labels = nx.get_edge_attributes(G,'t')
    nx.draw_networkx(G,pos)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.show()
    ''' 
    t_alpha, t_omega = 1, len(list(G.edges))+1

    #Assunzione grafo non diretto reso diretto con doppi archi
    edgeStream = sorted([(e[0], e[1], e[2]['t'], e[2]['w']) for e in G.edges(data=True)]+ 
                        [(e[1], e[0], e[2]['t'], e[2]['w']) for e in G.edges(data=True)],
                        key = lambda x: x[2])
    
    minPaths, ecc_x = [], []
    maxPath = -1
    sumDist = 0
    
    #Suppongo i threadpool eseguano l'algoritmo eap contemporaneamente su diversi nodi sorgente
    with concurrent.futures.ThreadPoolExecutor(max_workers = len(list(G.nodes()))) as pool:
        futures = [pool.submit(mtp.earliestArrivalPath, G, edgeStream, x, t_alpha, t_omega) for x in G.nodes]
    for future in concurrent.futures.as_completed(futures):
        #Di tutte le istanze terminate, prende il risultato ed estrae il eat massimo (per calcolare il diametro?)
        minPaths = future.result()
        maxPath = max(minPaths)
        #Se il diametro è inf, il grafo non è temporalmente connesso, cancella le chiamate
        if (maxPath == math.inf):
            for future in futures:
                future.cancel()
            return (-1, -1)
        else:
            ecc_x.append(maxPath)
            sumDist += sum(minPaths)
    diametro = max(ecc_x)
    return diametro, sumDist

def expFP(n,d):
    G = rg.regular_randTempGraph(n,d)
    while not nx.is_connected(G):
        G = rg.regular_randTempGraph(n,d)

    t_alpha, t_omega = 1, len(list(G.edges))+1
    edgeStream = sorted([(e[0], e[1], e[2]['t'], e[2]['w']) for e in G.edges(data=True)]+ 
                        [(e[1], e[0], e[2]['t'], e[2]['w']) for e in G.edges(data=True)],
                        key = lambda x: x[2])
    minPaths, ecc_x = [], []
    maxPath = -1
    sumDist = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers = len(list(G.nodes()))) as pool:
        futures = [pool.submit(mtp.fastestPathQueue, G, edgeStream, x, t_alpha, t_omega) for x in G.nodes]
    for future in concurrent.futures.as_completed(futures):
        minPaths = future.result()
        maxPath = max(minPaths)
        if (maxPath == math.inf):
            for future in futures:
                future.cancel()
            return (-1, -1)
        else:
            ecc_x.append(maxPath)
            sumDist += sum(minPaths)
    diametro = max(ecc_x)
    return (diametro, sumDist)

"""
if __name__ == "__main__":
    d_p = {
        100: 12, 200: 14, 300: 15, 400: 16, 500: 17,
        600: 17, 700: 18, 800: 18, 900: 18, 1000: 19
    }
    test = 10
    diametro, avgDiam, diametri = 0, 0, []
    sumDist, avgDist, distanze = 0, 0, []
    for n in range(100,1001,100):
        for i in range(0,8):
            d = d_p[n] + i
            currTest = 1
            while(currTest <= test):
                diametro, sumDist = expMTP(n,d)
                if (diametro, sumDist) != (-1, -1):
                    diametri.append(diametro)
                    distanze.append(sumDist/(n*(n-1)))
                    currTest += 1
            avgDiam = sum(diametri)/test
            avgDist = sum(distanze)/test
            diametri, distanze = [], []
            with open(f"EAP_Regular/output{n}_{k}.txt", "w") as file:
                file.write(f"Sono stati generati {test} grafi con n = {n} e p = {k}*log(n)/n = {p}\nDiametro medio = {avgDiam}\nDistanza media = {avgDist}")"""

if __name__ == "__main__":
    d_p = {
        100: 12, 200: 14, 300: 15, 400: 16, 500: 17,
        600: 17, 700: 18, 800: 18, 900: 18, 1000: 19
    }
    test = 10
    diametro, avgDiam, diametri = 0, 0, []
    sumDist, avgDist, distanze = 0, 0, []

    for k in range(0,8):
        for n in range(100,1001,100):
            d = d_p[n] + k
            print(n, k)
            currTest = 1
            while(currTest <= test):
                diametro, sumDist = expEAP(n,d)
                if (diametro, sumDist) != (-1, -1):
                    diametri.append(diametro)
                    distanze.append(sumDist/(n*(n-1)))
                    currTest += 1
            avgDiam = sum(diametri)/test
            avgDist = sum(distanze)/test
            diametri, distanze = [], []
            with open(f"EAP_Regular/output{n}_{k}.txt", "w") as file:
                file.write(f"Sono stati generati {test} grafi con n = {n} e d = d_p[n] + {k} = {d}\nDiametro medio = {avgDiam}\nDistanza media = {avgDist}")
            
            currTest = 1
            while(currTest <= test):
                diametro, sumDist = expFP(n,d)
                if (diametro, sumDist) != (-1, -1):
                    diametri.append(diametro)
                    distanze.append(sumDist/(n*(n-1)))
                    currTest += 1
            avgDiam = sum(diametri)/test
            avgDist = sum(distanze)/test
            diametri, distanze = [], []
            with open(f"FP_Regular/output{n}_{k}.txt", "w") as file:
                file.write(f"Sono stati generati {test} grafi con n = {n} e d = d_p[n] + {k} = {d}\nDiametro medio = {avgDiam}\nDistanza media = {avgDist}")
                