from nptyping import NDArray
import numpy as np
from matplotlib import pyplot as plt


T = 1
N = 1000
DELTA = 0.005


def line() -> NDArray:
    return np.linspace(0, 1, N)


def square() -> list[NDArray]:
    x = np.linspace(0, 1, N)
    y = np.linspace(0, 1, N)
    return np.meshgrid(x, y)


def K(x: NDArray, y: NDArray) -> NDArray:
    mapped_x = np.where(y < x, x, y)
    mapped_y = np.where(y < x, y, x)
    return mapped_y * (1 - mapped_x) / T


def u(x: NDArray) -> NDArray:
    return (x - 1) * np.sin(x)


def u_perturbation(x: NDArray) -> NDArray:
    return DELTA * (x - 1) * np.sin(x / DELTA)


def u_delta(x: NDArray) -> NDArray:
    return u(x) + u_perturbation(x)


def f(x: NDArray) -> NDArray:
    return T * ((x - 1) * np.sin(x) - 2 * np.cos(x))


def f_perturbation(x: NDArray) -> NDArray:
    return T * ((x - 1) / DELTA * np.sin(x / DELTA) - np.cos(x / DELTA))


def f_delta(x: NDArray) -> NDArray:
    return f(x) + f_perturbation(x)


if __name__ == "__main__":
    x = line()
    plt.plot(f(x))
    plt.plot(f_delta(x))
    plt.show()
