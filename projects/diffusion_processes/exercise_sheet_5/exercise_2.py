from enum import StrEnum, auto
from random import randint, uniform
from typing import TypeAlias

import networkx as nx
import numpy as np
from nptyping import NDArray
from plotly import express as xp


STATE = "state"


class NodeState(StrEnum):
    SUSCEPTIBLE = auto()
    INFECTIOUS = auto()
    REMOVED = auto()


Snapshot: TypeAlias = dict[int, NodeState]
Simulation: TypeAlias = list[Snapshot]


def get_infectious_nodes(graph: nx.Graph) -> list[int]:
    return [node for node, data in graph.nodes(data=True) if data[STATE] == NodeState.INFECTIOUS]


def get_susceptible_neighbours_of(node: int, graph: nx.Graph) -> list[int]:
    return [node for node in nx.neighbors(graph, node) if graph.nodes[node][STATE] == NodeState.SUSCEPTIBLE]


def init_as_susceptible(graph: nx.Graph) -> nx.Graph:
    nx.set_node_attributes(graph, NodeState.SUSCEPTIBLE, STATE)
    return graph


def spawn_infectious(graph: nx.Graph, node_id: int | None = None) -> nx.Graph:
    if node_id is None:
        node_id = randint(0, len(graph.nodes) - 1)
    graph.nodes[node_id][STATE] = NodeState.INFECTIOUS
    return graph


def step_forward(graph: nx.Graph, p: float) -> nx.Graph:
    next = graph.copy()

    for infectious in get_infectious_nodes(graph):
        for neighbour in get_susceptible_neighbours_of(infectious, graph):
            if uniform(0, 1) < p:
                next.nodes[neighbour][STATE] = NodeState.INFECTIOUS
        next.nodes[infectious][STATE] = NodeState.REMOVED

    return next


def take_snapshot(graph: nx.Graph) -> Snapshot:
    return nx.get_node_attributes(graph, STATE)


def simulate(graph: nx.Graph, p: float, max_steps: int, initial_infectious: int | None = None, shortcircuit: bool = False) -> Simulation:
    graph = graph.copy()
    graph = init_as_susceptible(graph)
    graph = spawn_infectious(graph, initial_infectious)

    simulation: Simulation = [take_snapshot(graph)]

    for _ in range(max_steps - 1):
        graph = step_forward(graph, p)
        simulation.append(take_snapshot(graph))

        if shortcircuit and not get_infectious_nodes(graph):
            break

    return simulation


def get_fraction_of_infected_nodes(simulation: Simulation) -> list[float]:
    return [
        len([1 for state in step.values() if state == NodeState.INFECTIOUS]) / len(step) for step in simulation
    ]


def get_average_fraction_of_infected_nodes(graph: nx.Graph, p: float, max_steps: int, num_runs: int, initial_infectious: int) -> NDArray:
    simulations = [simulate(graph=graph, p=p, max_steps=max_steps, initial_infectious=initial_infectious) for _ in range(num_runs)]
    fractions = np.array([get_fraction_of_infected_nodes(simulation) for simulation in simulations])
    return fractions.mean(axis=0)


def main():
    averages = get_average_fraction_of_infected_nodes(
        graph=nx.erdos_renyi_graph(100, 0.4),
        p=0.1,
        max_steps=10,
        num_runs=100,
        initial_infectious=0,
    )
    xp.line(y=averages).show()


if __name__ == "__main__":
    main()
