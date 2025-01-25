from enum import IntEnum
from dataclasses import dataclass, field
from random import sample, uniform
from typing import Self

import numpy as np
import networkx as nx


class AdoptionState(IntEnum):
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
    states: dict[int, AdoptionState] = field(default_factory=dict)
    adoption_history: np.ndarray = field(default_factory=lambda: np.array([]))

    def __post_init__(self):
        self.states = {n: AdoptionState.NOT_ADOPTED for n in self.graph}

        for node in sample(list(self.graph), self.initial_adoptions):
            self.states[node] = AdoptionState.ADOPTED

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
        # TODO: does "select an agent i randomly" allow for duplicates? Current implementation says NO
        for node in sample(list(self.graph), len(self.graph)):
            if self.states[node] == AdoptionState.ADOPTED:
                continue

            if uniform(0, 1) < self.params.innovation + self.params.imitation * self.fraction_of_adopted_neighbours(node):
                self.states[node] = AdoptionState.ADOPTED

        self.save_adoption()

    def fraction_of_adopted_neighbours(self, node: int) -> float:
        return len([1 for neighbor in self.graph[node] if self.is_adopted(neighbor)]) / len(self.graph)

    def fraction_of_adopted(self) -> float:
        return len([1 for node in self.graph if self.is_adopted(node)]) / len(self.graph)

    def is_adopted(self, node: int) -> bool:
        return self.states[node] == AdoptionState.ADOPTED

    def save_adoption(self):
        self.adoption_history = np.append(self.adoption_history, self.fraction_of_adopted())
