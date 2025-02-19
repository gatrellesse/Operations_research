import numpy as np
import math
import tableau
import bbNode
import bbTree

"""
Représente un noeud de branch-and-bound pour un problème de sac-à-dos
""" 
class KnapsackBBNode(bbNode.BBNode):

    # Poids des objets
    p = np.array([])
    
    # Capacité du sac-à-dos
    K = 0
    
    # Créer une feuille
    @classmethod
    def create_non_root(cls, parent, newA, newRhs, p, K):
        this = cls(parent = parent, newA = newA, newRhs = newRhs)
        this.p = p
        this.K = K
        return this
    
    # Créer une racine
    @classmethod
    def create_root(cls, A, rhs, obj, isMinimization, p, K):
        this = cls(A = A, rhs = rhs, obj = obj, isMinimization = isMinimization)
        this.p = p
        this.K = K
        return this
    
    # Génère une inégalité de couverture pour couper la solution optimale de la relaxation linéaire
    def generateCut(self):

        """
        Objectifs
         - Créer une liste contenant l'indice des objets figurant dans la coupe 
         - Ajouter la coupe au problème (utiliser la méthode addCoverCutToTableau de la classe Tableau)
         - Résoudre à nouveau le programme linéaire (utiliser la méthode applySimplexPhase1And2 de la classe Tableau)
         
        Indications
         I - Comment créer une variable de type liste d'entiers nommée l ?
         List<Integer> l = new ArrayList<>()
          
         II - Comment ajouter un élément à une liste d'entiers ?
         l.add(3)
        """ 
         
        # TODO

    def branch(self, tree):

        # TODO

    """
     Ajouter la coupe de couverture correspondant aux indices de la liste "cover"
     cover: Liste d'indices d'objets
    """ 
    def addCoverCutToTableau(self, cover):
        
        # Ajoute la coupe correspondant à la couverture
        m = self.tableau.m + 1
        n = self.tableau.n

        newMA = np.empty(shape=(m,n))

        for cstr in range(m-1):
            for var in range(n):
                newMA[cstr][var] = self.tableau.A[cstr][var] 

        for var in range(n):
            if var in cover:
                newMA[m-1][var] = 1.0
            else:
                newMA[m-1][var] = 0.0

        newMRhs = np.array([0.0] * m)

        for cstr in range(m-1):
            newMRhs[cstr] = self.tableau.b[cstr]

        newMRhs[m - 1] = len(cover) - 1

        self.tableau = tableau.Tableau(newMA, newMRhs, self.tableau.c, self.tableau.isMinimization)


def main():
    
    kTree = exKnapsackWithoutCuts()
    kTree.solve()
    
    kTreeCuts = exKnapsackWithCuts()
    kTreeCuts.solve()

def exKnapsackWithoutCuts(): 

    K = 17
    mA = np.array([[3, 7, 9, 6],
        [1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]])

    rhs = np.array([K, 1, 1, 1, 1])
    obj = np.array([8, 18, 20, 11])
    isMinimization = False

    return bbTree.BBTree(bbNode.BBNode.create_root(mA, rhs, obj, isMinimization))

def exKnapsackWithCuts(): 

    K = 17
    mA = np.array([[3, 7, 9, 6],
        [1, 0, 0, 0], \
        [0, 1, 0, 0], \
        [0, 0, 1, 0], \
        [0, 0, 0, 1]])

    rhs = np.array([K, 1, 1, 1, 1])
    obj = np.array([8, 18, 20, 11])
    isMinimization = False

    return bbTree.BBTree(KnapsackBBNode.create_root(mA, rhs, obj, isMinimization, mA[0], K))

def isFractional(d): 
    return abs(round(d) - d) > 1E-6 

if __name__ == '__main__':
    main()
