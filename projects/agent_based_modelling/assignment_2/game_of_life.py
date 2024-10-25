from io import StringIO
from pathlib import Path
from typing import Self

import numpy as np
from IPython.display import Image
from matplotlib import animation
from matplotlib import pyplot as plt
from scipy.signal import convolve2d

TXT_ZERO = "."
TXT_ONE = "1"


class GameOfLife(np.matrix):
    death_edges: bool = False

    @classmethod
    def from_path(cls, path: Path) -> Self:
        return cls(path.read_text(encoding="utf-8").replace(TXT_ZERO, "0").replace(TXT_ONE, "1").replace("", " ").replace("\n", ";")).astype(bool)

    def step(self):
        kernel = np.matrix("1 1 1; 1 0 1; 1 1 1")
        neighbours = convolve2d(self, kernel, mode="same", boundary="wrap")
        self[:, :] = np.logical_or(
            np.logical_and(self, np.logical_or(neighbours == 2, neighbours == 3)),
            np.logical_and(~self, neighbours == 3),
        )
        if self.death_edges:
            self[[0, -1], :] = self[:, [0, -1]] = 0

    def animate(self, filename: str, steps: int = 500, fps: int = 20) -> Image:
        fig, ax = plt.subplots(figsize=(8, 8), constrained_layout=True)
        ax.set_aspect("equal")
        ax.axis("off")

        img = ax.imshow(self, cmap=plt.cm.gray_r)  # type: ignore

        def update(_: int):
            self.step()
            img.set_data(self)

        def init():
            img.set_data(self)

        animation.FuncAnimation(
            fig=fig,
            func=update,  # type: ignore
            init_func=init,  # type: ignore
            frames=steps,
            cache_frame_data=False,
        ).save(
            filename=filename,
            writer=animation.PillowWriter(fps=fps),
        )
        plt.close()
        return Image(filename)

    def show(self):
        plt.imshow(self, cmap=plt.cm.gray_r)  # type: ignore
        plt.show()

    def embed(self, other: Self, at: tuple[int, int] = (0, 0)) -> Self:
        x, y = at
        dx, dy = other.shape
        self[x : x + dx, y : y + dy] = other
        return self.astype(bool)

    def save(self, path: Path):
        str_io = StringIO()
        np.savetxt(str_io, self, fmt="%d", delimiter="")
        path.write_text(str_io.getvalue().replace("0", TXT_ZERO).replace("1", TXT_ONE).rstrip("\n"))

    def flip_horizontal(self) -> Self:
        return GameOfLife(np.flip(self, axis=0))

    def flip_vertical(self) -> Self:
        return GameOfLife(np.flip(self, axis=1))


class GameOfLifeFactory:
    @staticmethod
    def empty(shape: tuple[int, int]) -> GameOfLife:
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


if __name__ == "__main__":
    game = (
        GameOfLifeFactory.empty((100, 100))
        .embed(GameOfLifeFactory.glider_gun(), (5, 5))
        .embed(GameOfLifeFactory.glider_gun().flip_vertical(), (5, 61))
    )
    game.animate("test.gif", 500)
