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
    mark = [sys.float_info.max] * g.n
    
    # Récupérer l'indice de la source et du puits
    s = g.indexOf(sName)
    t = g.indexOf(tName)           
    # Créer un nouveau graphe contenant les même sommets que g
     # Ajouter l'arête
    flow = graph.Graph(g.nodes)
    # Récupérer tous les arcs du graphe 
    arcs = g.getArcs()
    #tree.addCopyOfEdge(edge) 
    edges = g.getEdges()     
    
    maxFlow = False
    
    while not maxFlow:
        mark = [sys.float_info.max] * g.n
        mark[s] = s
        prev_idx = s
        idx = s
        queue = []
        visited = [False] * g.n
        queue.append(s)
        while queue:
            for arc in arcs:#analysing all edges of vertice
                id1 = arc.id1
                id2 = arc.id2
                if(id1 != idx):
                    continue
                #Verify if the arcs exists
                if (g.adjacency[id1][id2] == 0):
                    continue
                #print("Current flow: ",flow.adjacency[id1][id2] , " Max flow",g.adjacency[id1][id2] )
                #print(flow.adjacency)
                if ((mark[id1] != sys.float_info.max) and
                    (mark[id2] == sys.float_info.max) and
                    (flow.adjacency[id1][id2] < g.adjacency[id1][id2])):
                    mark[id2] = id1
                    idx = id2
                    queue.append(idx)
                    print("Marking ",id1," to ",id2)
                    
                elif ((mark[id1] == sys.float_info.max) and
                    (mark[id2] != sys.float_info.max) and
                    (flow.adjacency[id1][id2] != 0 )):
                    mark[id1] = -id2
                    idx = id1
                    queue.append(idx)
                    print("Marking -",id2," to ",id1)
                
            if mark[t] != sys.float_info.max:
                break
            else:
                visited[idx] = True
                print(visited)
                #print(visited)
                idx = queue.pop(0)
                print("Checking for ", idx)
                
            
        #print(mark)
        if mark[t] != sys.float_info.max:
            print("Updating flow")
            goodWay = []
            for i in range(1, g.n):
                if mark[i] >= 0 and mark[i] != sys.float_info.max:
                    goodWay.append(g.adjacency[mark[i]][i] - flow.adjacency[mark[i]][i])
            if(not goodWay):
                goodWay = 0
            else: goodWay = min(goodWay)
            
            badWay = []
            for i in range(1, g.n):
                if mark[i] < 0:
                    badWay.append(g.adjacency[i][abs(mark[i])] - flow.adjacency[i][abs(mark[i])])
            if(not badWay):
                badWay = goodWay
            else: badWay = min(badWay)
            newFlow = min(badWay, goodWay)
            print("Augmentation flow: ", newFlow,"\n")
            for i in range(1, g.n):
                if(mark[i] < 0):
                    flow.adjacency[abs(mark[i])][i] -= newFlow
                if(mark[i] >= 0 and mark[i] != sys.float_info.max):
                    flow.adjacency[mark[i]][i] +=  newFlow
        else: break
        
    return flow
   
if __name__ == '__main__':
    main()
