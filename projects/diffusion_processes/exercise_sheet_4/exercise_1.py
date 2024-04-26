from matplotlib import pyplot as plt
from matplotlib import animation
from nptyping import NDArray
import numpy as np
import plotly.express as ex


def animate_random_walk(x: NDArray, y: NDArray):
    fig, ax = plt.subplots()
    ax.set_xlim([x.min() - 2, x.max() + 2])
    ax.set_ylim([y.min() - 2, y.max() + 2])

    lines, = ax.plot(x[0], y[0])
    scat = ax.scatter([0], [0])

    def animate(n: int):
        lines.set_xdata(x[:n+1])
        lines.set_ydata(y[:n+1])
        scat.set_offsets([x[n], y[n]])
        return lines

    print("saving the animation...")
    animation.FuncAnimation(
        fig=fig,
        func=animate,
        frames=len(x),
        interval=50,
    ).save(
        filename="animation.gif",
        writer=animation.PillowWriter(fps=30, bitrate=1800),
    )


def generate_random_walk(n: int) -> tuple[NDArray, NDArray]:
    phi = np.random.choice([0, 1, 2, 3], size=n) * np.pi / 2
    return np.cumsum(np.round(np.cos(phi))), np.cumsum(np.round(np.sin(phi)))


def main():
    x, y = generate_random_walk(1000)
    animate_random_walk(x, y)


if __name__ == "__main__":
    main()
