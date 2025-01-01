from typing import Callable

from matplotlib import pyplot as plt
import numpy as np


Func = Callable[[np.ndarray], np.ndarray]


def kth_diag_indices(a, k):
    rowidx, colidx = np.diag_indices_from(a)
    colidx = colidx.copy()  # rowidx and colidx share the same buffer

    if k > 0:
        colidx += k
    else:
        rowidx -= k
    k = np.abs(k)

    return rowidx[:-k], colidx[:-k]


def solve(*, x: np.ndarray, func_c: Func, func_f: Func, alpha: float = 1.0) -> np.ndarray:
    h = np.diff(x)[0]  # assume that discretization is uniform YOLO
    n = x.shape[0]

    c_full = func_c(x)
    c_plus = c_full[2:]
    c_minus = c_full[:-2]
    c = c_full[1:-1]

    f = func_f(x)
    f[0] = f[-1] = 0

    a = np.zeros((n, n))
    np.fill_diagonal(a, np.hstack([np.array([1]), 1 + alpha / h**2 * (3*c + (c_plus + c_minus)/2), np.array([1])]))  # diagonal
    a[kth_diag_indices(a, 1)] = np.hstack([np.array([-1]), -alpha / h**2 * (c + (c_plus + c) / 2)])  # superdiagonal
    a[kth_diag_indices(a, -1)] = np.hstack([-alpha / h**2 * (c + (c + c_minus) / 2), np.array([-1])])  # subdiagonal

    return np.linalg.solve(a, f)


def main():
    x = np.linspace(0, np.pi, 500, endpoint=True)
    alpha = 1.0
    plt.plot(
        x,
        solve(
            x=x,
            func_c=lambda _x: np.ones_like(_x),
            func_f=lambda _x: 2*np.cos(_x),
            alpha=alpha,
        )
    )
    plt.plot(
        x,
        np.cos(x),
    )
    plt.show()


if __name__ == "__main__":
    main()
