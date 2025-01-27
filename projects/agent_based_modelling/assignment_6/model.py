from dataclasses import dataclass, field
from random import sample, uniform, choice
from typing import Self

import numpy as np
import networkx as nx


STATE = "state"
NOT_ADOPTED = 0
ADOPTED = 1


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
    adoption_history: np.ndarray = field(default_factory=lambda: np.array([]))

    def __post_init__(self):
        nx.set_node_attributes(self.graph, NOT_ADOPTED, STATE)  # type: ignore

        for node in sample(list(self.graph), self.initial_adoptions):
            self.graph.nodes[node][STATE] = ADOPTED

        self.save_adoption()

    def run(self) -> Self:
        if self.fraction_of_adopted() == 0 and self.params.innovation == 0:
            self.save_adoption()
            return self

        while any([not self.is_adopted(node) for node in self.graph]):
            self.step()

        return self

    def step(self):
        self.current_step += 1
        for _ in range(len(self.graph)):
            node = choice(list(self.graph.nodes))
            if self.is_adopted(node):
                continue

            if uniform(0, 1) < self.params.innovation + self.params.imitation * self.fraction_of_adopted_neighbours(node):
                self.set_adopted(node)

        self.save_adoption()

    def fraction_of_adopted_neighbours(self, node) -> float:
        return len([1 for neighbor in self.graph[node] if self.is_adopted(neighbor)]) / len(self.graph)

    def fraction_of_adopted(self) -> float:
        return len([1 for node in self.graph if self.is_adopted(node)]) / len(self.graph)

    def set_adopted(self, node):
        self.graph.nodes[node][STATE] = ADOPTED

    def is_adopted(self, node) -> bool:
        return self.graph.nodes[node][STATE] == ADOPTED

    def save_adoption(self):
        self.adoption_history = np.append(self.adoption_history, self.fraction_of_adopted())
