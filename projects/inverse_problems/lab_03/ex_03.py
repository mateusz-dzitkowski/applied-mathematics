from dataclasses import dataclass
from typing import Callable, Self
from contextlib import contextmanager
import numpy as np
from nptyping import NDArray
from matplotlib import pyplot as plt
import seaborn as sns


sns.set_style("whitegrid")


@dataclass
class FredholmTransform:
    func: Callable[[NDArray, NDArray], NDArray]

    @classmethod
    def gaussian(cls, sigma: float) -> Self:
        return cls(func=lambda x, y: np.exp(-np.square(x - y) / (2 * sigma**2)) / (np.sqrt(2 * np.pi) * sigma))

    def matrix(self, x: NDArray, y: NDArray) -> NDArray:
        return self.func(x, y).T * (y[1, 0] - y[0, 0])

    def inverse(self, x: NDArray, y: NDArray) -> NDArray:
        return np.linalg.inv(self.matrix(x, y))

    def apply(self, x: NDArray, y: NDArray, u: NDArray) -> NDArray:
        return self.matrix(x, y) @ u

    def apply_inverse(self, x: NDArray, y: NDArray, u: NDArray) -> NDArray:
        return self.inverse(x, y) @ u

    def apply_fourier(self, x: NDArray, y: NDArray, u: NDArray) -> NDArray:
        k = self.matrix(x, y)
        k = k / np.sum(k)
        return np.fft.ifft(np.fft.fft2(k) @ np.fft.fft(u))


@contextmanager
def fig(rows: int = 1, cols: int = 1):
    _fig, axs = plt.subplots(
        nrows=rows,
        ncols=cols,
        figsize=(10, 7),
        layout="tight",
    )
    yield _fig, axs
    _fig.show()
    _fig.clear()


def square(m: int, n: int) -> tuple[NDArray, NDArray, list[NDArray]]:
    x = np.linspace(-1, 1, m, endpoint=True)
    y = np.linspace(-1, 1, n, endpoint=True)
    return x, y, np.meshgrid(x, y)


def heaviside(x: NDArray) -> NDArray:
    return np.heaviside(x, 1)


def pseudo_invert(matrix: NDArray, cutoff: float) -> NDArray:
    return np.linalg.pinv(matrix, rcond=cutoff)


def tikhonov(k: NDArray, f: NDArray, alpha: float) -> NDArray:
    return np.linalg.inv(k.T @ k + np.identity(k.shape[1]) * alpha) @ k.T @ f


def sub_01():
    x, y, (xx, yy) = square(100, 123)
    transform = FredholmTransform.gaussian(0.06)
    u = heaviside(y+0.5) - heaviside(y-0.5)
    f = transform.apply(xx, yy, u)

    with fig():
        sns.lineplot(x=y, y=u, label="u")
        sns.lineplot(x=x, y=f, label="f")


def sub_02():
    # in general you can't invert the matrix K, so setting M, and N to be equal there
    x, y, (xx, yy) = square(123, 123)
    transform = FredholmTransform.gaussian(0.06)
    u = heaviside(y + 0.5) - heaviside(y - 0.5)
    f = transform.apply(xx, yy, u)
    u_back = transform.apply_inverse(xx, yy, f)

    with fig():
        sns.lineplot(x=y, y=u, label="u")
        sns.lineplot(x=x, y=f, label="f")
        sns.lineplot(x=y, y=u_back, label="u_back")


def sub_03():
    x, y, (xx, yy) = square(123, 100)
    transform = FredholmTransform.gaussian(0.06)
    u = heaviside(y + 0.5) - heaviside(y - 0.5)
    f = transform.apply(xx, yy, u)
    f_delta = f + np.random.normal(scale=0.05, size=f.shape)

    u_back, *_ = np.linalg.lstsq(transform.matrix(xx, yy), f)
    u_back_delta, *_ = np.linalg.lstsq(transform.matrix(xx, yy), f_delta)

    with fig(rows=2) as (_fig, (ax_1, ax_2)):
        sns.lineplot(x=y, y=u, ax=ax_1, label="u")
        sns.lineplot(x=x, y=f, ax=ax_1, label="f")
        sns.lineplot(x=y, y=u_back, ax=ax_1, label="u_back")

        sns.lineplot(x=y, y=u, ax=ax_2, label="u")
        sns.lineplot(x=x, y=f_delta, ax=ax_2, label="f w/ noise")
        sns.lineplot(x=y, y=u_back_delta, ax=ax_2, label="u back")


def sub_04():
    x, y, (xx, yy) = square(100, 123)
    transform = FredholmTransform.gaussian(0.06)
    u = heaviside(y + 0.5) - heaviside(y - 0.5)
    f = transform.apply(xx, yy, u)
    f_delta = f + np.random.normal(scale=0.05, size=f.shape)

    k_pseudo_inverted = pseudo_invert(transform.matrix(xx, yy), 0.1)
    u_back = k_pseudo_inverted @ f
    u_back_delta = k_pseudo_inverted @ f_delta

    with fig(rows=2) as (_fig, (ax_1, ax_2)):
        sns.lineplot(x=y, y=u, ax=ax_1, label="u")
        sns.lineplot(x=x, y=f, ax=ax_1, label="f")
        sns.lineplot(x=y, y=u_back, ax=ax_1, label="u_back")

        sns.lineplot(x=y, y=u, ax=ax_2, label="u")
        sns.lineplot(x=x, y=f_delta, ax=ax_2, label="f w/ noise")
        sns.lineplot(x=y, y=u_back_delta, ax=ax_2, label="u back")


def sub_05():
    alpha = 0.015
    x, y, (xx, yy) = square(100, 123)
    transform = FredholmTransform.gaussian(0.06)
    u = heaviside(y + 0.5) - heaviside(y - 0.5)
    f = transform.apply(xx, yy, u)
    f_delta = f + np.random.normal(scale=0.05, size=f.shape)

    u_back = tikhonov(transform.matrix(xx, yy), f, alpha)
    u_back_delta = tikhonov(transform.matrix(xx, yy), f_delta, alpha)

    with fig(rows=2) as (_fig, (ax_1, ax_2)):
        sns.lineplot(x=y, y=u, ax=ax_1, label="u")
        sns.lineplot(x=x, y=f, ax=ax_1, label="f")
        sns.lineplot(x=y, y=u_back, ax=ax_1, label="u_back")

        sns.lineplot(x=y, y=u, ax=ax_2, label="u")
        sns.lineplot(x=x, y=f_delta, ax=ax_2, label="f w/ noise")
        sns.lineplot(x=y, y=u_back_delta, ax=ax_2, label="u back")


def sub_06():
    x, y, (xx, yy) = square(100, 123)
    transform = FredholmTransform.gaussian(0.06)
    u = heaviside(y + 0.5) - heaviside(y - 0.5)

    f = transform.apply_fourier(xx, yy, u)

    with fig():
        sns.lineplot(x=y, y=u, label="u")
        sns.lineplot(x=x, y=f, label="f")


def main():
    sub_01()
    sub_02()
    sub_03()
    sub_04()
    sub_05()
    sub_06()


if __name__ == "__main__":
    main()
