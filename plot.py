import matplotlib.pyplot as plt
import networkx as nx


def plot_solution(data, model):
    plt.figure()

    for i in data.roots:
        plt.scatter(data.loc[i][0], data.loc[i][1], c='red')
        plt.annotate(i, (data.loc[i][0] + 2, data.loc[i][1]))

    for i in data.customers:
        plt.scatter(data.loc[i][0], data.loc[i][1], c='black')
        plt.annotate(i, (data.loc[i][0] + 2, data.loc[i][1]))

    for (i, j) in model.x_keys:
        if model.x[i, j].solution_value > 0.9:
            plt.plot([data.loc[i][0], data.loc[j][0]], [data.loc[i][1], data.loc[j][1]], c='blue', linewidth='1')
            plt.arrow(data.loc[i][0], data.loc[i][1], (data.loc[j][0] - data.loc[i][0]) / 2, (data.loc[j][1] - data.loc[i][1]) / 2, shape='full', lw=0, length_includes_head=True, head_width=0.035*data.width)

    for (i, j) in model.y_keys:
        if model.y[i, j].solution_value > 0.9:
            plt.plot([data.loc[i][0], data.loc[j][0]], [data.loc[i][1], data.loc[j][1]], c='red', linewidth='1')

    plt.show()


def create_network(data, model):
    G = nx.DiGraph()

    # Add root nodes to the graph and color them red
    roots = [i for i in data.roots]
    G.add_nodes_from(roots, color='red')

    # Add backbone nodes to the graph (nodes with solution value > 0.9) and color them orange
    backbone_nodes = [i for i in data.customers if model.w[i].solution_value > 0.9]
    G.add_nodes_from(backbone_nodes, color='orange')

    # Add leaf nodes to the graph (nodes with solution value < 0.1) and color them yellow
    leaf_nodes = [i for i in model.w_keys if model.w[i].solution_value < 0.1]
    G.add_nodes_from(leaf_nodes, color='yellow')

    # Add tree edges to the graph (edges with solution value > 0.9) and color them black
    tree_edges = [(i, j) for (i, j) in model.x_keys if model.x[i, j].solution_value > 0.9]
    G.add_edges_from(tree_edges, color="black")

    # Add assignment edges to the graph (edges with solution value > 0.9) and color them red
    assignment_edges = [(i, j) for (i, j) in model.y_keys if model.y[i, j].solution_value > 0.9]
    G.add_edges_from(assignment_edges, color="red")

    return G


def plot_graph(data, model):
    scaler = data.width

    # Create the network graph using the create_network function
    G = create_network(data, model)

    # Get the color attributes for nodes and edges
    node_colors = nx.get_node_attributes(G, 'color').values()
    edge_colors = nx.get_edge_attributes(G, 'color').values()

    # Define the positions of the nodes based on the data
    my_pos = {i: (data.loc[i][0], data.loc[i][1]) for i in data.V}

    # Define the drawing options for the graph
    options = {
        'pos': my_pos,
        'edge_color': edge_colors,
        'node_color': node_colors,
        'node_size': 2 * scaler,
        'arrowstyle': '-|>',
        'arrowsize': 0.12 * scaler,
        'with_labels': True,
    }
    nx.draw_networkx(G, arrows=True, **options)

    # Adjust the layout and display the graph
    plt.tight_layout()
    plt.draw()
    plt.show()
