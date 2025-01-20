from itertools import product

from projects.agent_based_modelling.assignment_6.model import Model, Params
from projects.agent_based_modelling.assignment_6.runge_kutta import runge_kutta_4

from matplotlib import pyplot as plt
import networkx as nx


GRAPH_SIZES = [100]
MEAN_DEGREES = [8]
INITIAL_ADOPTIONS = [0, 8]
PARAMS = [Params(innovation=innovation, imitation=imitation) for innovation, imitation in product([0, 0.01], [0.25, 0.5])]

REWIRING_PROBABILITIES = [0.3, 0.6, 0.9]


def plot_evolutions():
    setups = list(product(PARAMS, INITIAL_ADOPTIONS, GRAPH_SIZES, MEAN_DEGREES))
    fig, axs = plt.subplots(len(setups), 1, figsize=(10, 6*len(setups)), layout="tight")

    for i, ((params, initial_adoptions, graph_size, mean_degree), ax) in enumerate(zip(setups, axs)):
        for beta in REWIRING_PROBABILITIES:
            model = Model(
                params=params,
                graph=nx.watts_strogatz_graph(graph_size, mean_degree, beta),
                initial_adoptions=initial_adoptions,
            )
            model.run()
            ax.plot(model.adoption_history, label=f"{beta=}")
            ax.set_title(f"{params=}, {initial_adoptions=}, {graph_size=}, {mean_degree=}")
        ax.legend()
        ax.set_ylim(-0.05, 1.05)
        ax.grid()

    plt.show()


def main():
    plot_evolutions()


if __name__ == "__main__":
    main()
