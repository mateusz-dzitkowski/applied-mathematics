from itertools import product

import numpy as np

from multiprocessing import Pool
from projects.agent_based_modelling.assignment_6.model import Model, Params
from projects.agent_based_modelling.assignment_6.runge_kutta import runge_kutta_4

from matplotlib import pyplot as plt
import networkx as nx


GRAPH_SIZES = [100]
MEAN_DEGREES = [8]
INITIAL_ADOPTIONS = [0, 8]
PARAMS = [Params(innovation=innovation, imitation=imitation) for innovation, imitation in product([0, 0.01], [0.25, 0.5])]

REWIRING_PROBABILITIES = [0.3, 0.6, 0.9]
TIME_TO_STABILISE_RUNS = 10


def plot_evolutions():
    setups = list(product(PARAMS, INITIAL_ADOPTIONS, GRAPH_SIZES, MEAN_DEGREES))
    fig, axs = plt.subplots(len(setups), 1, figsize=(10, 6*len(setups)), layout="tight")

    for ax, (params, initial_adoptions, graph_size, mean_degree) in zip(axs, setups):
        for beta in REWIRING_PROBABILITIES:
            ax.plot(
                Model(
                    params=params,
                    graph=nx.watts_strogatz_graph(graph_size, mean_degree, beta),
                    initial_adoptions=initial_adoptions,
                ).run().adoption_history,
                label=f"{beta=}",
            )
            ax.set_title(f"{params=}, {initial_adoptions=}, {graph_size=}, {mean_degree=}")
        ax.legend()
        ax.set_ylim(-0.05, 1.05)
        ax.grid()

    plt.show()


def calculate_steps(args: tuple[Params, int, int, int, float]) -> int:
    params, initial_adoptions, graph_size, mean_degree, beta = args
    return Model(
        params=params,
        graph=nx.watts_strogatz_graph(graph_size, mean_degree, beta),
        initial_adoptions=initial_adoptions,
    ).run().current_step


def plot_time_to_stabilise():
    setups = list(product(PARAMS, INITIAL_ADOPTIONS, GRAPH_SIZES, MEAN_DEGREES))
    fig, ax = plt.subplots(1, 1, figsize=(30, 8), layout="tight")
    with Pool() as pool:
        for params, initial_adoptions, graph_size, mean_degree in setups:
            print(f"{params=}, {initial_adoptions=}, {graph_size=}, {mean_degree=}")
            beta = np.linspace(0, 1, 100)
            time_to_stabilise = np.array(
                [
                    np.array(pool.map(calculate_steps, [(params, initial_adoptions, graph_size, mean_degree, b)] * TIME_TO_STABILISE_RUNS)).mean()
                    for b in beta
                ]
            )
            ax.plot(beta, time_to_stabilise, label=f"{params=}, {initial_adoptions=}, {graph_size=}, {mean_degree=}")

    ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.show()


def main():
    # plot_evolutions()
    plot_time_to_stabilise()


if __name__ == "__main__":
    main()
