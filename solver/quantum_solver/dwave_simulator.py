import numpy as np

class DwaveSimulator:
    def __init__(self):
        # Le "planning" de l'évolution quantique : 101 pas de temps (s=0 à s=100)
        # Au début : A=1, B=0 → on est 100% dans H_init (état quantique facile)
        # À la fin : A=0, B=1 → on est 100% dans H_final (notre problème Ising)
        self.annealing_schedule = {
            'A': [1 - s/100 for s in range(101)],
            'B': [s/100 for s in range(101)]
        }

    def build_Hfinal(self, ising_problem):
        # H_final encode notre problème d'optimisation sous forme de matrice
        # Chaque variable s_i devient une matrice sigma_z placée au bon endroit
        # via des produits tensoriels (np.kron)
        linear = ising_problem['linear']       # poids des noeuds  {0: h0, 1: h1, ...}
        quadratic = ising_problem['quadratic'] # poids des arêtes  {(0,1): J01, ...}
        n = len(linear)

        sigma_z = np.array([[1, 0], [0, -1]])  # matrice de Pauli Z
        I = np.eye(2)                           # matrice identité 2x2

        H = np.zeros((2**n, 2**n))  # matrice finale de taille 2^n x 2^n

        # Pour chaque variable i : on place sigma_z à la position i,
        # et des identités partout ailleurs
        for i, h in linear.items():
            op = 1
            for k in range(n):
                op = np.kron(op, sigma_z if k == i else I)
            H += h * op  # on multiplie par le poids h_i

        # Pour chaque paire (i,j) : sigma_z en position i ET j, identités ailleurs
        for (i, j), J in quadratic.items():
            op = 1
            for k in range(n):
                op = np.kron(op, sigma_z if k == i or k == j else I)
            H += J * op  # on multiplie par le poids J_ij

        return H

    def build_Hinit(self, n):
        # H_init est le point de départ : une somme de sigma_x sur chaque qubit
        # C'est facile à préparer et son état fondamental est connu
        sigma_x = np.array([[0, 1], [1, 0]])  # matrice de Pauli X
        I = np.eye(2)

        H = np.zeros((2**n, 2**n))

        # Même logique que build_Hfinal mais avec sigma_x
        for i in range(n):
            op = 1
            for k in range(n):
                op = np.kron(op, sigma_x if k == i else I)
            H += op

        return H

    def simulate_evolution(self, ising_problem, nb_eigenvalues=3):
        # C'est le coeur du simulateur : on fait évoluer H(s) pas à pas
        # H(s) = A(s)*H_init + B(s)*H_final
        # À chaque pas, on diagonalise H(s) pour obtenir ses niveaux d'énergie
        n = len(ising_problem['linear'])

        H_init = self.build_Hinit(n)
        H_final = self.build_Hfinal(ising_problem)

        all_eigenvalues = []

        for s in range(101):
            A = self.annealing_schedule['A'][s]
            B = self.annealing_schedule['B'][s]

            H = A * H_init + B * H_final  # combinaison des deux Hamiltoniens

            # eigh diagonalise une matrice symétrique → donne les énergies triées
            eigenvalues, eigenvectors = np.linalg.eigh(H)

            # On ne garde que les nb_eigenvalues plus basses (les plus intéressantes)
            all_eigenvalues.append(eigenvalues[:nb_eigenvalues])

        return np.array(all_eigenvalues)  # shape : (101, nb_eigenvalues)