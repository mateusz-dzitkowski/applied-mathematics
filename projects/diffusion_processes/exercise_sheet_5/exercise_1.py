import numpy as np
from scipy.integrate import odeint
from pandas import DataFrame
from plotly import (
    express as xp,
    figure_factory as ff,
    graph_objects as go,
)
from nptyping import NDArray


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


def get_phase_portrait(beta: float, r: float, s_max: float = 1, i_max: float = 1) -> go.Figure:
    s, i = np.meshgrid(
        np.linspace(0, s_max, 20),
        np.linspace(0, i_max, 20),
    )
    u, v = phase_portrait(s, i, beta, r)
    return ff.create_quiver(s, i, u, v, scale=0.02)


def add_trajectories(fig: go.Figure, *solutions: DataFrame) -> go.Figure:
    for solution in solutions:
        fig = fig.add_trace(
            go.Scatter(
                x=solution["s"],
                y=solution["i"],
            ),
        )
    return fig


def show_solution(beta: float, r: float, t_max: float, initial: list[float], num_steps: int = 100_000):
    t = np.linspace(0, t_max, num_steps)
    equations = get_equations(beta, r)
    df = solve(equations, initial, t)

    plot_solution(df, beta, r)


def show_phase_portrait_and_trajectories(beta: float, r: float, num_trajectories: int, n: int = 1000, t_max: float = 10.):
    t = np.linspace(0, t_max, n)
    equations = get_equations(beta, r)

    solutions = [
        solve(equations, [s_0, i_0, r_0], t)
        for s_0, i_0, r_0
        in np.random.default_rng().uniform(size=(num_trajectories, 3))
    ]

    fig = get_phase_portrait(beta, r)
    fig = add_trajectories(fig, *solutions)
    fig.show()


def main():
    beta = 1
    r = 1
    t = np.linspace(0, 10, 1000)

    equations = get_equations(beta, r)
    solution = solve(equations, [0.99, 0.01, 0.], t)

    print(total_number_of_infected(solution))


if __name__ == "__main__":
    main()
