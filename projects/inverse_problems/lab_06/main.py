from contextlib import contextmanager
from typing import Callable

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

sns.set_style("whitegrid")

Arr = np.ndarray
Func = Callable[[Arr], Arr]


@contextmanager
def fig():
    _fig, axs = plt.subplots(
        figsize=(10, 7),
        layout="tight",
    )
    yield _fig, axs
    _fig.show()
    _fig.clear()


def landweber(k: Arr, y: Arr, x0: Arr, delta: float, max_steps: int = 10000, on_step: Callable[[Arr], None] | None = None) -> Arr:
    k_norm = np.linalg.norm(k, ord=2)
    tau = 1.9 / k_norm**2

    x = x0.copy()
    if on_step is not None:
        on_step(x)
    for _ in range(1, max_steps):
        if on_step is not None:
            on_step(x)

        if delta > 0 and np.linalg.norm(k@x - y) < delta * 2 / (2 - tau * k_norm**2):
            print("reached the noise level")
            break

        x = x - tau * k.T @ (k@x - y)

    return x


def main():
    m, n = 100, 100
    x = np.arange(n).astype(np.float64)
    # k = np.eye(n, m)
    k = np.random.normal(size=(m, n))
    y = k @ x
    delta = 30
    y_noise = y + np.random.normal(scale=delta, size=y.shape)

    errs = []

    def on_step(_x: Arr):
        errs.append(np.linalg.norm(k@_x - y_noise))

    x_back = landweber(
        k=k,
        y=y_noise,
        x0=np.zeros_like(x),
        delta=delta,
        on_step=on_step,
    )

    with fig():
        plt.plot(y, label="y")
        plt.plot(y_noise, label="y_noise")
        plt.legend()

    with fig():
        plt.plot(x, label="x")
        plt.plot(x_back, label="x_back")
        plt.legend()

    with fig():
        plt.loglog(errs, label="errs")
        plt.loglog(np.ones_like(errs) * delta * 2 / (2 - 1.9), label="eta * delta")
        plt.legend()


if __name__ == '__main__':
    main()
