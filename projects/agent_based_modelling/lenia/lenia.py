from dataclasses import dataclass
from typing import Self

import numpy as np

from base import h
from world import World
from mapping import Mapping, Map, Growth
from kernel import Kernel


@dataclass
class Lenia:
    world: World
    mapping: Mapping
    dt: float

    def step(self):
        self.world.arr[:, :] = np.clip(self.world.arr + self.dt * self.mapping.apply(self.world.arr), 0, 1)

    @classmethod
    def game_of_life(cls, initial: World) -> Self:
        return cls(
            world=initial,
            mapping=Mapping(
                maps=[
                    Map(
                        kernel=Kernel.from_func(
                            func=lambda x: x > 0,
                            radius_cells=1,
                            radius_xy=2,
                            midpoint=True,
                        ),
                        growth=Growth(lambda x: h(x - 1) + h(x - 2) - 2 * h(x - 3) - 1),
                    ),
                ],
            ),
            dt=1,
        )
