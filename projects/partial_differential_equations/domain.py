from dataclasses import dataclass
from functools import cached_property

import numpy as np
from nptyping import NDArray


@dataclass
class DomainShape:
    t: int
    xy: tuple[int, int]


@dataclass
class Domain:
    t: NDArray
    x: NDArray
    y: NDArray

    @classmethod
    def new(cls, shape: tuple[int, int, int], max_vals: tuple[float, float, float] = (1, 1, 1)) -> "Domain":
        # Assume that t, x, and y range from 0 to t_max, x_max, y_max
        x, y = np.meshgrid(
            np.linspace(0, max_vals[1], shape[1]),
            np.linspace(0, max_vals[2], shape[2]),
        )
        return cls(
            t=np.linspace(0, max_vals[0], shape[0]),
            x=x,
            y=y,
        )

    @cached_property
    def dt(self) -> float:
        return np.diff(self.t)[0]  # type: ignore

    @cached_property
    def dx(self) -> float:
        return np.diff(self.x, axis=1)[0, 0]  # type: ignore

    @cached_property
    def dy(self) -> float:
        return np.diff(self.y, axis=0)[0, 0]  # type: ignore

    @cached_property
    def diff(self) -> tuple[float, float, float]:
        return self.dt, self.dx, self.dy

    @cached_property
    def shape(self) -> DomainShape:
        # shape of self.x and self.y is the same due to np.meshgrid
        return DomainShape(
            t=self.t.shape[0],
            xy=(self.x.shape[0], self.x.shape[1]),
        )
