from dataclasses import dataclass, field
from random import sample, random, choice
from typing import Self

import numpy as np
import networkx as nx


@dataclass
class Params:
    innovation: float
    imitation: float


@dataclass
class Model:
    params: Params
    graph: nx.Graph
    initial_adoptions: int
    current_step: int = 0

    _adopted: set = field(default_factory=set)
    _adoption_history: list = field(default_factory=list)
    _nodes: list = field(default_factory=list)
    _num_nodes: int = 0

    def __post_init__(self):
        self._nodes = list(self.graph)
        self._num_nodes = len(self._nodes)

        for node in sample(self._nodes, self.initial_adoptions):
            self.set_adopted(node)

        self.save_adoption()

    def run(self) -> Self:
        if self.fraction_of_adopted() == 0 and self.params.innovation == 0:
            self.save_adoption()
            return self

        while len(self._adopted) < self._num_nodes:
            self.step()

        return self

    def step(self):
        self.current_step += 1
        for _ in range(self._num_nodes):
            node = choice(self._nodes)
            if self.is_adopted(node):
                continue

            if random() < self.params.innovation + self.params.imitation * self.fraction_of_adopted_neighbours(node):
                self.set_adopted(node)

        self.save_adoption()

    def fraction_of_adopted_neighbours(self, node) -> float:
        return len(set(self.graph[node]) & self._adopted) / self._num_nodes

    def fraction_of_adopted(self) -> float:
        return len(self._adopted) / self._num_nodes

    def set_adopted(self, node):
        self._adopted.add(node)

    def is_adopted(self, node) -> bool:
        return node in self._adopted

    def save_adoption(self):
        self._adoption_history.append(self.fraction_of_adopted())

    @property
    def adoption_history(self) -> np.ndarray:
        return np.array(self._adoption_history)
