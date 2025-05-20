from contextlib import contextmanager
from typing import Callable

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

sns.set_style("whitegrid")

Arr = np.ndarray
Func = Callable[[Arr], Arr]


@contextmanager
def fig(rows: int = 1, cols: int = 1, figsize: tuple[int, int] = (10, 7)):
    _fig, axs = plt.subplots(
        nrows=rows,
        ncols=cols,
        figsize=figsize,
        layout="tight",
    )
    yield _fig, axs
    _fig.show()
    _fig.clear()


def generate_x(n: int, *, s: int, func: Func = np.ones_like) -> Arr:
    assert 0 <= s < n

    x = func(np.arange(n))
    x[np.random.permutation(range(n))[: n - s]] = 0
    return x


def generate_k(m: int, n: int, *, delta: float) -> Arr:
    assert m < n

    k = np.random.normal(scale=delta, size=(m, n))
    return k / np.linalg.norm(k, axis=0)


def get_prox(lam: float) -> Func:
    assert lam > 0

    def prox(x: Arr) -> Arr:
        return np.sign(x) * np.maximum(np.abs(x) - lam, 0)

    return prox


def get_grad_g(y: Arr, k: Arr) -> Func:
    def grad_g(x: Arr) -> Arr:
        return 2 * k.T @ (k @ x - y)

    return grad_g


def proximal_gradient(y: Arr, k: Arr, *, lam: float, steps: int = 100) -> Arr:
    prox = get_prox(lam)
    grad_g = get_grad_g(y, k)

    x = np.ones(k.shape[1])
    for _ in range(steps):
        z = x - lam * grad_g(x)
        x = prox(z)

    return x


def solve_norm_2(y: Arr, k: Arr, *, lam: float) -> Arr:
    return lam * np.linalg.inv(np.eye(k.shape[1]) + lam * k.T @ k) @ k.T @ y


def sub_03():
    s = 50
    delta = 0.1
    n = 3210
    ms = [1234, 1987, 2345, 2789, 3209]
    lams = np.linspace(0.001, 0.5, 100)

    with fig() as (_, ax):
        ax.set_yscale("log")
        for m in ms:
            x = generate_x(n, s=s)
            k = generate_k(m, n, delta=delta)
            y = k @ x

            norms = [np.linalg.norm(x - proximal_gradient(y, k, lam=lam)) for lam in lams]
            plt.plot(lams, norms, label=f"m={m}")

        plt.xlabel("lambda")
        plt.ylabel("error")
        plt.legend()


def sub_04():
    s = 6
    delta = 0.1
    n = 100
    m = 70
    lam = 0.2

    x = generate_x(n, s=s, func=lambda _x: _x)
    k = generate_k(m, n, delta=delta)
    y = k @ x
    y_noise = y + np.random.normal(scale=3, size=y.shape)

    x_back = proximal_gradient(y, k, lam=lam)
    x_back_noise = proximal_gradient(y_noise, k, lam=lam)

    with fig(rows=2) as (_, (ax1, ax2)):
        ax1.plot(y, label="y")
        ax1.plot(y_noise, label="y noise")
        ax1.legend()

        ax2.plot(x, label="x")
        ax2.plot(x_back, label="x back")
        ax2.plot(x_back_noise, label="x back noise")
        ax2.legend()


def sub_05():
    s = 6
    delta = 0.1
    n = 100
    m = 70
    lam = 0.2

    x = generate_x(n, s=s, func=lambda _x: _x)
    k = generate_k(m, n, delta=delta)
    y = k @ x

    x_back = proximal_gradient(y, k, lam=lam)
    x_back_2 = solve_norm_2(y, k, lam=lam)

    with fig():
        plt.plot(x, label="x")
        plt.plot(x_back, label="x back")
        plt.plot(x_back_2, label="x back 2")
        plt.legend()


def main():
    # sub_03()
    # sub_04()
    sub_05()


if __name__ == "__main__":
    main()
