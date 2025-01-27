from cplex.callbacks import *
from docplex.mp.callbacks.cb_mixin import *
import numpy as np
from plot_class import *


class Callback_lazy(ConstraintCallbackMixin, LazyConstraintCallback):
    def __init__(self, env):
        """
        Initializes the Callback_lazy class.

        Args:
            env: CPLEX environment.

        Returns:
            None
        """
        LazyConstraintCallback.__init__(self, env)
        ConstraintCallbackMixin.__init__(self)

    def __call__(self):
        """
        Callback function to be called for lazy constraint callback.
        This function is called during the optimization process to add
        lazy constraints when the solution violates certain conditions.

        Returns:
            None
        """
        print('running lazy callback......')
        # Retrieve solution values for x and y variables
        sol_x = self.make_solution_from_vars(self.model_instance.x.values())
        sol_y = self.make_solution_from_vars(self.model_instance.y.values())
        sol_w = self.make_solution_from_vars(self.model_instance.w.values())
        K = self.model_instance.k

        # Create a graph G and add nodes
        G = nx.Graph()
        # nodes = [i for i in self.model_instance.data.V if sol_w[i] > 0]
        G.add_nodes_from(self.model_instance.data.V)

        # Add the source and the sink
        source = -1
        sink = -2
        G.add_nodes_from([source, sink])

        # Add edges to the graph G based on the solution values of x and y variables
        edges = []
        for (i, j) in self.model_instance.x_keys:
            if sol_x.get_value(self.model_instance.x[i, j]) > 1e-6:
                edges.append((i, j, {'capacity': min(1, sol_x.get_value(self.model_instance.x[i, j]))}))

        for r in self.model_instance.data.roots:
            # get the neighbourhood of root r
            array = [j for (i, j) in self.model_instance.data.edges if i == r]
            # get the maximal x_rj
            sr_capacity = max(array, key=lambda j: sol_x.get_value(self.model_instance.x[r, j]))
            edges.append((source, r, {'capacity': sr_capacity}))

        for costumer in self.model_instance.data.customers:
            edges.append((costumer, sink, {'capacity': 0}))

        G.add_edges_from(edges)

        min_cut, min_cut_vertex, cut_partition = np.inf, -1, None

        for i in self.model_instance.data.customers:
            for j in self.model_instance.data.customers:
                if i != j:
                    G[j][sink]['capacity'] = K * sol_y.get_value(self.model_instance.y[j, i])
            G[i][sink]['capacity'] = K * sol_w.get_value(self.model_instance.w[i])
            cut_value, partition = nx.minimum_cut(G, source, sink)
            if cut_value < min_cut and len(partition[1]) > 3:
                min_cut = cut_value
                min_cut_vertex = i
                cut_partition = partition

        print(min_cut)
        print(min_cut_vertex)
        print(cut_partition)

        if min_cut < K - 1e-2:
            print(sol_w.get_value(self.model_instance.w[min_cut_vertex]))
            print(cut_partition[1])
            num_of_roots = 0
            for i in cut_partition[1]:
                if 0 <= i <= self.model_instance.data.n - 1:
                    num_of_roots += 1

            cut_set = [(o, i) for (o, i) in self.model_instance.x_keys if
                       o not in cut_partition[1] and i in cut_partition[1]]
            c_edges = [(o, i) for (o, i) in self.model_instance.y_keys if
                       o in cut_partition[1] and i == min_cut_vertex]

            if min_cut_vertex in cut_partition[1]:
                ct = self.model_instance.model.sum(self.model_instance.x[o, i] for (o, i) in cut_set) >= \
                     (K - num_of_roots) * (
                                 self.model_instance.model.sum(self.model_instance.y[p, q] for (p, q) in c_edges) +
                                 self.model_instance.w[min_cut_vertex])

            else:
                ct = self.model_instance.model.sum(self.model_instance.x[o, i] for (o, i) in cut_set) >= \
                     (K - num_of_roots) * (
                             self.model_instance.model.sum(self.model_instance.y[p, q] for (p, q) in c_edges))

            ct_cpx = self.linear_ct_to_cplex(ct)
            print(ct)
            self.add(ct_cpx[0], ct_cpx[1], ct_cpx[2])
            print('added lazy cut')


