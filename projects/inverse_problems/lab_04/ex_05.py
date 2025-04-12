import cmath
from contextlib import contextmanager
from typing import Callable

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.optimize import minimize

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


def get_u(a: float, b: float, u0: float, u1: float) -> Func:
    d = cmath.sqrt(a**2 - 4 * b)
    assert d != 0, "Bad choice of a and b"

    def inner(x: Arr) -> Arr:
        e_xd = np.exp(x * d)
        return np.real(np.exp(-x / 2 * (d + a)) * (a * u0 * (e_xd - 1) + u0 * d * (e_xd + 1) + 2 * u1 * (e_xd - 1)) / (2 * d))

    return inner


def get_n(delta: float) -> Func:
    return lambda x: np.random.uniform(-delta, delta, size=x.shape)


def lstsq_sub_03(a: float, b: float, u0: float, u1: float, delta: float) -> Arr:
    x_max, steps = 10, 1000
    x = np.linspace(0, x_max, steps)
    u = get_u(a, b, u0, u1)(x)
    n = get_n(delta)(x)
    u_delta = u + n
    dx = x[1] - x[0]

    int_1 = np.cumsum(u_delta - u0) * dx

    xx = x.reshape(-1, 1)
    tt = x.reshape(1, -1)
    x_minus_t = np.maximum(xx - tt, 0.0)
    int_2 = np.sum(u_delta * x_minus_t, axis=1) * dx

    a_mat = np.vstack([int_1, int_2]).T
    f_vec = u0 + u1 * x - u_delta

    return np.linalg.lstsq(a_mat, f_vec, rcond=None)[0]


def runge_kutta(x: Arr, f: Callable[[float, Arr], Arr], u_0: Arr):
    u = [u_0]
    for x_n, x_n_plus in zip(x[:-1], x[1:]):
        h = x_n_plus - x_n
        u_n = u[-1]
        k_1 = f(x_n, u_n)
        k_2 = f(x_n + h / 2, u_n + h * k_1 / 2)
        k_3 = f(x_n + h / 2, u_n + h * k_2 / 2)
        k_4 = f(x_n_plus, u_n + h * k_3)
        u.append(u_n + h / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4))

    return np.asarray(u)


def get_f(a: float, b: float) -> Callable[[float, Arr], Arr]:
    def inner(_: float, uv: Arr) -> Arr:
        u, v = uv
        return np.array(
            [v, -a * v - b * u],
        )

    return inner


def sub_02():
    x = np.linspace(0, 10, 1000)
    u = get_u(2, 5, 1, -1)(x)
    n = get_n(0.02)(x)

    with fig():
        sns.lineplot(x=x, y=u + n)


def sub_03():
    n = 100
    deltas = np.linspace(0, 0.1, 100)
    a, b, u0, u1 = 2, 5, 1, -1
    ab = np.array([a, b])

    mean_of_errors = [np.mean([np.sqrt(ab**2 + lstsq_sub_03(a, b, u0, u1, delta) ** 2) for _ in range(n)]) for delta in deltas]

    with fig():
        sns.lineplot(x=deltas, y=mean_of_errors)


def sub_04():
    grad_epsilon = 1e-5
    a_true, b_true = 2, 5
    u0, u1 = 1, -1
    delta = 0.1
    x_max, steps = 10, 100
    x = np.linspace(0, x_max, steps)
    u_true = get_u(a_true, b_true, u0, u1)(x)
    u_delta = u_true + get_n(delta)(x)
    # u0_delta = u_delta[0]
    # u1_delta = (u_delta[1] - u_delta[0]) / (x[1] - x[0])
    u0u1 = np.array([u0, u1])

    def loss(_u: Arr) -> Arr:
        return 1 / 2 * np.sum((_u - u_delta) ** 2)

    def objective(ab: tuple[float, float]) -> Arr:
        a, b = ab
        u = runge_kutta(x, get_f(a, b), u0u1)[:, 0]
        return loss(u)

    def gradient(ab: tuple[float, float]) -> tuple[Arr, Arr]:
        a, b = ab

        u = runge_kutta(x, get_f(a, b), u0u1)[:, 0]
        u_loss = loss(u)

        u_a = runge_kutta(x, get_f(a + grad_epsilon, b), u0u1)[:, 0]
        grad_a = (loss(u_a) - u_loss) / grad_epsilon

        u_b = runge_kutta(x, get_f(a, b + grad_epsilon), u0u1)[:, 0]
        grad_b = (loss(u_b) - u_loss) / grad_epsilon

        return grad_a, grad_b

    res = minimize(
        fun=objective,
        x0=np.array([0.0, 0.0]),
        method="BFGS",  # not a standard Gradient Descent, but I don't wanna do it
        jac=gradient,
    )
    a, b = res.x
    u_back = runge_kutta(x, get_f(a, b), u0u1)[:, 0]

    with fig():
        sns.lineplot(x=x, y=u_delta, label="u delta")
        sns.lineplot(x=x, y=u_true, label="u true")
        sns.lineplot(x=x, y=u_back, label="u back")


def main():
    # sub_02()
    # sub_03()
    sub_04()


if __name__ == "__main__":
    main()
