from itertools import product
from typing import (
    Callable,
    NamedTuple,
)

import numpy as np
from scipy import sparse as sp
from scipy.sparse import linalg
from matplotlib import pyplot as plt


Matrix = np.ndarray
Func1d = Callable[[Matrix], Matrix]
Func2d = Callable[[Matrix, Matrix], Matrix]


class Cij(NamedTuple):
    c_ipj_: float  # c_{i+0.5, j}
    c_imj_: float  # etc.
    c_i_jp: float
    c_i_jm: float


def ij_to_k(i: int, j: int, y_size: int) -> int:
    return i * y_size + j


def assemble_c_ij(c: Matrix, i: int, j: int, x_size: int, y_size: int) -> Cij:
    if i == 0:
        c_ipj_ = 0.5 * (c[i, j] + c[i + 1, j])
        c_imj_ = c[i, j]
    elif i == x_size - 1:
        c_ipj_ = c[i, j]
        c_imj_ = 0.5 * (c[i, j] + c[i - 1, j])
    else:
        c_ipj_ = 0.5 * (c[i, j] + c[i + 1, j])
        c_imj_ = 0.5 * (c[i, j] + c[i - 1, j])

    if j == 0:
        c_i_jp = 0.5 * (c[i, j] + c[i, j + 1])
        c_i_jm = c[i, j]
    elif j == y_size - 1:
        c_i_jp = c[i, j]
        c_i_jm = 0.5 * (c[i, j] + c[i, j - 1])
    else:
        c_i_jp = 0.5 * (c[i, j] + c[i, j + 1])
        c_i_jm = 0.5 * (c[i, j] + c[i, j - 1])

    return Cij(
        c_ipj_=c_ipj_,  # type: ignore
        c_imj_=c_imj_,  # type: ignore
        c_i_jp=c_i_jp,  # type: ignore
        c_i_jm=c_i_jm,  # type: ignore
    )


def assemble_a(dx: float, dy: float, x_size: int, y_size: int, c: Matrix, alpha: float) -> Matrix:
    # this function sucks ass it's O(x_size * y_size)

    n = x_size * y_size
    a = sp.lil_matrix((n, n))

    dx2 = 1/dx**2
    dy2 = 1/dy**2

    for i, j in product(range(x_size), range(y_size)):
        k = ij_to_k(i, j, y_size)
        cij = assemble_c_ij(c, i, j, x_size, y_size)
        a[k, k] = 1.0 + alpha * ((cij.c_ipj_ + cij.c_imj_) * dx2 + (cij.c_i_jp + cij.c_i_jm) * dy2)

        if i < x_size - 1:
            a[k, ij_to_k(i+1, j, y_size)] = -alpha * cij.c_ipj_ * dx2
        else:
            a[k, k] += -alpha*cij.c_ipj_ * dx2

        if i > 0:
            a[k, ij_to_k(i-1, j, y_size)] = -alpha * cij.c_imj_ * dx2
        else:
            a[k, k] += -alpha*cij.c_imj_ * dx2

        if j < y_size - 1:
            a[k, ij_to_k(i, j+1, y_size)] = -alpha * cij.c_i_jp * dy2
        else:
            a[k, k] += -alpha*cij.c_i_jp * dy2

        if j > 0:
            a[k, ij_to_k(i, j-1, y_size)] = -alpha * cij.c_i_jm * dy2
        else:
            a[k, k] += -alpha*cij.c_i_jm * dy2

    return a.tocsr()  # type: ignore


def solve_once(*, dx: float, dy: float, x_size: int, y_size: int, f: Matrix, c: Matrix, alpha: float) -> Matrix:
    a = assemble_a(dx, dy, x_size, y_size, c, alpha)
    f = f.reshape((x_size*y_size, 1))
    return linalg.spsolve(a, f).reshape((x_size, y_size))


def solve(*, dx: float, dy: float, x_size: int, y_size: int, f: Matrix, smoothing: Func2d, alpha: float = 1.0, steps: int = 100) -> Matrix:
    u = np.copy(f)

    for step in range(steps):
        print(f"{step:3} / {steps}")
        ux = np.diff(u, axis=0, prepend=u[:1, :])
        uy = np.diff(u, axis=1, prepend=u[:, :1])
        c = smoothing(ux, uy)
        u = solve_once(
            dx=dx,
            dy=dy,
            x_size=x_size,
            y_size=y_size,
            c=c,
            f=f,
            alpha=alpha,
        )

    return u


def vo_smoothing(beta: float) -> Func2d:
    def inner(x: Matrix, y: Matrix) -> np.ndarray:
        return 1 / np.sqrt(beta**2 + x**2 + y**2)

    return inner


def my_smoothing(beta: float) -> Func2d:
    def inner(x: Matrix, y: Matrix) -> np.ndarray:
        norm = np.sqrt(x**2 + y**2)
        return np.where(norm <= beta, np.ones_like(x), beta / norm)

    return inner


def main():
    x_min, x_max, x_size = 0, 1, 200
    y_min, y_max, y_size = 0, 1, 223
    alpha = 0.0000025
    beta = 0.000001
    steps = 10

    x = np.linspace(x_min, x_max, x_size)
    dx: float = np.diff(x)[0]  # type: ignore
    y = np.linspace(y_min, y_max, y_size)
    dy: float = np.diff(y)[0]  # type: ignore

    x, y = np.meshgrid(x, y, indexing="ij")
    f = (
        np.heaviside(x - 0.4, 1)
        + np.heaviside(y - 0.2, 1)
        + np.heaviside(x ** 2 + y ** 2 - 0.7, 1)
    )
    f_with_randomness = f + np.random.normal(scale=0.2, size=x.shape)

    plt.imshow(f)
    plt.show()

    plt.imshow(f_with_randomness)
    plt.show()

    solution = solve(
        dx=dx,
        dy=dy,
        x_size=x_size,
        y_size=y_size,
        f=f_with_randomness,
        smoothing=vo_smoothing(beta),
        alpha=alpha,
        steps=steps,
    )

    plt.imshow(solution)
    plt.show()


if __name__ == '__main__':
    main()
