from nptyping import NDArray
import numpy as np
import plotly.graph_objects as go


def line(n: int) -> NDArray:
    return np.linspace(0, 1, n)


def f(x: NDArray) -> NDArray:
    return np.sin(2 * np.pi * x)


def f_prime(x: NDArray) -> NDArray:
    return 2 * np.pi * np.cos(2 * np.pi * x)


def f_prime_numerical(x: NDArray) -> NDArray:
    return (f(x[2:]) - f(x[:-2])) / (2 * np.diff(x)[0])


def n_delta(x: NDArray, k: int, delta: float) -> NDArray:
    return np.sqrt(2) * delta * np.sin(2 * np.pi * k * x)


def n_delta_prime(x: NDArray, k: int, delta: float) -> NDArray:
    return 2 * np.sqrt(2) * np.pi * delta * k * np.cos(2 * np.pi * k * x)


def f_delta(x: NDArray, k: int, delta: float) -> NDArray:
    return f(x) + n_delta(x, k, delta)


def f_delta_prime(x: NDArray, k: int, delta: float) -> NDArray:
    return f_prime(x) + n_delta_prime(x, k, delta)


def f_delta_prime_numerical(x: NDArray, k: int, delta: float) -> NDArray:
    return (f_delta(x[2:], k, delta) - f_delta(x[:-2], k, delta)) / (2 * np.diff(x)[0])


if __name__ == "__main__":
    DELTA = 0.01
    N = 1000
    K = 70

    x = line(N)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=f(x), mode="lines", name="f(x)"))
    fig.add_trace(go.Scatter(x=x, y=f_delta(x, K, DELTA), mode="lines", name="f_delta(x)"))
    fig.update_layout(
        xaxis_title="x",
        # yaxis_title="||n_delta'||_inf",
        # title=f"delta = {DELTA}",
    )
    fig.show()
