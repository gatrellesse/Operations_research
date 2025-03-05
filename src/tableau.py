import numpy as np
import sys

class Tableau:

    # Nombre de variables
    n = 0

    # Nombre de contraintes
    m = 0

    A = np.empty(0)
    b = np.array([])
    c = np.array([])

    # Base actuelle ou [] si aucune n'a été définie
    basis = np.array([])

    # Vector de taille n contenant la meilleure solution actuellement connue (ou [] si aucune n'a été trouvée) 
    bestSolution = None

    # Valeur de l'objectif de la meilleure solution connue
    bestObjective = 0

    # Vrai si on considère un problème dont l'objectif est une minimisation
    isMinimization = True

    # Vrai si on souhaite afficher le tableau à chaque itération de l'algorithme
    DISPLAY_SIMPLEX_LOGS = True
    
    # Crée un tableau
    def __init__(self, A, b, c, isMinimization):

        self.n = len(c)
        self.m = len(A)
        self.A = A.astype(np.float64)
        self.b = b.astype(np.float64)
        self.c = c.astype(np.float64)
        self.isMinimization = isMinimization

        self.basis = np.array([])
        self.bestSolution = None
        self.bestObjective = 0.0

    @staticmethod
    def ex1(): 
        A = np.array([[1, -1], [0, 1], [8, 5]], dtype=float)
        c = np.array([2, 1], dtype=float)
        b = np.array([4, 8, 56], dtype=float)
        return Tableau(A, b, c, False) 

    @staticmethod
    def ex2():
        A = np.array([[1, -2, 1, -1, 0, 0], [0, 1, 3, 0, 1, 0], [2, 0, 1, 2, 0, 1]], dtype=float)
        c = np.array([2, -3, 5, 0, 0, 0], dtype=float)
        b = np.array([4, 6, 7], dtype=float)
        return Tableau(A, b, c, True)

    @staticmethod
    def main():
        # Si le problème n'est pas sous forme normale, il faut le transformer 
        normalForm = True

        # Si on résout un problème sous forme normale 
        if normalForm:
            #** 1er cas - PL Ax = b et une base est fournie (aucune variable d'écart n'est ajoutée au problème) 
            t1 = Tableau.ex2()
            t1.basis = np.array([0, 2, 5])
            t1.applySimplex()
            
        # Si on résout un problème qui n'est pas sous forme normale 
        else: 
            #** 2ème cas - PL Ax <= b, ajouter des variables d'écart et les utiliser comme base
            t2 = Tableau.ex1()
            t2.addSlackAndSolve()
            t2.displaySolution()

    # Crée un tableau avec une variable d'écart pour chaque contrainte et résoudre
    def addSlackAndSolve(self):
        # Crée un tableau dans lequel une variable d'écart est ajouté pour chaque contrainte 
        # et sélectionne les variables d'écart comme base
        tSlack = self.tableauWithSlack()

        # Applique l'algorithme du simplexe sur le tableau avec les variables d'écart
        tSlack.applySimplex()

        # Met la solution dans tSlack
        self.setSolution(tSlack)

    # Applique l'algorithme du simplexe
    def applySimplex(self):
        # Affiche le tableau initial
        if self.DISPLAY_SIMPLEX_LOGS:
            print("Tableau initial: ")
            self.display()
        
        # Perturbe chaque valeur de b pour éviter les divisions par zéro quand la base est dégénérée
        eps = 1E-7
        
        for i in range(self.m):
            self.b[i] += eps
            eps *= 0.1

        # Tant que la solution de base peut être améliorée, effectuer un pivotage
        while self.pivot():
            if self.DISPLAY_SIMPLEX_LOGS:
                self.display()

        # Afficher le tableau final
        if self.DISPLAY_SIMPLEX_LOGS:
            print("Final array")
            self.display()

    # Effectuer un pivotage
    def pivot(self):
        # 1) Mise sous forme canonique
        for i in range(self.m):
            # Normalize the pivot row --> A[i][basis[i]] = 1
            pivot = self.A[i][self.basis[i]]
            if abs(pivot) < 1e-12:  # Avoid division by zero
                continue
            self.A[i] /= pivot
            self.b[i] /= pivot

            # Make all other rows zero in the pivot column
            for j in range(self.m):
                if j != i:
                    multiply_factor = self.A[j][self.basis[i]]
                    self.A[j] -= multiply_factor * self.A[i]
                    self.b[j] -= multiply_factor * self.b[i]

            # Update the objective row
            multiply_factor = self.c[self.basis[i]]
            self.c -= multiply_factor * self.A[i]
            self.bestObjective += multiply_factor * self.b[i]

        # 2) Find the entering variable
        var_entrant = -1
        max_reduced_cost = 1e-6 if self.isMinimization else -1e-6

        for j in range(self.n):
            if j not in self.basis:
                reduced_cost = self.c[j]
                if (self.isMinimization and reduced_cost < -1e-6) or (not self.isMinimization and reduced_cost > 1e-6):
                    if (self.isMinimization and reduced_cost < max_reduced_cost) or (not self.isMinimization and reduced_cost > max_reduced_cost):
                        max_reduced_cost = reduced_cost
                        var_entrant = j
                        #

        # If no entering variable is found, the solution is optimal
        if var_entrant == -1:
            return False

        # 3) Find the leaving variable
        leaving_var = -1
        min_ratio = float('inf')

        for i in range(self.m):
            if self.A[i][var_entrant] > 1e-6:
                ratio = self.b[i] / self.A[i][var_entrant]
                if ratio < min_ratio:
                    min_ratio = ratio
                    leaving_var = i

        # If no leaving variable is found, the problem is unbounded
        if leaving_var == -1:
            raise ValueError("The problem is unbounded.")

        # 4) Update the basis
        self.basis[leaving_var] = var_entrant

        return True

    # Obtenir la solution du tableau qui est supposé être sous forme canonique
    def getSolution(self):
        self.bestSolution = np.array([0.0] * self.n)

        # For each basic variable, get its value 
        for varBase in range(self.m):
            varId = self.basis[varBase]
            self.bestSolution[varId] = self.b[varBase]

    # Fixer la solution du tableau self à celle du tableau tSlack
    def setSolution(self, tSlack):
        # Obtenir la solution de tSlack
        tSlack.getSolution()

        self.bestSolution = np.array([0.0] * self.n)

        for varId in range(self.n):
            self.bestSolution[varId] = tSlack.bestSolution[varId]
            print("varId = ", varId, " solution value: ", "%.2f" % tSlack.bestSolution[varId])

        self.bestObjective = tSlack.bestObjective

    # Afficher la solution courante
    def displaySolution(self):
        print("z = ", "%.2f" % self.bestObjective, ", ", end='')

        variables = "("
        values = "("
        for i in range(len(self.bestSolution)):
            if self.bestSolution[i] != 0.0:
                variables += "x" + str(i+1) + ", "
                if self.isFractional(self.bestSolution[i]):
                    values += str("%.2f" % self.bestSolution[i]) + ", "
                else:
                    values += str("%.2f" % self.bestSolution[i]) + ", "

        variables = variables[0:max(0, len(variables) - 2)]
        values = values[0:max(0, len(values) - 2)]
        print(variables, ") = ", values, ")")

    # Crée un tableau avec une variable d'écart pour chaque contrainte et utilise ces variables d'écart comme base
    def tableauWithSlack(self):
        ASlack = np.zeros((self.m, self.n + self.m))

        # Pour chaque contrainte
        for cstr in range(self.m):
            # Fixer les coefficients des n variables d'origine
            for col in range(self.n):
                ASlack[cstr][col] = self.A[cstr][col]

            # Fixer le coefficient de la variable de slack non nulle
            ASlack[cstr][self.n + cstr] = 1.0

        # Augmenter le nombre de variables dans l'objectif
        cSlack = np.array([0.0] * (self.n + self.m))

        for i in range(self.n):
            cSlack[i] = self.c[i]

        # Créer une base avec les variables d'écart
        self.basis = np.array([0] * self.m)

        for i in range(self.m):
            self.basis[i] = i + self.n

        slackTableau = Tableau(ASlack, self.b, cSlack, self.isMinimization)
        slackTableau.basis = self.basis

        return slackTableau

    # Afficher le tableau
    def display(self):
        toDisplay = "\nVar.\t"

        for i in range(self.n):
            toDisplay += "x" + str(i+1) + "\t"

        dottedLine = ""
        for i in range(self.n + 2):
            dottedLine += "--------"

        print(toDisplay, "  (RHS)\t\n", dottedLine)

        for l in range(self.m):
            toDisplay = "(C" + str(l+1) + ")\t"
            for c in range(self.n):
                toDisplay += str("%.2f" % self.A[l][c]) + "\t"
            print(toDisplay, "| ",  "%.2f" % self.b[l])

        print(dottedLine)
        toDisplay = "(Obj)\t"
        for i in range(self.n):
            toDisplay += str("%.2f" % self.c[i]) + "\t"
        print(toDisplay, "|  ", "%.2f" % self.bestObjective)

        # Si un solution a été calculée
        if len(self.basis) > 0:
            print(dottedLine)
            self.getSolution()
            self.displaySolution()
        print()

    # Fonction pour vérifier si un nombre est fractionnaire
    def isFractional(self, d): 
        return abs(round(d) - d) > 1E-6

if __name__ == '__main__':
    Tableau.main()