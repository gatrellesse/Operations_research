import numpy as np
import tableau
import math

"""
Représente un noeud d'un arbre de branch-and-bound
"""
class BBNode:

    # Tableau associé à la relaxation linéaire de ce noeud
    tableau
    
    # Profondeur du noeud (utilisé uniquement pour afficher l'arbre dans la console avec une indentation)
    depth = 0
    """     
    Créer un noeud racine
    - A: matrice des coefficients
    - rhs: second membre
    - obj: coefficients de l'objectif
    - isMinimization: True si on considère un problème de minimisation
    """
    @classmethod
    def create_root(cls, A, rhs, obj, isMinimization):
        return cls(A = A, rhs = rhs, obj = obj,  isMinimization = isMinimization)

    """
    Créer un noeud qui n'est pas racine en ajoutant une contrainte au problème de son noeud parent
    parent: Le noeud parent
    newA: Coefficients de la nouvelle contrainte
    newRhs: Second membre de la nouvelle contrainte
    """        
    @classmethod
    def create_non_root(cls, parent, newA, newRhs):
        return cls(parent = parent, newA = newA, newRhs = newRhs)
    
    """
     Résout la relaxation linéaire du noeud "self" et branche si nécessaire (i.e. si la relaxation fournit une solution fractionnaire)
     tree: L'arbre contenant le noeud "self"
    """ 
    def branch(self, tree):

        # Résout la relaxation linéaire
        print(f"Best objective {tree.bestObjective}")
        relaxedTableau = self.tableau.tableauWithSlack()
        relaxedTableau.applySimplex()

         # Vérifier si le problème est faisable
        if relaxedTableau.bestSolution is None:
            return  # Noeud infaisable, on ne branche pas

        current_obj = int(relaxedTableau.bestObjective)
        # Vérification du critère d'élagage
        if tree.bestSolution is not None:
            if self.tableau.isMinimization and current_obj >= tree.bestObjective:
                print(f"Pruning node at depth {self.depth}: Worse than best found.")
                return
            elif not self.tableau.isMinimization and current_obj <= tree.bestObjective:
                print(f"Pruning node at depth {self.depth}: Worse than best found.")
                return
        """
        I - Description des variables et de leurs attributs que vous devrez utiliser
         - Variable tableau : représente le programme linéaire associé à ce sommet (c'est donc un problème continu). Ses attributs sont :
            - bestSolution (tableau de float) : solution optimale continue trouvée (None si le PL est infaisable) 
            - bestObjective (float) : valeur optimale de l'objectif 
            - isMinimization (boolean) : indique si c'est un problème de minimisation 
            - n (int) : nombre de variables (et donc taille du tableau bestSolution) 
            - depth (int) : profondeur du sommet dans l'arbre (mis à jour dans le constructeur, utilisé uniquement pour l'indentation des affichages).
            
         - Variable tree : représente l'arbre de branchement dans lequel se trouve le sommet. Ses attributs sont :
            - tree.bestSolution (tableau de float) : meilleure solution entière trouvée (None si aucune n'a encore été trouvée) 
            - tree.bestObjective (float) : valeur de l'objectif de la meilleure solution entière connue. 
         
           II - Comment savoir si une variable d de type float est fractionnaire ?
           Utiliser "isFractional(d)" qui retourne "True" si d est fractionnaire.
           
           III - Comment calculer les parties entières inférieures et supérieures d'une variable de type float ?
           Utiliser "math.floor(d)" et "math.ceil(d)".
           
           IV - Comment créer un nouveau sommet en lui ajoutant une nouvelle contrainte de la forme newA * x <= newRhs ?
           Utiliser le constructeur "BBNode.create_non_root_node(parent, newA, newRhs)" dans lequel :
             - parent correspond au noeud actuellement considéré (l'objet actuellement considéré dans une classe est obtenu grâce au mot-clé "self" en python) 
             - newA : tableau contenant les coefficients de la nouvelle contrainte 
               (pour créer un tableau contenant 10 float initialisés à la valeur 0.0, vous pouvez utiliser la syntaxe : monTableau = np.array([0.0] * 10)
             - newRhs : valeur du second membre de la nouvelle contrainte.
             Attention : les contraintes du tableau sont de la forme Ax <= b. Si vous voulez ajouter une contrainte x1 >= 2 (qui est équivalente à -x1 <= -2), il faudra donc que newA[0] soit égal à -1 et newRhs soit égal à -2.
             
           V - Comment brancher sur un objet "node" de type BBNode situé dans un arbre "tree" ?
           node.branch(tree)
        """
        greatest_frac = 0
        x_branch = -1
        for idx in range(self.tableau.n):  # Only consider original variables
            val = relaxedTableau.bestSolution[idx]
            if isFractional(val):
                fractionality = val % 1
                if fractionality > greatest_frac:
                    greatest_frac = fractionality
                    x_branch = idx
        if x_branch != -1:
            input(f"BRANCHING LESSER ON X{x_branch} FOR {relaxedTableau.bestSolution[:2]}")
            # Première branche (x <= floor(bestSolution[x_branch]))
            newA = np.array([0.0] * self.tableau.n)
            newA[x_branch] = 1  # Coefficient pour x_branch
            newRhs = math.floor(relaxedTableau.bestSolution[x_branch])

            left_child = BBNode.create_non_root(self, newA, newRhs)
            left_child.branch(tree)

            # Deuxième branche (x >= ceil(bestSolution[x_branch])) <=> -x <= -ceil(bestSolution[x_branch])
            input(f"BRANCHING HIGHER ON X{x_branch} FOR {relaxedTableau.bestSolution[:2]}")
            newA = np.array([0.0] * self.tableau.n)
            newA[x_branch] = -1  # Contraintes sous la forme Ax <= b
            newRhs = -math.ceil(relaxedTableau.bestSolution[x_branch])

            right_child = BBNode.create_non_root(self, newA, newRhs)
            right_child.branch(tree)
        else:#solution entier trouve
            if (tree.bestSolution is None or 
                (self.tableau.isMinimization and current_obj < tree.bestObjective) or
                (not self.tableau.isMinimization and current_obj > tree.bestObjective)):
                print("New best integer solution found")
                tree.bestSolution = relaxedTableau.bestSolution[:self.tableau.n]  # Only original variables
                tree.bestObjective = int(current_obj)

        print(f"Current best integer solution: {tree.bestSolution}")
        # TODO




    """
         (attention : ne pas utiliser directement cette méthode, utiliser à la place create_root ou create_non_root)
         Constructeur qui peut soit :
         - créer une racine (si les attributs A, rhs, obj et isMinimization sont définis)
         - créer un noeud non-racine (si les attributs parent, newA, newRhs sont définis)
    """
    def __init__(self, A = None, rhs = None, obj = None, isMinimization = None, parent = None, newA = None, newRhs = None):

        # Si on crée une racine
        if parent == None:
            
            # Créer le tableau associé 
            self.tableau = tableau.Tableau(A, rhs, obj, isMinimization)
            self.depth = 0
        else:
            # Ajouter la contrainte
            self.depth = parent.depth + 1
            newMA = np.copy(parent.tableau.A)
            newMA = np.vstack([newMA, np.copy(newA)])

            newMRhs = np.append(parent.tableau.b, newRhs)

            # Créer le tableau avec la contrainte supplémentaire
            self.tableau = tableau.Tableau(newMA, newMRhs, parent.tableau.c, parent.tableau.isMinimization)

def isFractional(d): 
    return abs(round(d) - d) > 1E-6 
