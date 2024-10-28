from io import StringIO
from pathlib import Path
from typing import Self

import numpy as np
from scipy.signal import convolve2d

TXT_ZERO = "."
TXT_ONE = "1"


class GameOfLife(np.matrix):
    death_edges: bool = False
    kernel: np.matrix = np.matrix("1 1 1; 1 0 1; 1 1 1")

    @classmethod
    def from_path(cls, path: Path) -> Self:
        return cls(path.read_text(encoding="utf-8").replace(TXT_ZERO, "0").replace(TXT_ONE, "1").replace("", " ").replace("\n", ";")).astype(bool)

    def step(self):
        neighbours = convolve2d(self, self.kernel, mode="same", boundary="wrap")
        self[:, :] = np.logical_or(
            np.logical_and(self, np.logical_or(neighbours == 2, neighbours == 3)),
            np.logical_and(~self, neighbours == 3),
        )
        if self.death_edges:
            self[[0, -1], :] = self[:, [0, -1]] = 0

    def embed(self, other: Self, at: tuple[int, int] = (0, 0)) -> Self:
        x, y = at
        dx, dy = other.shape
        self[x : x + dx, y : y + dy] = other
        return self.astype(bool)

    def save(self, path: Path):
        str_io = StringIO()
        np.savetxt(str_io, self, fmt="%d", delimiter="")
        path.write_text(str_io.getvalue().replace("0", TXT_ZERO).replace("1", TXT_ONE).rstrip("\n"))

    @property
    def flipped_horizontal(self) -> Self:
        return GameOfLife(np.flip(self, axis=1))

    @property
    def flipped_vertical(self) -> Self:
        return GameOfLife(np.flip(self, axis=0))

    @property
    def rotated(self) -> Self:
        return GameOfLife(np.rot90(self))

    @property
    def width(self) -> int:
        return self.shape[1]

    @property
    def height(self) -> int:
        return self.shape[0]


class GameOfLifeFactory:
    @staticmethod
    def empty(shape: tuple[int, int] = (100, 100)) -> GameOfLife:
        return GameOfLife(np.zeros(shape))

    @staticmethod
    def random(shape: tuple[int, int], p: float = 0.2) -> GameOfLife:
        return GameOfLife((np.random.uniform(size=shape) < p).astype(bool))  # type: ignore

    @staticmethod
    def from_schematic(schematic: str) -> GameOfLife:
        return GameOfLife.from_path(Path(__file__).parent / "schematics" / schematic)

    @classmethod
    def block(cls) -> GameOfLife:
        return cls.from_schematic("block")

    @classmethod
    def beehive(cls) -> GameOfLife:
        return cls.from_schematic("beehive")

    @classmethod
    def loaf(cls) -> GameOfLife:
        return cls.from_schematic("loaf")

    @classmethod
    def boat(cls) -> GameOfLife:
        return cls.from_schematic("boat")

    @classmethod
    def tub(cls) -> GameOfLife:
        return cls.from_schematic("tub")

    @classmethod
    def blinker(cls) -> GameOfLife:
        return cls.from_schematic("blinker")

    @classmethod
    def toad(cls) -> GameOfLife:
        return cls.from_schematic("toad")

    @classmethod
    def beacon(cls) -> GameOfLife:
        return cls.from_schematic("beacon")

    @classmethod
    def pulsar(cls) -> GameOfLife:
        return cls.from_schematic("pulsar")

    @classmethod
    def pentadecathlon(cls) -> GameOfLife:
        return cls.from_schematic("pentadecathlon")

    @classmethod
    def glider(cls) -> GameOfLife:
        return cls.from_schematic("glider")

    @classmethod
    def lightweight_spaceship(cls) -> GameOfLife:
        return cls.from_schematic("lightweight_spaceship")

    @classmethod
    def glider_gun(cls) -> GameOfLife:
        return cls.from_schematic("glider_gun")

    @classmethod
    def eater(cls) -> GameOfLife:
        return cls.from_schematic("eater")
