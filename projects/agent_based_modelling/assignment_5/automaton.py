from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property, reduce

import numpy as np
from matplotlib import pyplot as plt
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
        self._arr = np.array([np.concatenate([np.array([0] * self.run_length), self._arr, np.array([0] * self.run_length)])]).astype(int)
        self._arr = reduce(lambda a, _: np.vstack([self._arr[-1, :], self.rule.step_function(a)]), [0] * self.run_length, self._arr)

    @cached_property
    def arr_history(self) -> np.ndarray:
        print(self._arr)
        return self._arr[:, self.run_length : -self.run_length]

    def plot_evolution(self, ax: Axes):
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(self.arr_history, cmap=plt.cm.gray_r)  # type: ignore

    def plot_timeseries(self, ax: Axes):
        number_of_ones = self.arr_history.sum(axis=1)
        activity = np.vstack([np.full(self.arr_history[0].shape[0], np.nan), np.abs(np.diff(self.arr_history, axis=0))]).sum(axis=1)
        bonds = np.abs(np.diff(self.arr_history, axis=1)).sum(axis=1)

        ax.plot(number_of_ones, label="number of ones")
        ax.plot(activity, label="activity")
        ax.plot(bonds, label="bonds")
        ax.legend()
