from enum import Enum
from random import choice, uniform
from statistics import mean
from typing import Callable, Sequence, Iterable

import networkx as nx


QPanel = Callable[[nx.Graph, int], Sequence[int]]


OPINION = "opinion"


class Opinion(Enum):
    UP = 1
    DOWN = -1

    @classmethod
    def random(cls) -> "Opinion":
        return choice((cls.UP, cls.DOWN))


def all_equal(x: Sequence[Opinion]) -> Opinion | None:
    # return the opinion if all opinions in x are the same, otherwise return None
    first = x[0]
    if all(first == item for item in x):
        return first
    return None


class Network:
    graph: nx.Graph
    q_panel: QPanel
    p: float
    epsilon: float
    coin_weight: float

    def __init__(self, graph: nx.Graph, q_panel: QPanel, p: float, epsilon: float = 0, coin_weight: float = 0.5):
        assert 0 <= p <= 1
        assert 0 <= epsilon <= 1
        assert 0 <= coin_weight <= 1

        nx.set_node_attributes(graph, {node: Opinion.UP for node in graph.nodes}, OPINION)

        self.graph = graph
        self.q_panel = q_panel
        self.p = p
        self.epsilon = epsilon
        self.coin_weight = coin_weight

    def flip_opinion(self, spinson: int):
        opinion = self.graph.nodes[spinson][OPINION]
        if opinion == Opinion.DOWN:
            self.graph.nodes[spinson][OPINION] = Opinion.UP
        elif opinion == Opinion.UP:
            self.graph.nodes[spinson][OPINION] = Opinion.DOWN

    @property
    def epsilon_coin_flip(self) -> bool:
        return uniform(0, 1) < self.epsilon

    @property
    def coin_flip(self) -> bool:
        return uniform(0, 1) < self.coin_weight

    @property
    def acts_independently(self) -> bool:
        return uniform(0, 1) < self.p

    def q_panel_unanimous(self, spinson: int) -> Opinion | None:
        return all_equal([self.graph.nodes[spinson][OPINION] for spinson in self.q_panel(self.graph, spinson)])

    def step(self):
        for _ in self.graph.nodes:
            spinson = choice(list(self.graph.nodes))
            if self.acts_independently and self.coin_flip:
                self.flip_opinion(spinson)
            else:
                if opinion := self.q_panel_unanimous(spinson):
                    self.graph.nodes[spinson][OPINION] = opinion
                elif self.epsilon_coin_flip:
                    self.flip_opinion(spinson)

    def simulate(self, steps: int = 1000) -> Iterable[float]:
        for _ in range(steps):
            self.step()
            yield self.magnetization

    @property
    def opinions_as_int(self) -> list[int]:
        return [self.graph.nodes[node][OPINION].value for node in self.graph.nodes]

    @property
    def magnetization(self) -> float:
        return abs(mean(self.opinions_as_int))
