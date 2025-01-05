from dataclasses import dataclass
from functools import cached_property
from typing import Self

import cvxpy as cp


@dataclass
class Plant:
    capacity: float
    coefficient: float


@dataclass
class Problem:
    beets_per_day: int
    days_beets_delivered: int
    plants: list[Plant]

    @classmethod
    def main_problem(cls) -> Self:
        return cls(
            beets_per_day=800,
            days_beets_delivered=20,
            plants=[
                Plant(
                    capacity=220,
                    coefficient=0.00006,
                ),
                Plant(
                    capacity=160,
                    coefficient=0.00002,
                ),
                Plant(
                    capacity=180,
                    coefficient=0.00003,
                ),
            ],
        )

    @cached_property
    def num_plants(self) -> int:
        return len(self.plants)

    @cached_property
    def x(self) -> cp.Variable:
        return cp.Variable((self.days_beets_delivered, self.num_plants))

    @cached_property
    def objective(self) -> cp.Expression:
        objective = 0

        for j, plant in enumerate(self.plants):
            for i in range(self.days_beets_delivered):
                processing_time = cp.sum(self.x[:i, j]) / plant.capacity
                objective += plant.coefficient * self.x[i, j] * (processing_time + processing_time - 2*(i+1))

        return objective

    @cached_property
    def constraints(self) -> list[cp.Constraint]:
        constraints = []

        for i in range(self.days_beets_delivered):
            constraints.append(cp.sum(self.x[i, :]) == self.beets_per_day)

        for j, plant in enumerate(self.plants):
            for i in range(self.days_beets_delivered):
                constraints.append(self.x[i, j] <= plant.capacity)

        constraints.append(self.x >= 0)

        return constraints  # type: ignore

    def solve(self) -> cp.Variable:
        problem = cp.Problem(
            objective=cp.Minimize(self.objective),
            constraints=self.constraints,
        )
        print(problem)
        problem.solve()
        return self.x
