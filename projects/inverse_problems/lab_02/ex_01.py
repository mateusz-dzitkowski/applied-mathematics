from itertools import product
from typing import Callable

import numpy as np
from matplotlib import pyplot as plt

X = np.ndarray
F = Callable[[X], X]


def f(x: X) -> X:
    return np.sin(2 * np.pi * x)


def f_prime(x: X) -> X:
    return 2 * np.pi * np.cos(2 * np.pi * x)


def get_f_delta(delta: float, k: int) -> F:
    return lambda x: f(x) + get_n(delta, k)(x)


def get_f_delta_prime(delta: float, k: int) -> F:
    return lambda x: f_prime(x) + get_n_prime(delta, k)(x)


def get_n(delta: float, k: int) -> F:
    return lambda x: np.sqrt(2) * delta * np.sin(2 * np.pi * k * x)


def get_n_prime(delta: float, k: int) -> F:
    return lambda x: 2 * np.sqrt(2) * delta * np.pi * k * np.cos(2 * np.pi * k * x)


def sub_2():
    ks = [1, 10, 100]
    deltas = [0.1, 0.01, 0.001]
    x = np.linspace(0, 1, 1000)

    combinations = list(product(deltas, ks))
    fig, axs = plt.subplots(len(combinations), 2, figsize=(14, 5 * len(combinations)))

    for i, (delta, k) in enumerate(combinations):
        axs[i][0].plot(x, f(x), label="f")
        axs[i][0].plot(x, get_f_delta(delta, k)(x), label="f_delta")
        axs[i][0].set_ylabel(f"{k=}, {delta=}")
        axs[i][0].legend()

        axs[i][1].plot(x, f_prime(x), label="f'")
        axs[i][1].plot(x, get_f_delta_prime(delta, k)(x), label="f'_delta")
        axs[i][1].legend()

    fig.tight_layout()
    fig.show()


def sub_4():
    delta = 0.1
    k = 10
    f_delta = get_f_delta(delta, k)
    hs = np.logspace(0, 3, 10000) / 10000

    estimates = 4 * np.pi**2 * hs + 2 * np.sqrt(2) * np.pi * delta * k
    norms = np.zeros_like(hs)

    for i, h in enumerate(hs):
        x = np.arange(start=0, stop=1, step=h)
        true = f_prime(x)[1:-1]
        approx = (f_delta(x)[2:] - f_delta(x)[:-2]) / (2 * h)
        norms[i] = np.max(np.abs(true - approx))

    plt.plot(hs, norms, label="numerical error")
    plt.plot(hs, estimates, label="analytical estimation")
    plt.xlabel("h")
    plt.ylabel("error")
    plt.title(f"log-log plot of the numerical differentiation error, {delta=}, {k=}")
    plt.grid()
    plt.legend()
    plt.show()


def main():
    sub_4()


if __name__ == "__main__":
    main()
