import random
from dataclasses import dataclass

from tqdm import tqdm
from projects.agent_based_modelling.assignment_2.game_of_life import GameOfLife, GameOfLifeFactory
from IPython.display import Image
from matplotlib import animation, pyplot as plt


@dataclass
class PlotSubset:
    # define the plot bounds here, but allow the simulation to happen outside of them
    x_min: int | None = None
    x_max: int | None = None
    y_min: int | None = None
    y_max: int | None = None

    @property
    def x_slice(self) -> slice:
        return slice(self.x_min, self.x_max)

    @property
    def y_slice(self) -> slice:
        return slice(self.y_min, self.y_max)


def show(game: GameOfLife, subset: PlotSubset = PlotSubset()):
    plt.imshow(game[subset.y_slice, subset.x_slice], cmap=plt.cm.gray_r)  # type: ignore
    plt.show()


def animate(game: GameOfLife, filename: str, steps: int = 500, fps: int = 20, subset: PlotSubset = PlotSubset()) -> Image:
    fig, ax = plt.subplots(figsize=(8, 8), constrained_layout=True)
    ax.set_aspect("equal")

    img = ax.imshow(game[subset.y_slice, subset.x_slice], cmap=plt.cm.gray_r)  # type: ignore

    def update(_: int):
        game.step()
        img.set_data(game[subset.y_slice, subset.x_slice])

    def init():
        img.set_data(game[subset.y_slice, subset.x_slice])

    animation.FuncAnimation(
        fig=fig,
        func=update,  # type: ignore
        init_func=init,  # type: ignore
        frames=tqdm(range(steps)),
        cache_frame_data=False,
    ).save(
        filename=filename,
        writer=animation.PillowWriter(fps=fps),
    )
    plt.close()
    return Image(filename)


def single_glider_gun():
    game = (
        GameOfLifeFactory.empty((50, 50))
        .embed(GameOfLifeFactory.glider_gun(), (5, 0))
    )
    animate(game, "single_glider_gun_cyclic.gif", steps=500, fps=40)


def death_edges():
    game = (
        GameOfLifeFactory.empty((50, 50))
        .embed(GameOfLifeFactory.glider_gun(), (5, 5))
        .embed(GameOfLifeFactory.pentadecathlon().rotated, (40, 20))
    )
    game.death_edges = True
    animate(game, "death_edges.gif", steps=500, fps=40)


def spaceships():
    game = GameOfLifeFactory.empty()
    for _ in range(20):
        game.embed(GameOfLifeFactory.lightweight_spaceship(), (random.randint(0, 100), random.randint(0, 100)))

    animate(game, "fleet.gif", steps=500, fps=30)


if __name__ == "__main__":
    death_edges()
