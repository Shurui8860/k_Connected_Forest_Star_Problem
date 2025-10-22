from data import *
from model import *
from callback import *
import random


num_of_roots, num_of_customers = 3, 24
k, const, seed = 3, 2, 0
# seed = random.randint(0, 100)

p = Data(num_of_roots, num_of_customers)

p.create_data(const=const, seed=seed, width=100)
m = KfspModel("KFSP", p, k)

cb_lazy = m.model.register_callback(Callback_lazy)
cb_lazy.model_instance = m
cb_lazy.problem_data = p
cb_lazy.num_calls = 0

cb_user = m.model.register_callback(Callback_user)
cb_user.model_instance = m
cb_user.problem_data = p
cb_user.num_calls = 0
cb_user.best_gap_root_node = np.infty

# cb_heur = m.model.register_callback(HeuristicsCallback)
# cb_heur.model_instance = m
# cb_heur.problem_data = p


m.solve(True)
print('The objective function is:', round(m.solution.get_objective_value(), 2))
print(cb_user.best_gap_root_node)
plot_graph(p, m)
