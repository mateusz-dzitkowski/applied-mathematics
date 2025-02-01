from dataclasses import dataclass
from typing import Self, Literal

from matplotlib import pyplot as plt
import numpy as np
from scipy import ndimage

from base import Array


OrganismName = Literal["fish", "orbium", "geminium"]


@dataclass
class World:
    arr: Array

    def embed(self, other: Self, *, at: tuple[int, int] = (0, 0)) -> Self:
        x, y = at
        dx, dy = other.arr.shape
        self.arr[x : x + dx, y : y + dy] = other.arr
        return self

    def save(self, name: OrganismName):
        np.save(f"organisms/{name}.npy", self.arr)

    def show(self):
        fig, ax = plt.subplots(1, 1, constrained_layout=True)
        ax.imshow(self.arr)
        fig.show()

    @classmethod
    def load(cls, name: OrganismName):
        return cls(np.load(f"organisms/{name}.npy"))

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

    def zoom(self, scale: float, order: int = 0) -> Self:
        return World(arr=ndimage.zoom(self.arr, scale, order=order))
