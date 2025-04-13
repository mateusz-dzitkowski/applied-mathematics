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

    r_plus = (-a + d) / 2
    r_minus = (-a - d) / 2
    big_a = (u1 - u0*r_minus) / (r_plus - r_minus)
    big_b = (u0*r_plus - u1) / (r_plus - r_minus)

    def inner(x: Arr) -> Arr:
        return np.real(big_a*np.exp(r_plus*x) + big_b*np.exp(r_minus*x))

    return inner


def get_n(delta: float) -> Func:
    return lambda x: np.random.uniform(-delta, delta, size=x.shape)


def lstsq_sub_03(a: float, b: float, u0: float, u1: float, delta: float) -> Arr:
    x_max, steps = 10, 321
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


def sub_02(a: float, b: float, u0: float, u1: float):
    delta = 0.1

    x = np.linspace(0, 10, 321)
    u = get_u(a, b, u0, u1)(x)
    n = get_n(delta)(x)

    with fig() as (f, _):
        f.suptitle(f"{a=}, {b=}, {u0=}, {u1=}, {delta=}")
        sns.lineplot(x=x, y=u + n)


def sub_03(a_true: float, b_true: float, u0: float, u1: float):
    delta = 0.1
    x_max, steps = 10, 321
    x = np.linspace(0, x_max, steps)
    u_true = get_u(a_true, b_true, u0, u1)(x)
    u_delta = u_true + get_n(delta)(x)
    dx = x[1] - x[0]

    int_1 = np.cumsum(u_delta - u0) * dx

    xx = x.reshape(-1, 1)
    tt = x.reshape(1, -1)
    x_minus_t = np.maximum(xx - tt, 0.0)
    int_2 = np.sum(u_delta * x_minus_t, axis=1) * dx

    a_mat = np.vstack([int_1, int_2]).T
    f_vec = u0 + u1 * x - u_delta
    a, b = np.linalg.lstsq(a_mat, f_vec, rcond=None)[0]
    u_back = get_u(a, b, u0, u1)(x)
    with fig() as (f, _):
        f.suptitle(f"{a_true=}, {b_true=}, {u0=}, {u1=}, {delta=}\n{a=}, {b=}")
        sns.lineplot(x=x, y=u_delta, label="u delta")
        sns.lineplot(x=x, y=u_true, label="u true")
        sns.lineplot(x=x, y=u_back, label="u back")

    # compute the errors
    n = 100
    deltas = np.linspace(0, 0.1, 100)
    ab = np.array([a_true, b_true])

    mean_of_errors = [np.mean([np.linalg.norm(ab - lstsq_sub_03(a, b, u0, u1, delta)) for _ in range(n)]) for delta in deltas]

    with fig() as (f, _):
        f.suptitle(f"{a=}, {b=}, {u0=}, {u1=}, {delta=}")
        sns.lineplot(x=deltas, y=mean_of_errors)


def sub_04(a_true: float, b_true: float, u0: float, u1: float):
    grad_epsilon = 1e-5
    delta = 0.1
    x_max, steps = 10, 321
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

    with fig() as (f, _):
        f.suptitle(f"{a_true=}, {b_true=}, {u0=}, {u1=}, {delta=}\n{a=}, {b=}")
        sns.lineplot(x=x, y=u_delta, label="u delta")
        sns.lineplot(x=x, y=u_true, label="u true")
        sns.lineplot(x=x, y=u_back, label="u back")


def main():
    params = 2, 5, 1, -1
    sub_02(*params)
    sub_03(*params)
    sub_04(*params)


if __name__ == "__main__":
    main()
