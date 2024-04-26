from nptyping import NDArray
import numpy as np
import plotly.graph_objects as go


def line(n: int) -> NDArray:
    return np.linspace(0, 1, n)


def square(n: int) -> list[NDArray]:
    x = np.linspace(0, 1, n)
    y = np.linspace(0, 1, n)
    return np.meshgrid(x, y)


def K(x: NDArray, y: NDArray, t: float) -> NDArray:
    mapped_x = np.where(y < x, x, y)
    mapped_y = np.where(y < x, y, x)
    return mapped_y * (1 - mapped_x) / t


def u(x: NDArray) -> NDArray:
    return (x - 1) * np.sin(x)


def u_perturbation(x: NDArray, delta: float) -> NDArray:
    return delta * (x - 1) * np.sin(x / delta)


def u_delta(x: NDArray, delta: float) -> NDArray:
    return u(x) + u_perturbation(x, delta)


def f(x: NDArray, t: float) -> NDArray:
    return t * ((x - 1) * np.sin(x) - 2 * np.cos(x))


def f_perturbation(x: NDArray, t: float, delta: float) -> NDArray:
    return t * ((x - 1) / delta * np.sin(x / delta) - np.cos(x / delta))


def f_delta(x: NDArray, t: float, delta: float) -> NDArray:
    return f(x, t) + f_perturbation(x, t, delta)


def f_numerical(x: NDArray, t: float) -> NDArray:
    return -t * np.diff(u(x), n=2) / np.diff(x)[0]**2


def f_delta_numerical(x: NDArray, t: float, delta: float) -> NDArray:
    return -t * np.diff(u_delta(x, delta), n=2) / np.diff(x)[0] ** 2


if __name__ == "__main__":
    T = 1
    N = 1000
    DELTA = 0.002

    x = line(N)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=f_delta(x, T, DELTA), mode="lines", name="f_delta(x)"))
    fig.add_trace(go.Scatter(x=x, y=f_delta_numerical(x, T, DELTA), mode="lines", name="f_delta(x) (numerical)"))
    fig.update_layout(xaxis_title="x", title=f"delta = {DELTA}")
    fig.show()
