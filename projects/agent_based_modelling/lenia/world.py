from dataclasses import dataclass
from typing import Literal, Self

import numpy as np
from base import Array
from matplotlib import pyplot as plt
from scipy import ndimage

OrganismName = Literal[
    "aquarium",
    "fish",
    "geminium",
    "orbium",
]


@dataclass
class World:
    arr: Array

    def __post_init__(self):
        dims = self.arr.ndim
        if dims not in {2, 3}:
            raise ValueError("the array should be 2 or 3 dimensional")
        if dims == 2:
            self.arr = np.array([self.arr])

    def embed(self, other: Self, *, at: tuple[int, int] = (0, 0)) -> Self:
        x, y = at
        dx, dy = other.arr.shape[1:]
        self.arr[:, x : x + dx, y : y + dy] = other.arr
        return self

    def save(self, name: OrganismName):
        np.save(f"organisms/{name}.npy", self.arr)

    def show(self):
        fig, ax = plt.subplots(1, 1, constrained_layout=True)
        ax.imshow(np.dstack(self.arr))
        fig.show()

    @classmethod
    def load(cls, name: OrganismName) -> Self:
        return cls(np.load(f"organisms/{name}.npy"))

    @classmethod
    def empty(cls, shape: tuple[int, ...]) -> Self:
        return cls(arr=np.zeros(shape))

    @classmethod
    def uniform(cls, shape: tuple[int, ...]) -> Self:
        return cls(arr=np.random.uniform(size=shape))

    @property
    def flipped_horizontal(self) -> Self:
        return World(arr=np.flip(self.arr, axis=self.arr.ndim - 1))

    @property
    def flipped_vertical(self) -> Self:
        return World(arr=np.flip(self.arr, axis=self.arr.ndim - 2))

    @property
    def rotated(self) -> Self:
        return World(arr=np.rot90(self.arr, axes=(-1, -2)))

    def zoomed(self, scale: float, order: int = 0) -> Self:
        return World(arr=np.array([ndimage.zoom(arr, scale, order=order) for arr in self.arr]))
