import numpy as np
from nptyping import NDArray
from pandas import DataFrame
from plotly import (
    express as xp,
)
from plotly import (
    figure_factory as ff,
)
from plotly import (
    graph_objects as go,
)
from scipy.integrate import odeint


def get_equations(beta: float, r: float):
    def inner(y, _):
        _s, _i, _r = y
        ds = -beta * _s * _i
        di = beta * _s * _i - r * _i
        dr = r * _i

        return [ds, di, dr]

    return inner


def phase_portrait(s: NDArray, i: NDArray, beta: float, r: float) -> tuple[NDArray, NDArray]:
    return (
        -beta * s * i,
        beta * s * i - r * i,
    )


def solve(equations, initial_values: list[float], t: NDArray) -> DataFrame:
    y = odeint(equations, initial_values, t)
    return DataFrame(
        data={
            "t": t,
            "s": y[:, 0],
            "i": y[:, 1],
            "r": y[:, 2],
        }
    )


def plot_solution(solution: DataFrame, beta: float, r: float):
    xp.line(
        data_frame=solution,
        x="t",
        y=["s", "i", "r"],
        title=f"{beta=}, {r=}, s_0={solution['s'][0]}, i_0={solution['i'][0]}",
    ).show()


def total_number_of_infected(solution: DataFrame) -> float:
    return solution["i"].iloc[-1] + solution["r"].iloc[-1]


def get_phase_portrait(beta: float, r: float, s_max: float = 1, i_max: float = 1, normalised: bool = False) -> go.Figure:
    s, i = np.meshgrid(
        np.linspace(0, s_max, 10),
        np.linspace(0, i_max, 10),
    )
    u, v = phase_portrait(s, i, beta, r)
    if normalised:
        norm = np.sqrt(u**2 + v**2)
        u, v = u / norm, v / norm
    return ff.create_quiver(s, i, u, v, scale=0.02, showlegend=False)


def add_trajectories(fig: go.Figure, *solutions: DataFrame) -> go.Figure:
    for solution in solutions:
        fig = fig.add_trace(
            go.Scatter(
                x=solution["s"],
                y=solution["i"],
                showlegend=False,
            ),
        )
    return fig


def show_solution(beta: float, r: float, t_max: float, initial: list[float], num_steps: int = 100_000):
    t = np.linspace(0, t_max, num_steps)
    equations = get_equations(beta, r)
    df = solve(equations, initial, t)

    plot_solution(df, beta, r)


def show_phase_portrait_and_trajectories(
    beta: float,
    r: float,
    num_trajectories: int,
    n: int = 1000,
    t_max: float = 10.0,
    normalised: bool = False,
):
    t = np.linspace(0, t_max, n)
    equations = get_equations(beta, r)

    solutions = [solve(equations, [s_0, i_0, r_0], t) for s_0, i_0, r_0 in np.random.default_rng().uniform(size=(num_trajectories, 3))]

    fig = get_phase_portrait(beta, r, normalised=normalised)
    fig = add_trajectories(fig, *solutions)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_layout(
        autosize=False,
        width=1000,
        height=700,
        xaxis_title="S",
        yaxis_title="I",
    )
    fig.show()


def show_total_number_of_infected(beta_max: float = 5, n_beta: int = 1000, t_max: float = 10.0, n_t: int = 1000):
    t = np.linspace(0, t_max, n_t)
    beta = np.linspace(0, beta_max, n_beta)

    solutions = [solve(get_equations(b, 1), [0.99, 0.01, 0.0], t) for b in beta]
    totals = [total_number_of_infected(solution) for solution in solutions]

    xp.line(
        x=beta,
        y=totals,
    ).update_layout(
        xaxis_title="beta",
        yaxis_title="total infected",
    ).show()


def main():
    show_solution(
        beta=1.9,
        r=1,
        t_max=20,
        initial=[0.99, 0.01, 0],
    )

    show_phase_portrait_and_trajectories(
        beta=1.1,
        r=1,
        num_trajectories=20,
        normalised=True,
    )

    show_total_number_of_infected()


if __name__ == "__main__":
    main()
