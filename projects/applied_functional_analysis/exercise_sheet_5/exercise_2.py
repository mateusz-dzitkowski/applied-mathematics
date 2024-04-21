from nptyping import NDArray
import numpy as np
from matplotlib import pyplot as plt


DELTA = 0.001
K = 67
N = 1000


def line() -> NDArray:
    return np.linspace(0, 1, N)


def d(x: NDArray) -> NDArray:
    return np.diff(x)


def f(x: NDArray) -> NDArray:
    return np.sin(2 * np.pi * x)


def n_delta(x: NDArray) -> NDArray:
    return np.sqrt(2) * DELTA * np.sin(2 * np.pi * K * x)


def f_delta(x: NDArray) -> NDArray:
    return f(x) + n_delta(x)


def f_prime(x: NDArray) -> NDArray:
    return (f(x[2:]) - f(x[:-2])) / (2 * d(x)[1:])


def n_delta_prime(x: NDArray) -> NDArray:
    return (n_delta(x[2:]) - n_delta(x[:-2])) / (2 * d(x)[1:])


def f_delta_prime(x: NDArray) -> NDArray:
    return (f_delta(x[2:]) - f_delta(x[:-2])) / (2 * d(x)[1:])


if __name__ == "__main__":
    x = line()
    plt.plot(f_prime(x))
    plt.plot(f_delta_prime(x))
    plt.show()
