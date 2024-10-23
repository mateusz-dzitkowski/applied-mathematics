from pathlib import Path
from typing import Literal, Self

import numpy as np
from IPython.display import Image
from matplotlib import animation
from matplotlib import pyplot as plt
from scipy.signal import convolve2d

Boundary = Literal["fill", "wrap", "symm"]


class GameOfLife(np.matrix):
    @classmethod
    def from_path(cls, path: Path) -> Self:
        return cls(path.read_text(encoding="utf-8").replace(".", "0").replace("", " ").replace("\n", ";")).astype(bool)

    @classmethod
    def empty(cls, shape: tuple[int, int]) -> Self:
        return cls(np.zeros(shape))

    @classmethod
    def random(cls, shape: tuple[int, int], p: float = 0.2) -> Self:
        return cls((np.random.uniform(size=shape) < p).astype(bool))  # type: ignore

    def step(self, boundary: Boundary = "wrap"):
        kernel = np.matrix("1 1 1; 1 0 1; 1 1 1")
        neighbours = convolve2d(self, kernel, mode="same", boundary=boundary)
        self[:, :] = np.logical_or(
            np.logical_and(self, np.logical_or(neighbours == 2, neighbours == 3)),
            np.logical_and(~self, neighbours == 3),
        )

    def animate_show(self, filename: str, boundary: Boundary = "wrap", steps: int = 500, fps: int = 20) -> Image:
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect("equal")

        img = ax.imshow(self, cmap=plt.cm.gray_r)

        def update(_: int):
            self.step(boundary=boundary)
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
        plt.imshow(self, cmap=plt.cm.gray_r)
        plt.show()

    def embed(self, other: Self, at: tuple[int, int] = (0, 0)) -> Self:
        x, y = at
        dx, dy = other.shape
        self[x : x + dx, y : y + dy] = other
        return self.astype(bool)


class GameOfLifeFactory:
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

    @staticmethod
    def from_schematic(schematic: str) -> GameOfLife:
        return GameOfLife.from_path(Path(__file__).parent / "schematics" / schematic)


if __name__ == "__main__":
    game = (
        GameOfLife.random((50, 50), 0.01)
        .embed(GameOfLifeFactory.glider(), (0, 0))
        .embed(GameOfLifeFactory.lightweight_spaceship(), (10, 0))
        .embed(GameOfLifeFactory.loaf(), (20, 0))
    )
    game.animate_show("test.gif")
