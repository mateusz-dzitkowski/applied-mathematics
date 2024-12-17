from dataclasses import dataclass, field
from enum import Enum
from matplotlib import pyplot as plt

import numpy as np
from matplotlib.axes import Axes

from projects.agent_based_modelling.assignment_5.rule import Rule


class StartPosition(Enum):
    DOT = 0
    RANDOM = 1


@dataclass
class Automaton:
    rule: Rule
    size: int
    run_length: int
    start_position: StartPosition

    _arr: np.ndarray = field(default_factory=lambda: np.array([]))
    _arr_history: np.ndarray = field(default_factory=lambda: np.array([]))

    def __post_init__(self):
        match self.start_position:
            case StartPosition.DOT:
                self._arr = np.zeros(self.size)
                self._arr[self.size // 2] = 1
            case StartPosition.RANDOM:
                self._arr = np.random.randint(low=0, high=2, size=self.size)

        self._arr = self._arr.astype(int)
        self._arr = np.concatenate([np.array([0] * self.run_length), self._arr, np.array([0] * self.run_length)])
        self._arr_history = np.array([self._arr])

    def run(self):
        for _ in range(self.run_length):
            self.step()

    def step(self):
        self._arr = self.rule.step_function(self._arr)
        self._arr_history = np.vstack([self._arr_history, self._arr])

    def plot(self, ax: Axes):
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(f"rule {self.rule.number}")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(self._arr_history[:, self.run_length : -self.run_length], cmap=plt.cm.gray_r)  # type: ignore
