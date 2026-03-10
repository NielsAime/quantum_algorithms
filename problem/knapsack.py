# Ce fichier définit le problème du Sac à dos (Knapsack 0/1).
# On a une liste d'objets avec un poids et une valeur.
# Le but est de maximiser la valeur totale sans dépasser la capacité du sac.
# Chaque objet peut être pris (1) ou pas (0), d'où le "0/1".

import random


class KnapsackProblem:

    def __init__(self, weights, values, capacity):
        if len(weights) != len(values):
            raise ValueError("weights et values doivent avoir la même longueur.")
        self.weights = list(weights)
        self.values = list(values)
        self.capacity = capacity
        self.n_items = len(weights)

    def __repr__(self):
        return f"KnapsackProblem(n_items={self.n_items}, capacity={self.capacity})"

    @staticmethod
    def generate_random(n_items, capacity=None, weight_range=(1, 20), value_range=(1, 50), seed=None):
        if seed is not None:
            random.seed(seed)
        weights = [random.randint(*weight_range) for _ in range(n_items)]
        values  = [random.randint(*value_range)  for _ in range(n_items)]
        if capacity is None:
            capacity = sum(weights) // 2
        return KnapsackProblem(weights, values, capacity)
import random


class KnapsackProblem:

    def __init__(self, weights, values, capacity):
        if len(weights) != len(values):
            raise ValueError("weights et values doivent avoir la même longueur.")
        self.weights = list(weights)
        self.values = list(values)
        self.capacity = capacity
        self.n_items = len(weights)

    def __repr__(self):
        return f"KnapsackProblem(n_items={self.n_items}, capacity={self.capacity})"

    @staticmethod
    def generate_random(n_items, capacity=None, weight_range=(1, 20), value_range=(1, 50), seed=None):
        if seed is not None:
            random.seed(seed)
        weights = [random.randint(*weight_range) for _ in range(n_items)]
        values  = [random.randint(*value_range)  for _ in range(n_items)]
        if capacity is None:
            capacity = sum(weights) // 2
        return KnapsackProblem(weights, values, capacity)