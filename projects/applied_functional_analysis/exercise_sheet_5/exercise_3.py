import numpy as np
import plotly.graph_objects as go
from nptyping import NDArray


def square(m: int, n: int) -> list[NDArray]:
    x = np.linspace(0, 1, m)
    y = np.linspace(0, 1, n)
    return np.meshgrid(x, y)


def heaviside(x: NDArray) -> NDArray:
    return np.heaviside(x, 1)


def K(x: NDArray, y: NDArray, sigma: float) -> NDArray:
    return np.exp(-np.square(x - y) / (2 * sigma**2)) / (np.sqrt(2 * np.pi) * sigma)


def f(x: NDArray) -> NDArray:
    # return heaviside(x - 0.3) - heaviside(x - 0.5) + heaviside(x - 0.9) + 3 * x  # lines 6
    # return heaviside(x - 0.2) + heaviside(x - 0.5) + heaviside(x - 0.7) + heaviside(x - 0.9)  # lines 7
    return -x + np.sin(8 * x) + heaviside(x - 0.2) + heaviside(x - 0.5) - heaviside(x - 0.8)  # lines 8
    # return heaviside(x - 0.3) - heaviside(x - 0.5)  # normal


def A(x: NDArray, y: NDArray, sigma: float) -> NDArray:
    dy = 1 / (len(y) - 1)
    return K(x, y, sigma).T * dy


def pseudo_invert(matrix: NDArray, cutoff: float) -> NDArray:
    return np.linalg.pinv(matrix, rcond=cutoff)


def plot_condition():
    m = 500
    sigma = 0.05
    n_v = np.array([num for num in range(2, 1000)])

    def _cond(_m: int, _n: int, _sigma: float) -> float:
        x, y = square(_m, _n)
        return np.linalg.cond(A(x, y, sigma))

    condition_numbers = np.array([_cond(m, n, sigma) for n in n_v])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n_v, y=np.log(condition_numbers), mode="markers"))
    fig.update_layout(
        xaxis_title="N",
        yaxis_title="log(condition number of A_N)",
    )
    fig.show()


def plot_everything(
    _x: NDArray,
    _y: NDArray,
    _f: NDArray,
    _u: NDArray,
    _recovered_f: NDArray,
    sigma: float,
    cutoff: float,
):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=_y, y=_f, mode="lines", name="Original f"))
    fig.add_trace(go.Scatter(x=_x, y=_u, mode="lines", name="u"))
    fig.add_trace(go.Scatter(x=_y, y=_recovered_f, mode="lines", name="Recovered f"))
    fig.update_layout(title=f"N = {len(_y)}, M = {len(_x)}, sigma = {sigma}, cutoff = {cutoff}")
    fig.show()


def main():
    SIGMA = 0.05
    CUTOFF = 1e-10
    M = 4000
    N = 3000

    x, y = square(M, N)
    x_line = x[0]
    y_line = y[:, 0]

    A_m = A(x, y, SIGMA)
    f_v = f(y_line)
    u_v = A_m @ f_v

    f_back_v = pseudo_invert(A_m, CUTOFF) @ u_v

    plot_everything(x_line, y_line, f_v, u_v, f_back_v, SIGMA, CUTOFF)


if __name__ == "__main__":
    main()
