from contextlib import contextmanager
from typing import Callable

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

sns.set_style("whitegrid")
Arr = np.ndarray
Func = Callable[[Arr], Arr]


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


def f(x: Arr) -> Arr:
    return -np.ones_like(x)


def u(delta: float = 0.0) -> Func:
    if delta == 0:
        return lambda x: x

    return lambda x: x + delta * np.sin(x / delta**2)


def u_prime(delta: float = 0.0) -> Func:
    if delta == 0:
        return lambda x: np.ones_like(x)

    return lambda x: np.ones_like(x) + 1 / delta * np.cos(x / delta**2)


def solve_for_a(x: Arr, u_prime_func: Func) -> Arr:
    dx = x[1] - x[0]
    return -np.cumsum(f(x)) * dx / u_prime_func(x)


def main():
    delta = 0.1
    x = np.linspace(0, 1, 123)
    with fig(rows=2) as (_, (ax1, ax2)):
        sns.lineplot(x=x, y=u()(x), ax=ax1)
        sns.lineplot(x=x, y=u(delta)(x), ax=ax1)

        sns.lineplot(x=x, y=solve_for_a(x, u_prime()), ax=ax2)
        sns.lineplot(x=x, y=solve_for_a(x, u_prime(delta)), ax=ax2)


if __name__ == "__main__":
    main()
