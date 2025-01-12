from dataclasses import dataclass
from functools import cached_property
from typing import Callable

import numpy as np
from matplotlib.axes import Axes
from scipy.optimize import minimize


@dataclass(frozen=True)
class Plant:
    capacity: float
    coefficient: float


@dataclass(frozen=True)
class Problem:
    beets_per_day: int
    num_days: int
    plants: list[Plant]

    @cached_property
    def num_plants(self) -> int:
        return len(self.plants)

    @cached_property
    def days(self) -> list[int]:
        return list(range(self.num_days))

    @cached_property
    def total_demand(self) -> float:
        return self.num_days * self.beets_per_day

    def v_to_x(self, v: np.ndarray) -> np.ndarray:
        return v.reshape(self.num_days, self.num_plants)

    @cached_property
    def loss_function(self) -> Callable[[np.ndarray], float]:
        def inner(v: np.ndarray) -> float:
            x = self.v_to_x(v)
            t = np.zeros((self.num_days + 1, self.num_plants))
            loss = 0
            for j, plant in enumerate(self.plants):
                for i in self.days:
                    t[i + 1, j] = x[: i + 1, j].sum() / plant.capacity
                    loss += plant.coefficient * x[i, j] * (t[i, j] + t[i + 1, j] - 2 * (i + 1)) / 2
            return loss

        return inner

    @cached_property
    def constraint(self) -> Callable[[np.ndarray], list[float]]:
        def inner(v: np.ndarray) -> list[float]:
            # every day, all beets have to be distributed
            return self.v_to_x(v).sum(axis=1) - self.beets_per_day

        return inner

    @cached_property
    def bounds(self) -> list[tuple[float, None]]:
        # number of beets assigned to plant j at day i has to be nonnegative
        return [(0, None) for _ in self.days for _ in self.plants]

    @cached_property
    def solution(self) -> np.ndarray:
        result = minimize(
            fun=self.loss_function,
            x0=np.ones(self.num_days * self.num_plants),
            method="SLSQP",
            bounds=self.bounds,
            constraints={
                "type": "eq",
                "fun": self.constraint,
            },
        )
        return self.v_to_x(result.x)

    def plot_solution(self, ax: Axes):
        for i, x in enumerate(self.solution.T):
            ax.plot(x, "-*", label=f"Plant {i + 1}")
