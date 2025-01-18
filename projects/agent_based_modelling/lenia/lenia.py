from dataclasses import dataclass
from typing import Self, Callable
import numpy as np
from scipy.signal import convolve2d


Array = np.ndarray
Func = Callable[[Array], Array]


def bell(m: float, s: float) -> Func:
    def inner(x: Array) -> Array:
        return np.exp(-0.5*((x-m)/s)**2)
    return inner


def h(x: Array) -> Array:
    return np.heaviside(x, 0)


@dataclass
class Kernel:
    arr: Array

    @classmethod
    def from_func(cls, func: Func, radius_cells: int, radius_xy: float) -> Self:
        x, y = np.meshgrid(*np.ogrid[-radius_cells:radius_cells+1, -radius_cells:radius_cells+1])
        x, y = x / radius_xy, y / radius_xy
        r = np.sqrt(x**2 + y**2)
        return cls(arr=(r < 1) * func(r))

    def apply(self, arr: Array) -> Array:
        return convolve2d(arr, self.arr, mode="same", boundary="wrap")


class GrowthMapping:
    func: Func

    def __init__(self, func: Func):
        self.func = func

    def apply(self, arr: Array) -> Array:
        return self.func(arr)


@dataclass
class Lenia:
    arr: Array
    kernel: Kernel
    growth_mapping: GrowthMapping
    dt: float

    def step(self):
        convolved = self.kernel.apply(self.arr)
        growth = self.growth_mapping.apply(convolved)
        self.arr[:, :] = np.clip(self.arr + self.dt*growth, 0, 1)

    @classmethod
    def game_of_life(cls, initial: Array) -> Self:
        return cls(
            arr=initial,
            kernel=Kernel.from_func(
                func=lambda x: x > 0,
                radius_cells=1,
                radius_xy=2,
            ),
            growth_mapping=GrowthMapping(lambda x: h(x - 1) + h(x - 2) - 2 * h(x - 3) - 1),
            dt=1,
        )
