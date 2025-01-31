from itertools import product
from multiprocessing import Pool

from matplotlib import pyplot as plt
import numpy as np

from projects.agent_based_modelling.assignment_6.model import Model, Params
from projects.agent_based_modelling.assignment_6.runge_kutta import runge_kutta_4
from projects.agent_based_modelling.assignment_6.graphs import lattice_with_diagonals


GRAPH_SIZES = [(10, 10)]
INITIAL_ADOPTIONS = [0, 8]
PARAMS = [Params(innovation=innovation, imitation=imitation) for innovation, imitation in product([0, 0.01], [0.25, 0.5])]

REWIRING_PROBABILITIES = [0.3, 0.6, 0.9]
TIME_TO_STABILISE_RUNS = 20


def plot_evolutions():
    setups = list(product(PARAMS, INITIAL_ADOPTIONS, GRAPH_SIZES))
    fig, axs = plt.subplots(len(setups), 1, figsize=(10, 6*len(setups)), layout="tight")

    for ax, (params, initial_adoptions, (m, n)) in zip(axs, setups):
        for beta in REWIRING_PROBABILITIES:
            ax.plot(
                Model(
                    params=params,
                    graph=lattice_with_diagonals(m, n, beta),
                    initial_adoptions=initial_adoptions,
                ).run().adoption_history,
                label=f"{beta=}",
            )
            ax.set_title(f"{params=}, {initial_adoptions=}, {m=}, {n=}")
        ax.legend()
        ax.set_ylim(-0.05, 1.05)
        ax.grid()

    plt.show()


def calculate_steps(args: tuple[Params, int, tuple[int, int], float]) -> int:
    params, initial_adoptions, (m, n), beta = args
    return Model(
        params=params,
        graph=lattice_with_diagonals(m, n, beta),
        initial_adoptions=initial_adoptions,
    ).run().current_step


def plot_time_to_stabilise():
    setups = list(product(PARAMS, INITIAL_ADOPTIONS, GRAPH_SIZES))
    fig, ax = plt.subplots(1, 1, figsize=(30, 8), layout="tight")
    with Pool() as pool:
        for params, initial_adoptions, graph_size in setups:
            print(f"{params=}, {initial_adoptions=}, {graph_size=}")
            beta = np.linspace(0, 1, 100)
            time_to_stabilise = np.array(
                [
                    np.array(pool.map(calculate_steps, [(params, initial_adoptions, graph_size, b)] * TIME_TO_STABILISE_RUNS)).mean()
                    for b in beta
                ]
            )
            ax.plot(beta, time_to_stabilise, label=f"{params=}, {initial_adoptions=}, {graph_size=}")

    ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.show()


def compare_graph_and_ode():
    params = Params(
        innovation=0.01,
        imitation=0.35,
    )
    simulated_raw = [
        Model(
            params=params,
            graph=lattice_with_diagonals(10, 10, 0.2),
            initial_adoptions=0,
        ).run().adoption_history
        for _ in range(10)
    ]
    max_run_length = max(len(run) for run in simulated_raw)
    simulated = np.array(
        [
            np.append(run, np.ones(max_run_length - len(run)))
            for run in simulated_raw
        ]
    ).mean(axis=0)

    def ode(_: float, y: float) -> float:
        return (1 - y)*(params.innovation + params.imitation*y)

    def exact(_x: np.ndarray, p: float, q: float) -> float:
        return p*(np.exp((p+q)*_x) - 1)/(p*np.exp((p+q)*_x) + q)

    x = np.linspace(start=0, stop=50, num=len(simulated))
    y_rk4 = runge_kutta_4(ode, 0, x)
    y_exact = exact(x, params.innovation, params.imitation)

    plt.plot(y_rk4)
    plt.plot(y_exact)
    plt.plot(simulated)
    plt.show()


def main():
    # plot_evolutions()
    # plot_time_to_stabilise()
    compare_graph_and_ode()


if __name__ == "__main__":
    main()
