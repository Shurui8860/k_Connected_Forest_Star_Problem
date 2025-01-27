from docplex.mp.model import Model


class KfspModel:
    def __init__(self, name, data, k):
        self.data = data  # Instance of Data class containing problem data
        self.model = Model(name)  # Create a new optimization model with the given name
        self.k = k  # Connectedness

        # Define keys for binary decision variables
        self.x_keys = [(i, j) for (i, j) in data.edges]
        self.y_keys = [(i, j) for (i, j) in data.edges]
        self.w_keys = [v for v in data.V]

        # Define keys for binary decision variables
        self.x = self.model.binary_var_dict(self.x_keys, name='x')
        self.y = self.model.binary_var_dict(self.y_keys, name='y')
        self.w = self.model.binary_var_dict(self.w_keys, name='w')

        # Define objective function: minimize total costs including assignment costs and connectedness cost
        self.model.minimize(
            self.model.sum(self.x[i, j] * data.c[i, j] for (i, j) in data.edges)
            + self.model.sum(self.y[i, j] * data.a[i, j] for (i, j) in data.edges))

        # fix the roots
        self.model.add_constraints(self.w[i] == 1 for i in data.roots)

        self.model.add_constraints(self.x[i, j] >= 0 for (i, j) in data.edges)
        self.model.add_constraints(self.y[i, j] >= 0 for (i, j) in data.edges)
        self.model.add_constraints(self.w[i] >= 0 for i in data.V)

        self.model.add_constraints(self.model.sum(self.x[p, i] for (p, q) in data.edges if q == i) >= k * self.w[i]
                                   for i in data.customers)

        # i can be assigned to other vertex iff i is not on a tree.
        self.model.add_constraints(self.model.sum(self.y[p, i] for (p, q) in self.data.edges if q == i) == 1 - self.w[i]
                                   for i in data.customers)

        # j can be connected or assigned to i in a tree only if i is on a tree plus no bi-directed loops
        self.model.add_constraints(self.x[i, j] + self.y[i, j] + self.x[j, i] <= self.w[i]
                                   for (i, j) in data.edges if (j, i) in data.edges)

        # j can be assigned to i only if i is on a tree
        self.model.add_constraints(self.x[i, j] + self.y[i, j] <= self.w[i]
                                   for (i, j) in data.edges if (j, i) not in data.edges)

        # j can be assigned to i only if i is on a tree
        self.model.add_constraints(self.y[i, j] == 0 for (i, j) in data.edges if i in data.roots)

    def solve(self, log=False):
        self.solution = self.model.solve(log_output=log)