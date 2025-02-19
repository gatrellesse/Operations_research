import numpy as np
import graph
import sys

def main():
    
    # Créer un graphe contenant les sommets a, b, c, d, e, f, g 
    g = graph.Graph(np.array(["a", "b", "c", "d", "e", "f", "g"]))

    # Ajouter les arêtes
    g.addEdge("a", "b",  1.0)
    g.addEdge("a", "c",  8.0)
    g.addEdge("b", "c",  2.0)
    g.addEdge("b", "d",  5.0)
    g.addEdge("b", "e",  7.0)
    g.addEdge("b", "f",  9.0)
    g.addEdge("c", "d",  4.0)
    g.addEdge("d", "e",  6.0)
    g.addEdge("d", "g", 12.0)
    g.addEdge("e", "f",  8.0)
    g.addEdge("e", "g", 11.0)
    g.addEdge("f", "g", 10.0)
    
    # Obtenir un arbre couvrant de poids minimal du graphe
    tree = kruskalCC(g)
    #tree = kruskal(g, True)
    
    # S'il existe un tel arbre (i.e., si le graphe est connexe)
    if tree != None: 
        # L'afficher
        print(tree)
    
    else:
        print("Pas d'arbre couvrant")
    tests()

def tests():
    g1 = graph.Graph(np.array(["a", "b", "c", "d", "e", "f", "g", "h"]))

    g1.addEdge("a", "b", 9)
    g1.addEdge("a", "f", 6)
    g1.addEdge("a", "g", 9)
    g1.addEdge("b", "c", 8)
    g1.addEdge("b", "e", 5)
    g1.addEdge("c", "d", 2)
    g1.addEdge("c", "e", 5)
    g1.addEdge("d", "h", 7)
    g1.addEdge("e", "f", 1)
    g1.addEdge("e", "g", 5)
    g1.addEdge("e", "h", 8)
    g1.addEdge("g", "h", 9)

    g2 = graph.Graph(np.array(["A", "B", "C", "D", "E", "F"]))

    g2.addEdge("A", "B", 4)
    g2.addEdge("A", "C", 3)
    g2.addEdge("B", "F", 5)
    g2.addEdge("C", "D", 2)
    g2.addEdge("C", "F", 5)
    g2.addEdge("D", "E", 4)
    g2.addEdge("E", "F", 3)

    # Obtenir un arbre couvrant de poids minimal du graphe
    tree1_min = kruskal(g1, True)
    tree1_max = kruskal(g1, False)
    tree2_min = kruskal(g2, True)
    tree2_max = kruskal(g2, False)
    
    # S'il existe un tel arbre (i.e., si le graphe est connexe)
    if tree1_min != None: 
        # L'afficher
        print(tree1_min)
    else:
        print("Pas d'arbre couvrant")
    if tree1_max != None: 
        # L'afficher
        print(tree1_max)
    else:
        print("Pas d'arbre couvrant")
    if tree2_min != None: 
        # L'afficher
        print(tree2_min)
    else:
        print("Pas d'arbre couvrant")
    if tree2_max != None: 
        # L'afficher
        print(tree2_max)
    else:
        print("Pas d'arbre couvrant")

# Applique l'algorithme de Kruskal pour trouver un arbre couvrant de poids minimal d'un graphe
# Retourne: Un arbre couvrant de poids minimal du graphe ou None s'il n'en existe pas
def kruskal(g, computeMin: bool):
    # Créer un nouveau graphe contenant les mêmes sommets que g
    tree = graph.Graph(g.nodes)
    # Nombre d'arêtes dans l'arbre
    addedEdges = 0
    # Récupérer toutes les arêtes de g
    edges = g.getEdges()
    # Trier les arêtes par poids croissant si computMin true else decroi.
    if computeMin:edges.sort(key=lambda x: x.weight)
    else : edges.sort(key=lambda x: x.weight, reverse=True)
    addedEdges = 0
    idx = 0
    # Ajouter des arêtes jusqu'à obtenir un arbre couvrant (n-1 arêtes)
    while addedEdges < g.n - 1 and idx < len(edges):
        edge = edges[idx]
        if not tree.createACycle(edge):  # Vérifier si l'ajout de l'arête crée un cycle
            tree.addCopyOfEdge(edge)  # Ajouter l'arête
            addedEdges += 1
        idx += 1

    return tree

def kruskalCC(g):
        # Créer un nouveau graphe contenant les mêmes sommets que g
    tree = graph.Graph(g.nodes)
    # Nombre d'arêtes dans l'arbre
    addedEdges = 0
    # Récupérer toutes les arêtes de g
    edges = g.getEdges()
    # Trier les arêtes par poids croissant si computMin true else decroi.
    edges.sort(key=lambda x: x.weight)
    
    addedEdges = 0
    idx = 0
    component = []
    rank = []
    for node in edges:
        if node.id1 not in component:
            component.append(node.id1)
            rank.append(0)
        if node.id2 not in component:
            component.append(node.id2)
            rank.append(0)

    # Ajouter des arêtes jusqu'à obtenir un arbre couvrant (n-1 arêtes)
    while addedEdges < g.n - 1 and idx < len(edges):
        edge = edges[idx]
        x = find(component, edge.id1)
        y = find(component, edge.id2)
        if x != y:
            addedEdges += 1 
            tree.addCopyOfEdge(edge)  # Ajouter l'arête
            apply_union(component, rank, x, y)
        idx += 1
    
    return tree

def find(component, i):
    if component[i] == i:
        return i
    return find(component, component[i])
def apply_union(component, rank, x, y):
    xroot = find(component, x)
    yroot = find(component, y)
    if rank[xroot] < rank[yroot]:
        component[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        component[yroot] = xroot
    else:
        component[yroot] = xroot
        rank[xroot] += 1

if __name__ == '__main__':
    main()

