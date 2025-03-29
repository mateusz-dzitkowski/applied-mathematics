from dataclasses import dataclass
from typing import Callable, Self
from contextlib import contextmanager
import numpy as np
from nptyping import NDArray
from matplotlib import pyplot as plt
import seaborn as sns


sns.set_style("whitegrid")


@contextmanager
def fig(rows: int = 1, cols: int = 1):
    _fig, axs = plt.subplots(
        nrows=rows,
        ncols=cols,
        figsize=(10, 7),
        layout="tight",
    )
    yield _fig, axs
    _fig.show()
    _fig.clear()


def d2dx2(y: NDArray, dx: float) -> NDArray:
    return (y[2:] - 2*y[1:-1] + y[:-2]) / dx


def main():
    t = 3
    delta = 0.01

    x = np.linspace(0, 1, 1000)
    dx: float = x[1] - x[0]  # type: ignore

    f = (x-1) * np.sin(x)
    f_delta = f + delta*(x-1)*np.sin(x/delta)

    u_back = -t * d2dx2(f, dx)
    u_back_delta = -t * d2dx2(f_delta, dx)

    with fig(rows=2) as (_, (ax_1, ax_2)):
        sns.lineplot(x=x, y=f, ax=ax_1, label="f")
        sns.lineplot(x=x, y=f_delta, ax=ax_1, label="f w/ noise")

        sns.lineplot(x=x[1:-1], y=u_back, ax=ax_2, label="u from f")
        sns.lineplot(x=x[1:-1], y=u_back_delta, ax=ax_2, label="u from f w/ noise")


if __name__ == '__main__':
    main()
