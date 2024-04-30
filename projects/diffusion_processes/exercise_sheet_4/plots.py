import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib import pyplot as plt
from matplotlib import animation
from nptyping import NDArray


AX_OVERHEAD = 2
FIG_SIZE = (10, 10)
NUM_STEPS = 200
FPS = 30
BITRATE = -1
LINE_WIDTH = 0.5


def animate_random_walk(x: NDArray, y: NDArray):
    fig, ax = _prepare_fig(x, y)

    ax.scatter([0], [0], color="green")  # color the start point
    lines, = ax.plot([0], [0], linewidth=LINE_WIDTH)
    scat_current = ax.scatter([0], [0], color="red")

    step = int(x.size) // NUM_STEPS
    def animate(n: int):
        _n = step * n
        lines.set_xdata(x[:_n+1])
        lines.set_ydata(y[:_n+1])
        scat_current.set_offsets([x[_n], y[_n]])
        return lines

    print("saving the animation...")
    animation.FuncAnimation(
        fig=fig,
        func=animate,  # type: ignore
        frames=len(x) // step,
    ).save(
        filename="animation.gif",
        writer=animation.PillowWriter(fps=FPS, bitrate=BITRATE),
    )


def plot_random_walk(x: NDArray, y: NDArray):
    fig, ax = _prepare_fig(x, y)
    ax.plot(x, y, linewidth=LINE_WIDTH)
    ax.scatter(x[0], y[0], color="green")
    ax.scatter(x[-1], y[-1], color="red")
    plt.show()


def plot_histograms(x: NDArray, y: NDArray):
    a = np.sum(np.where(x > 0, 1, 0), axis=0) / x.shape[0]
    b = np.sum(np.where(np.logical_and(x > 0, y > 0), 1, 0), axis=0) / x.shape[0]

    fig, (ax_1, ax_2) = plt.subplots(2, 1, figsize=FIG_SIZE)

    ax_1.set_title(f"<A> = {a.mean()}")
    ax_2.set_title(f"<B> = {b.mean()}")

    ax_1.hist(a, bins=100, density=True)
    ax_2.hist(b, bins=100, density=True)
    plt.show()


def _prepare_fig(x: NDArray, y: NDArray) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    ax.set_aspect("equal")
    ax.grid()
    ax.set_xlim([x.min() - AX_OVERHEAD, x.max() + AX_OVERHEAD])
    ax.set_ylim([y.min() - AX_OVERHEAD, y.max() + AX_OVERHEAD])

    return fig, ax
