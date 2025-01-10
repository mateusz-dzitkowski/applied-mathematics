from typing import Callable

import numpy as np
from matplotlib import pyplot as plt

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


def vo_smoothing(beta: float) -> Func:
    def inner(x: np.ndarray) -> np.ndarray:
        return 1 / np.sqrt(beta**2 + np.abs(x) ** 2)

    return inner


def my_smoothing(beta: float) -> Func:
    def inner(x: np.ndarray) -> np.ndarray:
        return np.where(np.abs(x) <= beta, np.ones_like(x), beta / np.abs(x))

    return inner


def solve_once(*, x: np.ndarray, c: np.ndarray, f: np.ndarray, alpha: float = 1.0) -> np.ndarray:
    h = np.diff(x)[0]  # assume that discretization is uniform YOLO
    n = x.shape[0]

    c_plus = c[2:]
    c_minus = c[:-2]
    c_mid = c[1:-1]
    c_plus_half = (c_plus + c_mid) / 2
    c_minus_half = (c_minus + c_mid) / 2

    almost_diagonal = 1 + alpha / h**2 * (c_plus_half + c_minus_half)
    almost_superdiagonal = -alpha / h**2 * c_plus_half
    almost_subdiagonal = -alpha / h**2 * c_minus_half

    diagonal = np.hstack(
        [
            np.array([1 + alpha/h**2*(c[0]+c[1])/2]),
            almost_diagonal,
            np.array([1 + alpha/h**2*(c[-1]+c[-2])/2])
        ],
    )
    superdiagonal = np.hstack([np.array([-alpha/h**2*(c[0]+c[1])/2]), almost_superdiagonal])
    subdiagonal = np.hstack([almost_subdiagonal, np.array([-alpha/h**2*(c[-1]+c[-2])/2])])

    a = np.zeros((n, n))
    np.fill_diagonal(a, diagonal)
    a[kth_diag_indices(a, 1)] = superdiagonal
    a[kth_diag_indices(a, -1)] = subdiagonal

    return np.linalg.solve(a, f)


def solve(*, x: np.ndarray, f: np.ndarray, smoothing_f: Func, alpha: float = 1.0, steps: int = 100) -> np.ndarray:
    u = np.copy(f)

    for _ in range(steps):
        u_diff = np.diff(u, prepend=u[0])
        c = smoothing_f(u_diff)
        u = solve_once(
            x=x,
            c=c,
            f=f,
            alpha=alpha,
        )

    return u


def main():
    x = np.linspace(0, 1, 1000, endpoint=True)
    alpha = 0.0000001
    beta = 0.00001

    def func_f(_x: np.ndarray) -> np.ndarray:
        return 1 + np.heaviside(_x - 0.4, 1) - np.heaviside(_x - 0.7, 1) + np.cos(np.pi*_x)

    f_with_randomness = func_f(x) + np.random.normal(scale=0.03, size=x.size)

    plt.figure(figsize=(15, 11), dpi=300)
    plt.plot(
        x,
        solve(
            x=x,
            smoothing_f=vo_smoothing(beta),
            f=f_with_randomness,
            alpha=alpha,
        ),
        label="denoised",
    )
    plt.plot(
        x,
        func_f(x),
        label="with no noise",
    )
    plt.plot(
        x,
        f_with_randomness,
        "r.",
        markersize=1,
        label="with noise",
    )
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
