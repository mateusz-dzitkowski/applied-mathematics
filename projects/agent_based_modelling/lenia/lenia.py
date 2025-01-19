from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Callable, Self

import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import convolve2d

Array = np.ndarray
Func = Callable[[Array], Array]


def bell(m: float, s: float) -> Func:
    def inner(x: Array) -> Array:
        return np.exp(-0.5 * ((x - m) / s) ** 2)

    return inner


def h(x: Array) -> Array:
    return np.heaviside(x, 0)


@dataclass
class Kernel:
    arr: Array

    @classmethod
    def from_func(cls, func: Func, radius_cells: int, radius_xy: float, midpoint: bool = False) -> Self:
        if midpoint:
            x, y = np.meshgrid(*np.ogrid[-radius_cells : radius_cells + 1, -radius_cells : radius_cells + 1])
        else:
            x, y = np.meshgrid(*np.ogrid[-radius_cells:radius_cells, -radius_cells:radius_cells])
        x, y = x / radius_xy, y / radius_xy
        r = np.sqrt(x**2 + y**2)
        return cls(arr=func(r))

    @cached_property
    def fft(self) -> Array:
        print("using fft to compute the convolution")
        return np.fft.fft2(np.fft.fftshift(self.arr / self.arr.sum()))

    def apply(self, arr: Array) -> Array:
        if arr.shape == self.arr.shape:  # if you set everything up nicely you will get a performance boost from fft
            return np.real(np.fft.ifft2(self.fft * np.fft.fft2(arr)))
        return convolve2d(arr, self.arr, mode="same", boundary="wrap")


class Growth:
    func: Func

    def __init__(self, func: Func):
        self.func = func

    def apply(self, arr: Array) -> Array:
        return self.func(arr)


@dataclass
class Map:
    kernel: Kernel
    growth: Growth


@dataclass
class Mapping:
    maps: list[Map]

    def apply(self, arr: Array) -> Array:
        convolved = [_map.kernel.apply(arr) for _map in self.maps]
        growth = np.asarray([_map.growth.apply(conv) for conv, _map in zip(convolved, self.maps)])
        return growth.mean(axis=0)

    def show(self):
        fig, (ax1, ax2, ax3) = plt.subplots(
            nrows=1,
            ncols=3,
            figsize=(14, 3),
            constrained_layout=True,
            gridspec_kw={"width_ratios": [1, 2, 2]},
        )
        arrays = np.asarray([_map.kernel.arr for _map in self.maps])

        ax1.imshow(np.dstack(arrays), cmap="viridis", interpolation="nearest", vmin=0)
        ax1.set_title("kernel matrix")

        ax2.plot(arrays[:, arrays.shape[1] // 2, :].T)
        ax2.set_title("kernel cross section")

        x = np.linspace(0, 1, 1000)
        g = np.asarray([_map.growth.apply(x) for _map in self.maps]).T
        ax3.plot(x, g)
        ax3.axhline(y=0, color="grey", linestyle="dotted")
        ax3.set_title("growth mapping")

        plt.show()


@dataclass
class World:
    arr: Array

    def embed(self, other: Self, *, at: tuple[int, int] = (0, 0)) -> Self:
        x, y = at
        dx, dy = other.arr.shape
        self.arr[x : x + dx, y : y + dy] = other.arr
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