class Callback_user(ConstraintCallbackMixin, UserCutCallback):
    def __init__(self, env):
        """
        Initializes the Callback_user class.

        Args:
            env: CPLEX environment.

        Returns:
            None
        """
        UserCutCallback.__init__(self, env)
        ConstraintCallbackMixin.__init__(self)

    def __call__(self):
        """
        Callback function to be called for user cut callback.

        Returns:
            None
        """

        print('running user callback......')

        # Retrieve solution values for x and y variables
        sol_x = self.make_solution_from_vars(self.model_instance.x.values())
        sol_y = self.make_solution_from_vars(self.model_instance.y.values())
        sol_w = self.make_solution_from_vars(self.model_instance.w.values())
        K = self.model_instance.k

        if self.get_num_nodes() == 0:
            self.best_gap_root_node = self.get_MIP_relative_gap()
            print(self.get_lower_bounds())
            print(self.get_upper_bounds())


        # Create a graph G and add nodes
        G = nx.Graph()
        # nodes = [i for i in self.model_instance.data.V if sol_w[i] > 0]
        G.add_nodes_from(self.model_instance.data.V)

        # Add the source and the sink
        source = -1
        sink = -2
        G.add_nodes_from([source, sink])

        # Add edges to the graph G based on the solution values of x and y variables
        edges = []
        for (i, j) in self.model_instance.x_keys:
            if sol_x.get_value(self.model_instance.x[i, j]) > 1e-6:
                edges.append((i, j, {'capacity': min(1, sol_x.get_value(self.model_instance.x[i, j]))}))

        for r in self.model_instance.data.roots:
            # get the neighbourhood of root r
            array = [j for (i, j) in self.model_instance.data.edges if i == r]
            # get the maximal x_rj
            sr_capacity = max(array, key=lambda j: sol_x.get_value(self.model_instance.x[r, j]))
            edges.append((source, r, {'capacity': sr_capacity}))

        for costumer in self.model_instance.data.customers:
            edges.append((costumer, sink, {'capacity': 0}))

        G.add_edges_from(edges)

        min_cut, min_cut_vertex, cut_partition = np.inf, -1, None

        for i in self.model_instance.data.customers:
            for j in self.model_instance.data.customers:
                if i != j:
                    G[j][sink]['capacity'] = K * sol_y.get_value(self.model_instance.y[j, i])
            G[i][sink]['capacity'] = K * sol_w.get_value(self.model_instance.w[i])
            cut_value, partition = nx.minimum_cut(G, source, sink)
            if cut_value < min_cut and len(partition[1]) > 3:
                min_cut = cut_value
                min_cut_vertex = i
                cut_partition = partition

        if min_cut < K - 1e-2:
            print(sol_w.get_value(self.model_instance.w[min_cut_vertex]))
            print(cut_partition[1])
            num_of_roots = 0
            for i in cut_partition[1]:
                if 0 <= i <= self.model_instance.data.n - 1:
                    num_of_roots += 1

            cut_set = [(o, i) for (o, i) in self.model_instance.x_keys if
                       o not in cut_partition[1] and i in cut_partition[1]]
            c_edges = [(o, i) for (o, i) in self.model_instance.y_keys if
                       o in cut_partition[1] and i == min_cut_vertex]

            print('The left hand side is', sum([sol_x.get_value(self.model_instance.x[i, j]) for (i, j) in cut_set]))
            value = sol_w.get_value(self.model_instance.w[min_cut_vertex])
            value += sum([sol_y.get_value(self.model_instance.y[i, j]) for (i, j) in c_edges])
            print('The right hand side is:', 3 * value)
            if min_cut_vertex in cut_partition[1]:
                ct = self.model_instance.model.sum(self.model_instance.x[o, i] for (o, i) in cut_set) >= \
                     (K - num_of_roots) * ((self.model_instance.model.sum(self.model_instance.y[p, q] for (p, q) in c_edges)) +
                    self.model_instance.w[min_cut_vertex])
            else:
                print(min_cut_vertex)
                ct = self.model_instance.model.sum(self.model_instance.x[o, i] for (o, i) in cut_set) >= \
                     (K - num_of_roots) * (self.model_instance.model.sum(self.model_instance.y[p, q] for (p, q) in c_edges))
                print(ct)

            ct_cpx = self.linear_ct_to_cplex(ct)
            print(ct)
            self.add(ct_cpx[0], ct_cpx[1], ct_cpx[2])
            print('added user cut')


class HeuristicsCallback(ConstraintCallbackMixin, HeuristicCallback):

    def __init__(self, env):
        HeuristicCallback.__init__(self, env)
        ConstraintCallbackMixin.__init__(self)


    def __call__(self):
        print('run heuristic')
        # build solution
        print(self.get_cplex_status())
        
        cost = 0
        if cost < self.get_incumbent_objective_value():
            # tb = heu.current_tour
            weights = []
            c = []
            for (i, j) in self.model_instance.x:
                c.append(self.model_instance.x[i, j].name)
                # if (i, j) in tb:
                #     weights.append(1)
                # else:
                #     weights.append(0)
            for (i, j) in self.model_instance.y:
                c.append(self.model_instance.y[i, j].name)

            # self.set_solution([c, weights], cost)
            # print("Incumbent updated with cost = " + str(cost))
            print(c)
        else:
            print("failed")