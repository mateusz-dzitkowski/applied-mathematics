from typing import Callable
from nptyping import NDArray
import numpy as np
from plotly import express as xp
from pandas import DataFrame


def line(n: int) -> NDArray:
    return np.linspace(0, 1, n)


def A(alpha: float, n: int) -> NDArray:
    h = 1 / (n - 1)
    diag_ones = np.identity(n)

    diag_inner = np.identity(n) * 2 * alpha / h**2
    diag_inner[0, 0] = 0
    diag_inner[-1, -1] = 0

    near_diagonal = np.ones(n - 1) * alpha / h**2

    upper = np.diag(near_diagonal, 1)
    upper[0, 1] = 0

    lower = np.diag(near_diagonal, -1)
    lower[-1, -2] = 0

    return diag_ones + diag_inner - upper - lower


def f(x: NDArray) -> NDArray:
    return np.sin(2 * np.pi * x)


def f_prime_true(x: NDArray) -> NDArray:
    return 2 * np.pi * np.cos(2 * np.pi * x)


def f_with_noise(delta: float, k: int) -> Callable[[NDArray], NDArray]:
    def inner(x: NDArray) -> NDArray:
        return f(x) + np.sqrt(2) * delta * np.sin(2 * np.pi * k * x)
    return inner


def solve(n: int, foo: Callable[[NDArray], NDArray], alpha: float) -> DataFrame:
    x_v = line(n)
    f_v = foo(x_v)
    a_m = A(alpha, n)
    u_v = np.linalg.solve(a_m, f_v)

    return DataFrame(
        data={
            "x": x_v,
            "f": f_v,
            "u": u_v,
        }
    )


def derivatives(df) -> DataFrame:
    x = df["x"][1:]
    return DataFrame(
        data={
            "x": x,
            "f": df["f"].diff() / df["x"].diff(),
            "f_true": f_prime_true(x),
            "u": df["u"].diff() / df["x"].diff(),
        }
    )


def main():
    n = 4000
    delta = 0.01
    k = 91
    alpha = 0.0001

    f_foo = f_with_noise(delta, k)
    solution = solve(n, f_foo, alpha)
    solution_derivatives = derivatives(solution)

    xp.line(solution_derivatives, x="x", y=["f", "f_true", "u"]).show()


if __name__ == "__main__":
    main()
