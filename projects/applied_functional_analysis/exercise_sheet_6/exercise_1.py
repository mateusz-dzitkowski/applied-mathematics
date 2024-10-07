from typing import Callable

import numpy as np
from nptyping import NDArray
from pandas import DataFrame
from plotly import express as xp


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


def f_true(x: NDArray) -> NDArray:
    return np.sin(2 * np.pi * x)


def f_prime_true(x: NDArray) -> NDArray:
    return 2 * np.pi * np.cos(2 * np.pi * x)


def f_with_noise(delta: float, k: int) -> Callable[[NDArray], NDArray]:
    def inner(x: NDArray) -> NDArray:
        return f_true(x) + np.sqrt(2) * delta * np.sin(2 * np.pi * k * x)

    return inner


def solve(n: int, foo: Callable[[NDArray], NDArray], alpha: float) -> DataFrame:
    x_v = line(n)
    f_v = foo(x_v)
    a_m = A(alpha, n)
    u_v = np.linalg.solve(a_m, f_v)

    return DataFrame(
        data={
            "x": x_v,
            "f": f_true(x_v),
            "f_delta": f_v,
            "u": u_v,
        }
    )


def derivatives(df) -> DataFrame:
    x = df["x"][1:]
    return DataFrame(
        data={
            "x": x,
            "f": f_prime_true(x),
            "f_delta": df["f_delta"].diff() / df["x"].diff(),
            "u": df["u"].diff() / df["x"].diff(),
        }
    ).dropna()


def function_error(alpha: float, delta: float, k: int, n: int = 1000) -> float:
    # ||u_alpha - f||
    f_foo = f_with_noise(delta, k)
    solution = solve(n, f_foo, alpha)

    return np.linalg.norm(solution["u"] - solution["f"])


def function_derivatives_error(alpha: float, delta: float, k: int, n: int = 1000) -> float:
    # ||u_alpha' - f'||
    f_foo = f_with_noise(delta, k)
    solution = solve(n, f_foo, alpha)
    solution_derivatives = derivatives(solution)

    return np.linalg.norm(solution_derivatives["u"] - solution_derivatives["f"])


def show_functions(n: int, delta: float, k: int, alpha: float):
    f_foo = f_with_noise(delta, k)
    solution = solve(n, f_foo, alpha)

    xp.line(
        solution,
        x="x",
        y=["f", "f_delta", "u"],
    ).update_layout(
        title=f"{n=}, {delta=}, {k=}, {alpha=}",
    ).show()


def show_function_derivatives(n: int, delta: float, k: int, alpha: float):
    f_foo = f_with_noise(delta, k)
    solution = solve(n, f_foo, alpha)
    solution_derivatives = derivatives(solution)

    xp.line(
        solution_derivatives,
        x="x",
        y=["f", "f_delta", "u"],
    ).update_layout(
        title=f"{n=}, {delta=}, {k=}, {alpha=}",
    ).show()


def show_function_errors(alpha_max: float, n: int, delta: float, k: int, num_alphas: int = 200):
    alpha = np.linspace(0, alpha_max, num_alphas)
    errors = np.array([function_error(a, delta, k, n) for a in alpha])

    xp.line(
        x=alpha,
        y=errors,
    ).update_layout(
        title=f"{n=}, {delta=}, {k=}",
        xaxis_title="alpha",
        yaxis_title="||u_alpha - f||",
    ).show()


def show_function_derivatives_errors(alpha_max: float, n: int, delta: float, k: int, num_alphas: int = 200):
    alpha = np.linspace(0, alpha_max, num_alphas)
    errors = np.array([function_derivatives_error(a, delta, k, n) for a in alpha])

    xp.line(
        x=alpha,
        y=errors,
    ).update_layout(
        title=f"{n=}, {delta=}, {k=}",
        xaxis_title="alpha",
        yaxis_title="||u_alpha' - f'||",
    ).show()


def main():
    delta = 0.001
    k = 1234
    n = 1000

    show_function_errors(0.0001, n, delta, k)


if __name__ == "__main__":
    main()
