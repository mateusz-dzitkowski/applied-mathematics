from nptyping import NDArray
import numpy as np

from matplotlib import pyplot as plt


SIGMA = 0.02
M = 1000
N = 1000
dy = 1 / N


def line() -> NDArray:
    return np.linspace(0, 1, M)


def square() -> list[NDArray]:
    x = np.linspace(0, 1, M)
    y = np.linspace(0, 1, N)
    return np.meshgrid(x, y)


def K(x: NDArray, y: NDArray) -> NDArray:
    return np.exp(-np.square(x - y) / (2 * SIGMA ** 2)) / (np.sqrt(2 * np.pi) * SIGMA)


def f(x: NDArray) -> NDArray:
    return np.heaviside(x - 0.3, 1) - np.heaviside(x - 0.5, 1)


def A(x: NDArray, y: NDArray) -> NDArray:
    return K(x, y) * dy


if __name__ == "__main__":
    x, y = square()
    x_line = x[0]
    A_m = A(x, y)
    f_v = f(x_line)

    u_v = A_m.dot(f_v)
    plt.plot(x_line, u_v)

    # f_back_v = np.linalg.inv(A_m).dot(u_v)
    # plt.plot(f_back_v)
    plt.show()
