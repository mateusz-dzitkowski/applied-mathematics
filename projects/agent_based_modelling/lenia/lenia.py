from functools import cached_property
from dataclasses import dataclass
from typing import Self, Callable
import numpy as np
from scipy.signal import convolve2d
from pathlib import Path
from matplotlib import pyplot as plt


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
    def from_func(cls, func: Func, radius_cells: int, radius_xy: float, midpoint: bool = False) -> Self:
        if midpoint:
            x, y = np.meshgrid(*np.ogrid[-radius_cells:radius_cells+1, -radius_cells:radius_cells+1])
        else:
            x, y = np.meshgrid(*np.ogrid[-radius_cells:radius_cells, -radius_cells:radius_cells])
        x, y = x / radius_xy, y / radius_xy
        r = np.sqrt(x**2 + y**2)
        return cls(arr=(r < 1) * func(r))

    @cached_property
    def fft(self) -> Array:
        return np.fft.fft2(np.fft.fftshift(self.arr / self.arr.sum()))

    def apply(self, arr: Array) -> Array:
        if arr.shape == self.arr.shape:  # if you set everything up nicely you will get a performance boost from fft
            return np.real(np.fft.ifft2(self.fft * np.fft.fft2(arr)))
        return convolve2d(arr, self.arr, mode="same", boundary="wrap")

    def show(self):
        plt.imshow(self.arr)
        plt.show()


class GrowthMapping:
    func: Func

    def __init__(self, func: Func):
        self.func = func

    def apply(self, arr: Array) -> Array:
        return self.func(arr)

    def show(self, x: Array):
        plt.plot(x, self.func(x))
        plt.show()


@dataclass
class World:
    arr: Array

    def embed(self, other: Self, at: tuple[int, int] = (0, 0)) -> Self:
        x, y = at
        dx, dy = other.arr.shape
        self.arr[x:x + dx, y:y + dy] = other.arr
        return self

    def save(self, path: Path | str):
        np.save(path, self.arr)

    @classmethod
    def load(cls, path: Path | str):
        return cls(np.load(path))

    @classmethod
    def new(cls, width: int, height: int):
        return cls(np.zeros((width, height)))

    @property
    def flipped_horizontal(self) -> Self:
        return World(arr=np.flip(self.arr, axis=1))

    @property
    def flipped_vertical(self) -> Self:
        return World(arr=np.flip(self.arr, axis=0))

    @property
    def rotated(self) -> Self:
        return World(arr=np.rot90(self.arr))


@dataclass
class Lenia:
    world: World
    kernel: Kernel
    growth_mapping: GrowthMapping
    dt: float

    def step(self):
        convolved = self.kernel.apply(self.world.arr)
        growth = self.growth_mapping.apply(convolved)
        self.world.arr[:, :] = np.clip(self.world.arr + self.dt*growth, 0, 1)

    def show(self):
        plt.imshow(self.world.arr)
        plt.show()

    @classmethod
    def game_of_life(cls, initial: World) -> Self:
        return cls(
            world=initial,
            kernel=Kernel.from_func(
                func=lambda x: x > 0,
                radius_cells=1,
                radius_xy=2,
                midpoint=True,
            ),
            growth_mapping=GrowthMapping(lambda x: h(x - 1) + h(x - 2) - 2 * h(x - 3) - 1),
            dt=1,
        )
