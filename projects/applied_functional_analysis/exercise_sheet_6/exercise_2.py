from typing import Callable

import numpy as np
from nptyping import NDArray
from plotly import express as xp

Function = Callable[[NDArray], NDArray]


def line(n: int) -> NDArray:
    return np.linspace(0, 1, n)


def f(x: NDArray) -> NDArray:
    return -1 * np.ones(x.shape)


def u(x: NDArray) -> NDArray:
    return x


def u_delta(delta: float) -> Function:
    def inner(x: NDArray) -> NDArray:
        return u(x) + delta * np.sin(x / delta**2)

    return inner


def a(x: NDArray, f_function: Function, u_function: Function) -> NDArray:
    _x = x[1:]
    dx = np.diff(x)
    return np.concatenate([np.array([0]), -dx / np.diff(u_function(x)) * np.cumsum(f_function(_x) * dx)])


def main():
    n = 100000
    delta = 0.00001

    x = line(n)
    xp.line(
        x=x,
        y=a(x, f, u_delta(delta)),
    ).update_layout(
        title=f"{n=}, {delta=}",
        xaxis_title="x",
        yaxis_title="a_delta(x)",
    ).show()


if __name__ == "__main__":
    main()
