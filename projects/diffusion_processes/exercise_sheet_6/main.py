from itertools import product
from random import sample

import numpy as np
from matplotlib import pyplot as plt
import networkx as nx

from projects.diffusion_processes.exercise_sheet_6.network import Network, QPanel


def nn_q_panel(q) -> QPanel:
    def inner(graph: nx.Graph, spinson: int) -> list[int]:
        neighbours = list(graph.neighbors(spinson))
        return sample(neighbours, min(q, len(neighbours)))

    return inner


def plot_time_evolution_of_magnetization(graph: nx.Graph, q_panel: QPanel, p_vals: list = np.arange(0, 0.5, 0.02).tolist(), num_runs: int = 100):
    for p in p_vals:
        m_values = np.zeros((num_runs, 1000))
        for i in range(num_runs):
            network = Network(
                graph=graph.copy(),
                q_panel=q_panel,
                p=p,
            )
            m_values[i, :] = list(network.simulate_gen_magnetization())
        plt.plot(m_values.mean(axis=0))
    plt.show()


def get_final_magnetization(graph: nx.Graph, q_panel: QPanel, p: float) -> float:
    network = Network(
        graph=graph.copy(),
        q_panel=q_panel,
        p=p,
    )
    network.simulate_gen_magnetization()
    return network.magnetization


def plot_average_final_magnetization(graphs: dict[str, nx.Graph], q_panels: dict[str, QPanel], num_runs: int = 100):
    p_vals = np.arange(0, 0.5, 0.01).tolist()

    values: dict[str, list[float]] = {}
    for graph, q_panel in product(graphs, q_panels):
        label = f"{graph}/{q_panel}"
        values[label] = []
        for p in p_vals:
            magnetizations = []
            for _ in range(num_runs):
                network = Network(
                    graph=graphs[graph].copy(),
                    q_panel=q_panels[q_panel],
                    p=p,
                )
                network.simulate()
                magnetizations.append(network.magnetization)
            values[label].append(np.array(magnetizations).mean())

    for label, value in values.items():
        plt.plot(p_vals, value, label=label)

    plt.legend()
    plt.show()


def main():
    # plot_time_evolution_of_magnetization(graph=nx.watts_strogatz_graph(100, 4, 0.4), q_panel=nn_q_panel())

    plot_average_final_magnetization(
        graphs={
            "WS_001": nx.watts_strogatz_graph(100, 8, 0.01),
            "WS_02": nx.watts_strogatz_graph(100, 8, 0.2),
            "BA": nx.barabasi_albert_graph(100, 4),
        },
        q_panels={
            "NN4": nn_q_panel(4),
            "NN3": nn_q_panel(3),
        },
    )


if __name__ == "__main__":
    main()
