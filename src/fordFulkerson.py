import numpy as np
import graph
import sys

def main():

    # Le poids des arcs de ce graphe correspondent aux capacités
    g = example()
    # Le poids des arcs de ce graphe correspondent au flot
    flow = fordFulkerson(g, "s", "t")

    print(flow)
    
# Fonction créant un graphe sur lequel sera appliqué l'algorithme de Ford-Fulkerson
def example():
        
    g = graph.Graph(np.array(["s", "a", "b", "c", "d", "e", "t"]))

    g.addArc("s", "a", 8)
    g.addArc("s", "c", 4)
    g.addArc("s", "e", 6)
    g.addArc("a", "b", 10)
    g.addArc("a", "d", 4)
    g.addArc("b", "t", 8)
    g.addArc("c", "b", 2)
    g.addArc("d", "b", 2)
    g.addArc("c", "d", 1)
    g.addArc("d", "t", 6)
    g.addArc("e", "b", 4)
    g.addArc("e", "t", 2)
    
    return g

# Fonction appliquant l'algorithme de Ford-Fulkerson à un graphe
# Les noms des sommets sources est puits sont fournis en entrée
def fordFulkerson(g, sName, tName):
    
    """
    Marquage des sommets du graphe:
     - mark[i] est égal à +j si le sommet d'indice i peut être atteint en augmentant le flot sur l'arc ji
     - mark[i] est égal à  -j si le sommet d'indice i peut être atteint en diminuant le flot de l'arc ji
     - mark[i] est égal à sys.float_info.max si le sommet n'est pas marqué
    """
    # Récupérer l'indice de la source et du puits
    s = g.indexOf(sName)
    t = g.indexOf(tName)           
    # Créer un nouveau graphe contenant les même sommets que g
    flow = graph.Graph(g.nodes)
    # Récupérer tous les arcs du graphe 
    arcs = g.getArcs()
    edges = g.getEdges()     
    while True:
        mark = [sys.float_info.max] * g.n
        queue = []
        visited = [False] * g.n
        queue.append(s)
        # print("Restarting:",queue)
        while queue:
            idx = queue.pop(0)
            visited[idx] = True
            for arc in arcs:#Forward arests
                id1 = arc.id1
                id2 = arc.id2
                if(id1 != idx):#Current noued
                    continue
                if ((mark[id2] == sys.float_info.max) and
                    (flow.adjacency[id1][id2] < g.adjacency[id1][id2])):
                    mark[id2] = id1
                    queue.append(id2)
                    # print("Marking ",id1," to ",id2)
            
            for arc in arcs:#Backward arest
                id1 = arc.id1
                id2 = arc.id2
                if(id2 != idx):
                    continue

                if ((mark[id1] == sys.float_info.max) and
                    (flow.adjacency[id1][id2] > 0 )):#antecesor of s : adj[:][0] , next of s : adj[0][:]
                    mark[id1] = -id2
                    queue.append(id1)
                    # print("Marking -",id2," to ",id1)
            
        if mark[t] != sys.float_info.max:#Updating flow
            v = t
            bn = sys.float_info.max
            while v != s:
                u = abs(mark[v])
                if (mark[v] >= 0):
                    bn = min(bn, g.adjacency[u][v] - flow.adjacency[u][v])
                elif (mark[v] < 0 ):
                    bn = min(bn, flow.adjacency[v][u])

                v = u
            # print("Update flow:",bn)
            v = t
            while v != s:
                u = abs(mark[v])
                if (mark[v] >= 0):
                    flow.adjacency[u][v] += bn
                elif (mark[v] < 0):
                    flow.adjacency[v][u] -= bn
                v = u
        else:
            
            break
        
    return flow
   
if __name__ == '__main__':
    main()
