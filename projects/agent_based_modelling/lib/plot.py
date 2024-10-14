from matplotlib import pyplot as plt, animation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from IPython.display import Image
from tempfile import NamedTemporaryFile

from typing import TypeVar, Callable

from .model import Model


T = TypeVar("T")


def animate(model: Model, filename: str, agent_color_func: Callable[[T], str]):
    fig, ax = _prepare_fig(model)

    x, y, c = zip(*[(pos.x, pos.y, agent_color_func(agent)) for pos, agent in model.pos_agents])
    scatter = ax.scatter(
        x=x,
        y=y,
        color=c,
        marker="s",
        s=_scaling_factor(ax),
        edgecolors="black",
    )

    def update(_model: Model):
        scatter.set_facecolor([agent_color_func(agent) for agent in _model.agents])

    def frames():
        while model.running:
            yield model
            model.step()

    animation.FuncAnimation(
        fig=fig,
        func=update,  # type: ignore
        frames=frames,
        cache_frame_data=False,
    ).save(
        filename=filename,
        writer=animation.PillowWriter(fps=10, bitrate=2400),
    )
    plt.close()


def animate_show(model: Model, agent_color_func: Callable[[T], str]) -> Image:
    filename = f"{NamedTemporaryFile().name}.gif"
    animate(model, filename, agent_color_func)
    return Image(filename)


def _plot(ax: Axes, model: Model, agent_color_func: Callable[[T], str]):
    x, y, c = zip(*[(pos.x, pos.y, agent_color_func(agent)) for pos, agent in model.pos_agents])
    ax.scatter(
        x=x,
        y=y,
        color=c,
        marker="s",
        s=_scaling_factor(ax),
    )


def _scaling_factor(ax: Axes) -> float:
    trans = ax.transData.transform
    x0, _ = trans((0, 0))
    x1, _ = trans((1, 1))
    return (x1 - x0)**2 / 2


def _prepare_fig(model: Model) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_aspect("equal")
    ax.set_xlim([-0.5, model.grid.width - 0.5])
    ax.set_ylim([-0.5, model.grid.height - 0.5])
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    return fig, ax
