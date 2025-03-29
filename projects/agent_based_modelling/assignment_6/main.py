import time
from itertools import product
from multiprocessing import Pool

import numpy as np
from matplotlib import pyplot as plt

from projects.agent_based_modelling.assignment_6.graphs import lattice_with_diagonals
from projects.agent_based_modelling.assignment_6.model import Model, Params
from projects.agent_based_modelling.assignment_6.runge_kutta import runge_kutta_4

GRAPH_SIZES = [(10, 10)]
PARAMS = [
    Params(
        innovation=innovation,
        imitation=imitation,
        initial_adoptions=initial_adoptions,
    )
    for innovation, imitation, initial_adoptions in product(
        [0, 0.01],
        [0.25, 0.5],
        [0, 8],
    )
]

REWIRING_PROBABILITIES = [0.3, 0.6, 0.9]
TIME_TO_STABILISE_RUNS = 100


def plot_evolutions():
    setups = list(product(PARAMS, GRAPH_SIZES))
    fig, axs = plt.subplots(len(setups), 1, figsize=(10, 6 * len(setups)), layout="tight")

    for ax, (params, (m, n)) in zip(axs, setups):
        for beta in REWIRING_PROBABILITIES:
            ax.plot(
                Model(
                    params=params,
                    graph=lattice_with_diagonals(m, n, beta),
                )
                .run()
                .adoption_history,
                label=f"{beta=}",
            )
            ax.set_title(f"{params=}, {m=}, {n=}")
        ax.legend()
        ax.set_xlabel("step")
        ax.set_ylabel("fraction of adopted")
        ax.set_ylim(-0.05, 1.05)
        ax.grid()

    plt.show()


def calculate_steps(args: tuple[Params, tuple[int, int], float]) -> int:
    params, (m, n), beta = args
    return (
        Model(
            params=params,
            graph=lattice_with_diagonals(m, n, beta),
        )
        .run()
        .current_step
    )


def plot_time_to_stabilise():
    setups = list(product(PARAMS, GRAPH_SIZES))
    fig, ax = plt.subplots(1, 1, figsize=(30, 8), layout="tight")
    with Pool() as pool:
        for params, graph_size in setups:
            print(f"{params=}, {graph_size=}")
            beta = np.linspace(0, 1, 100)
            time_to_stabilise = np.array(
                [np.array(pool.map(calculate_steps, [(params, graph_size, b)] * TIME_TO_STABILISE_RUNS)).mean() for b in beta]
            )
            ax.plot(beta, time_to_stabilise, label=f"{params=}, {graph_size=}")

    ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    ax.set_title(f"mean time to stabilise as a function of beta over {TIME_TO_STABILISE_RUNS} runs")
    ax.set_xlabel("beta")
    ax.set_ylabel("mean time to stabilise")
    ax.grid()
    plt.show()


def compare_graph_and_ode():
    params = Params(
        innovation=0.01,
        imitation=0.35,
        initial_adoptions=0,
    )
    m = 10
    n = 10
    beta = 0
    runs = 100

    simulated_raw = [
        Model(
            params=params,
            graph=lattice_with_diagonals(m, n, beta),
        )
        .run()
        .adoption_history
        for _ in range(runs)
    ]
    max_run_length = max(len(run) for run in simulated_raw)
    simulated = np.array([np.append(run, np.ones(max_run_length - len(run))) for run in simulated_raw]).mean(axis=0)

    def ode(_: float, y: float) -> float:
        return (1 - y) * (params.innovation + params.imitation * y)

    def exact(_x: np.ndarray, p: float, q: float, a: float) -> float:
        return (p * (a + np.exp((p + q) * _x) - 1) + a * q * np.exp((p + q) * _x)) / ((a * q + p) * np.exp((p + q) * _x) + q - a * q)

    x = np.linspace(start=0, stop=50, num=len(simulated))  # arbitrary 50 IDK
    y_rk4 = runge_kutta_4(ode, 0, x)
    y_exact = exact(x, params.innovation, params.imitation, params.initial_adoptions / (m * n))

    plt.plot(y_rk4, label="runge kutta 4")
    plt.plot(y_exact, label="exact solution")
    plt.plot(simulated, label="graph simulation")
    plt.title("comparison of the graph simulation with the ode")
    plt.xlabel("step")
    plt.ylabel("fraction of adopted")
    plt.grid()
    plt.legend()
    plt.show()


def main():
    plot_evolutions()
    plot_time_to_stabilise()
    compare_graph_and_ode()


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()

    print(f"Done, took {end - start} seconds")
