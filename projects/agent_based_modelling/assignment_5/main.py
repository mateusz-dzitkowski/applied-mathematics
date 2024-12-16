from dataclasses import dataclass, field
from projects.agent_based_modelling.assignment_5.rule import Rule

import numpy as np
from scipy.ndimage import shift


@dataclass
class Automaton:
    rule: Rule
    arr: np.ndarray

    _arr_history: list[np.ndarray] = field(default_factory=list)

    def __post_init__(self):
        self.arr = arr.astype(int)
        self._arr_history.append(self.arr)

    def run(self, steps: int):
        print(self)
        for _ in range(steps):
            self.step()
            print(self)

    def step(self):
        self.arr = self.rule.step_function(
            p=shift(self.arr, 1, cval=False),
            q=self.arr,
            r=shift(self.arr, -1, cval=False),
        )
        self._arr_history.append(self.arr)

    def __str__(self) -> str:
        return "[" + "".join(["█" if bit else " " for bit in self.arr]) + "]"


if __name__ == "__main__":
    rule = Rule(number=30)

    size = 101

    arr = np.zeros(size)
    arr[size // 2] = 1

    automaton = Automaton(rule=rule, arr=arr)
    automaton.run(size // 2)
