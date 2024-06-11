from random import sample

import numpy as np
from matplotlib import pyplot as plt
import networkx as nx

from projects.diffusion_processes.exercise_sheet_6.network import Network


def nn_q_panel(graph: nx.Graph, spinson: int) -> list[int]:
    neighbours = list(graph.neighbors(spinson))
    return sample(neighbours, min(4, len(neighbours)))


def main():
    m_values = np.zeros((100, 1000))
    for i in range(30):
        print(i)
        graph = nx.watts_strogatz_graph(100, 4, 0.4)
        network = Network(graph, nn_q_panel, 0.2)
        m_values[i, :] = list(network.simulate())

    plt.plot(m_values.mean(axis=0))
    plt.show()


if __name__ == "__main__":
    main()
