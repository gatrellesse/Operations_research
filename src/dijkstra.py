import graph
import sys

def main():
    cities = []
    cities.append("Paris")
    cities.append("Hambourg")
    cities.append("Londres")
    cities.append("Amsterdam")
    cities.append("Edimbourg")
    cities.append("Berlin")
    cities.append("Stockholm")
    cities.append("Rana")
    cities.append("Oslo")

    g = graph.Graph(cities)
    
    g.addArc("Paris", "Hambourg", 7)
    g.addArc("Paris",  "Londres", 4)
    g.addArc("Paris",  "Amsterdam", 3)
    g.addArc("Hambourg",  "Stockholm", 1)
    g.addArc("Hambourg",  "Berlin", 1)
    g.addArc("Londres",  "Edimbourg", 2)
    g.addArc("Amsterdam",  "Hambourg", 2)
    g.addArc("Amsterdam",  "Oslo", 8)
    g.addArc("Stockholm",  "Oslo", 2)
    g.addArc("Stockholm",  "Rana", 5)
    g.addArc("Berlin",  "Amsterdam", 2)
    g.addArc("Berlin",  "Stockholm", 1)
    g.addArc("Berlin",  "Oslo", 3)
    g.addArc("Edimbourg",  "Oslo", 7)
    g.addArc("Edimbourg",  "Amsterdam", 3)
    g.addArc("Edimbourg",  "Rana", 6)
    g.addArc("Oslo",  "Rana", 2)
    
    # Applique l'algorithme de Dijkstra pour obtenir une arborescence
    #tree = dijkstra(g, "Paris")
    #print(tree)
    # Appliquer Dijkstra
    distances, predecessors = dijkstra(g, "Paris")

    # Affichage des distances minimales depuis Paris
    print("\nDistances minimales depuis Paris :")
    for i, city in enumerate(cities):
        print(f"{city}: {distances[i]}")

    # Reconstruction des chemins
    print("\nChemins les plus courts :")
    for i, city in enumerate(cities):
        path = reconstruct_path(predecessors, g.indexOf("Paris"), i, cities)
        print(f"{city}: {' -> '.join(path)}")
    

def dijkstra(g, origin):
		
   # Get the index of the origin 
    r = g.indexOf(origin)

    # Next node considered 
    
    pivot = r
    
    # Liste qui contiendra les sommets ayant été considérés comme pivot
    # v2 --> visited
    v2 = []
    
    #Predecesseurs
    pred = [-1] * g.n
    # Les pi entre r et les autres sommets sont initialement infinies
    pi = [sys.float_info.max] * g.n
    pi[r] = 0 #distance(origin<-->pivot)

    while len(v2) < g.n:
        # Trouver le sommet avec la plus petite distance
        min_distance = sys.float_info.max
        
        pivot = -1
        for noued in range(g.n):
            if noued not in v2 and pi[noued] < min_distance:
                min_distance = pi[noued]
                pivot = noued
        if pivot == -1:
            break  # Plus de sommets atteignables

        v2.append(pivot)

        # Mise à jour des pi des voisins
        for neighbor in range(g.n):
            if g.adjacency[pivot][neighbor] > 0 and neighbor not in v2:
                new_pi = pi[pivot] + g.adjacency[pivot][neighbor]
                if new_pi < pi[neighbor]:
                    pi[neighbor] = new_pi
                    pred[neighbor] = pivot
    
    return pi, pred


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
    distances, predecessors = dijkstra(g1, "a")

    # Affichage des distances minimales depuis Paris
    print("\nDistances minimales depuis Paris :")
    for i, city in enumerate(cities):
        print(f"{city}: {distances[i]}")

    # Reconstruction des chemins
    print("\nChemins les plus courts :")
    for i, city in enumerate(cities):
        path = reconstruct_path(predecessors, g.indexOf("Paris"), i, cities)
        print(f"{city}: {' -> '.join(path)}")
    
def reconstruct_path(predecessors, start, end, cities):
    """Reconstitue le chemin le plus court depuis start jusqu'à end."""
    path = []
    current = end
    while current != -1:
        path.append(cities[current])
        if current == start:
            break
        current = predecessors[current]
    return path[::-1] 
   
if __name__ == '__main__':
    main()
