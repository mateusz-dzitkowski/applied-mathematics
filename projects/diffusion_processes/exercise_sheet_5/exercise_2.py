from enum import StrEnum, auto
from random import randint, uniform

import networkx as nx


STATE = "state"


class NodeState(StrEnum):
    SUSCEPTIBLE = auto()
    INFECTIOUS = auto()
    REMOVED = auto()


def get_infectious_nodes(graph: nx.Graph) -> list[int]:
    return [node for node, data in graph.nodes(data=True) if data[STATE] == NodeState.INFECTIOUS]


def get_susceptible_neighbours_of(node: int, graph: nx.Graph) -> list[int]:
    return [node for node in nx.neighbors(graph, node) if graph.nodes[node][STATE] == NodeState.SUSCEPTIBLE]


def step_forward(graph: nx.Graph, p: float) -> nx.Graph:
    next = graph.copy()

    for infectious in get_infectious_nodes(graph):
        for neighbour in get_susceptible_neighbours_of(infectious, graph):
            if uniform(0, 1) < p:
                next.nodes[neighbour][STATE] = NodeState.INFECTIOUS
        next.nodes[infectious][STATE] = NodeState.REMOVED

    return next


def init_as_susceptible(graph: nx.Graph) -> nx.Graph:
    nx.set_node_attributes(graph, NodeState.SUSCEPTIBLE, STATE)
    return graph


def spawn_infectious(graph: nx.Graph, node_id: int | None = None) -> nx.Graph:
    if node_id is None:
        node_id = randint(0, len(graph.nodes) - 1)
    graph.nodes[node_id][STATE] = NodeState.INFECTIOUS
    return graph


def main():
    g = nx.erdos_renyi_graph(3, 0.8)
    g = init_as_susceptible(g)
    g = spawn_infectious(g)

    h = step_forward(g, 0.5)
    i = step_forward(h, 0.5)

    print(nx.get_node_attributes(g, STATE))
    print(nx.get_node_attributes(h, STATE))
    print(nx.get_node_attributes(i, STATE))


if __name__ == "__main__":
    main()
