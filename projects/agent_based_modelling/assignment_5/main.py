from dataclasses import dataclass, field
from enum import Enum

import numpy as np

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
    _arr_history: list[np.ndarray] = field(default_factory=list)

    def __post_init__(self):
        match self.start_position:
            case StartPosition.DOT:
                self._arr = np.zeros(self.size)
                self._arr[self.size // 2] = 1
            case StartPosition.RANDOM:
                self._arr = np.random.randint(low=0, high=2, size=self.size)

        self._arr = self._arr.astype(int)
        self._arr = np.concatenate([np.array([0] * self.run_length), self._arr, np.array([0] * self.run_length)])
        self._arr_history.append(self._arr)

    def run(self):
        print(self)
        for _ in range(self.run_length):
            self.step()
            print(self)

    def step(self):
        self._arr = self.rule.step_function(self._arr)
        self._arr_history.append(self._arr)

    def __str__(self) -> str:
        return "[" + "".join(["█" if bit else " " for bit in self._arr[self.run_length : -self.run_length]]) + "]"


if __name__ == "__main__":
    size = 201
    arr = np.zeros(size)
    arr[size // 2] = 1

    automaton = Automaton(
        rule=Rule(number=161),
        size=200,
        run_length=100,
        start_position=StartPosition.RANDOM,
    )
    automaton.run()
