from dataclasses import dataclass
from pathlib import Path
from typing import Self

import numpy as np

from base import Array


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