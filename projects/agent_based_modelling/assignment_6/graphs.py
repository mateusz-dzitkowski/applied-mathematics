from random import choice, uniform
from itertools import product

import networkx as nx


ONE_SIDE_ADJ = [
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
]


def lattice_with_diagonals(m: int, n: int, beta: float) -> nx.Graph:
    def add(left: tuple[int, int], right: tuple[int, int]):
        return (left[0] + right[0]) % m, (left[1] + right[1]) % n

    g = nx.Graph()
    all_nodes = set(product(range(m), range(n)))
    g.add_nodes_from(all_nodes)

    for node, adj in product(g, ONE_SIDE_ADJ):
        g.add_edge(node, add(node, adj))

    for node, adj in product(g, ONE_SIDE_ADJ):
        if uniform(0, 1) < beta:
            g.remove_edge(node, add(node, adj))
            candidates = all_nodes - set(g.neighbors(node)) - {node}
            target = choice(list(candidates))
            g.add_edge(node, target)

    return g
