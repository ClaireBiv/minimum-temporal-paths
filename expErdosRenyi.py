import math
import concurrent.futures
import randomGraphs as rg
import minTempPaths as mtp
import networkx as nx

def expEAP(n,p):
    #Genera grafo random connesso
    G = rg.er_randTempGraph(n,p)
    while not nx.is_connected(G):
        G = rg.er_randTempGraph(n,p)

    t_alpha, t_omega = 1, len(list(G.edges))+1

    #Assunzione grafo non diretto reso diretto con doppi archi
    edgeStream = sorted([(e[0], e[1], e[2]['time'], e[2]['weight']) for e in G.edges(data=True)]+ 
                        [(e[1], e[0], e[2]['time'], e[2]['weight']) for e in G.edges(data=True)],
                        key = lambda x: x[2])
    
    minPaths, ecc_x = [], []
    maxPath, sumDist = -1, 0
    
    #Suppongo i threadpool eseguano l'algoritmo eap contemporaneamente su diversi nodi sorgente
    with concurrent.futures.ThreadPoolExecutor(max_workers = len(list(G.nodes()))) as pool:
        futures = [pool.submit(mtp.earliestArrivalPath, G, edgeStream, x, t_alpha, t_omega) for x in G.nodes]
    for future in concurrent.futures.as_completed(futures):
        #Di tutte le istanze terminate, prende il risultato ed estrae il minPath massimo
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

def expFP(n,p):
    G = rg.er_randTempGraph(n,p)
    while not nx.is_connected(G):
        G = rg.er_randTempGraph(n,p)

    t_alpha, t_omega = 1, len(list(G.edges))+1
    edgeStream = sorted([(e[0], e[1], e[2]['time'], e[2]['weight']) for e in G.edges(data=True)]+ 
                        [(e[1], e[0], e[2]['time'], e[2]['weight']) for e in G.edges(data=True)],
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

if __name__ == "__main__":
    test = 10
    diametro, avgDiam, diametri = 0, 0, []
    sumDist, avgDist, distanze = 0, 0, []
    for n in range(100,1001,100):
        for i in range(3,11):
            p = i*(math.log(n))/n
            currTest = 1
            while(currTest <= test):
                diametro, sumDist = expEAP(n,p)
                if (diametro, sumDist) != (-1, -1):
                    diametri.append(diametro)
                    distanze.append(sumDist/(n*(n-1)))
                    currTest += 1
            avgDiam = sum(diametri)/test
            avgDist = sum(distanze)/test
            diametri, distanze = [], []
            with open(f"EAP_ErdosRenyi/output{n}_{i}.txt", "w") as file:
                file.write(f"Sono stati generati {test} grafi con n = {n} e p = {i}*log(n)/n = {p}\nDiametro medio = {avgDiam}\nDistanza media = {avgDist}")