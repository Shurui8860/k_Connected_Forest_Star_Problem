import numpy as np
import math


class Data:
    def __init__(self, n, m):
        self.n = n  # Number of roots
        self.m = m  # Number of customers

        self.roots = range(self.n)  # Define index set for roots
        self.customers = range(self.n, self.n + self.m)  # Define index set for customers

        self.V = [*self.roots, *self.customers]
        self.loc = []  # Locations of roots and customers
        self.edges = []
        self.edges_customers = []

        self.c = np.zeros((self.n + self.m, self.n + self.m))  # Distance matrix
        self.a = np.zeros((self.n + self.m, self.n + self.m))  # Assignment cost matrix

    def create_data(self, width=100, const=None, seed=0):
        self.width = width

        # Create random number generator with seed
        rnd = np.random.RandomState(seed)

        # Define boundaries for random location generation
        width_1 = - width
        width_2 = width
        length_1 = - width
        length_2 = width

        # Generate set of all possible edges
        self.edges = \
            [(i, j) for i in self.V for j in self.customers if i != j]

        self.edges_customers = \
            [(i, j) for i in self.customers for j in self.customers if i != j]

        # Generate random locations for all vertices
        self.loc = {i: (width_1 + rnd.random() * (width_2 - width_1),
                        length_1 + rnd.random() * (length_2 - length_1)) for i in self.V}

        # Calculate distances between each pair of customers
        for i in self.V:
            for j in self.V:
                self.c[i, j] = math.hypot(self.loc[i][0] - self.loc[j][0], self.loc[i][1] - self.loc[j][1])

        if const is None:
            self.a = self.k * self.c
        else:
            self.a = const * self.c
