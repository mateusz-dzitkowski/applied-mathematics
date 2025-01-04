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


def vo_smoothing(beta: float) -> Func:
    def inner(x: np.ndarray) -> np.ndarray:
        return 1 / np.sqrt(beta ** 2 + np.abs(x) ** 2)

    return inner


def my_smoothing(beta: float) -> Func:
    def inner(x: np.ndarray) -> np.ndarray:
        return np.where(np.abs(x) <= beta, np.ones_like(x), beta / np.abs(x))

    return inner


def solve_once(*, x: np.ndarray, c_full: np.ndarray, f_full: np.ndarray, alpha: float = 1.0) -> np.ndarray:
    h = np.diff(x)[0]  # assume that discretization is uniform YOLO
    n = x.shape[0]

    c_plus = c_full[2:]
    c_minus = c_full[:-2]
    c = c_full[1:-1]

    f = f_full
    f[0] = f[-1] = 0

    diagonal = 1 + alpha / (4 * h ** 2) * (8 * c)
    superdiagonal = -alpha / (4 * h ** 2) * (4 * c + c_plus - c_minus)
    subdiagonal = -alpha / (4 * h ** 2) * (4 * c + c_minus - c_plus)

    a = np.zeros((n, n))
    np.fill_diagonal(a, np.hstack([np.array([1]), diagonal, np.array([1])]))
    a[kth_diag_indices(a, 1)] = np.hstack([np.array([-1]), superdiagonal])
    a[kth_diag_indices(a, -1)] = np.hstack([subdiagonal, np.array([-1])])

    return np.linalg.solve(a, f)


def solve(*, x: np.ndarray, func_f: Func, smoothing_f: Func, alpha: float = 1.0, steps: int = 100) -> np.ndarray:
    f_full = func_f(x)
    u = np.copy(f_full)

    for _ in range(steps):
        u_diff = np.diff(u, prepend=u[0])
        c_full = smoothing_f(u_diff)
        u = solve_once(
            x=x,
            c_full=c_full,
            f_full=f_full,
            alpha=alpha,
        )

    return u


def main():
    x = np.linspace(0, 1, 1000, endpoint=True)
    alpha = 0.000001
    beta = 0.001

    randomness = np.random.normal(scale=0.03, size=x.size)
    func_f = lambda _x: np.heaviside(_x - 0.4, 1) - np.heaviside(_x - 0.6, 1) + randomness

    plt.figure(figsize=(10, 8), dpi=300)
    plt.plot(
        x,
        solve(
            x=x,
            smoothing_f=vo_smoothing(beta),
            func_f=func_f,
            alpha=alpha,
        ),
        label="with no noise",
    )
    plt.plot(
        x,
        func_f(x),
        "r.",
        markersize=1,
        label="with noise",
    )
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
