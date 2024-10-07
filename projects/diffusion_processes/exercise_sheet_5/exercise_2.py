from dataclasses import asdict, dataclass
from enum import StrEnum, auto
from random import choice, uniform
from typing import Protocol, TypeAlias

import networkx as nx
import numpy as np
from matplotlib import (
    animation,
)
from matplotlib import (
    pyplot as plt,
)
from nptyping import NDArray
from pandas import DataFrame
from plotly import express as xp

STATE = "state"
FPS = 1
BITRATE = 2400


@dataclass
class Measures:
    total_infected_proportion: float
    time_to_clear: int
    time_to_peak: int


class NodeState(StrEnum):
    SUSCEPTIBLE = auto()
    INFECTIOUS = auto()
    REMOVED = auto()


Step: TypeAlias = dict[int, NodeState]


class StepForward(Protocol):
    def __call__(self, graph: nx.Graph, p: float, q: float = ..., /) -> nx.Graph: ...


@dataclass
class Simulation:
    steps: list[Step]

    def add_step(self, step: Step):
        self.steps.append(step)

    def get_fraction_of_infected_nodes(self) -> list[float]:
        return [len([1 for state in step.values() if state == NodeState.INFECTIOUS]) / len(step) for step in self.steps]

    def get_total_infected_fraction(self) -> float:
        last_step = self.steps[-1]
        return len(list(state for state in last_step.values() if state != NodeState.SUSCEPTIBLE)) / len(last_step)

    def get_time_to_clear(self) -> int:
        # evil list comprehension hack
        return next(
            n
            for n, step in enumerate(self.steps)
            if all(state != NodeState.INFECTIOUS for state in step.values())  # what the fuck
        )

    def get_time_to_peak(self) -> int:
        infected_counts = [len(list(state for state in step.values() if state == NodeState.INFECTIOUS)) for step in self.steps]
        return np.argmax(infected_counts)

    def to_measures(self) -> Measures:
        return Measures(
            total_infected_proportion=self.get_total_infected_fraction(),
            time_to_clear=self.get_time_to_clear(),
            time_to_peak=self.get_time_to_peak(),
        )


def get_nodes(graph: nx.Graph, state: NodeState) -> list[int]:
    return [node for node, data in graph.nodes(data=True) if data[STATE] == state]


def get_susceptible_neighbours_of(node: int, graph: nx.Graph) -> list[int]:
    return [node for node in nx.neighbors(graph, node) if graph.nodes[node][STATE] == NodeState.SUSCEPTIBLE]


def init_as_susceptible(graph: nx.Graph) -> nx.Graph:
    nx.set_node_attributes(graph, NodeState.SUSCEPTIBLE, STATE)
    return graph


def spawn_infectious(graph: nx.Graph, node_id: int | tuple[int, int] | None = None) -> nx.Graph:
    if node_id is None:
        node_id = choice(list(graph.nodes))
    graph.nodes[node_id][STATE] = NodeState.INFECTIOUS
    return graph


def step_forward_asynchronous(graph: nx.Graph, p: float, q: float = 0.0) -> nx.Graph:
    for _ in range(len(graph.nodes)):
        node = choice(list(graph.nodes))
        state = graph.nodes[node][STATE]

        if state == NodeState.INFECTIOUS:
            for neighbour in get_susceptible_neighbours_of(node, graph):
                if uniform(0, 1) < p:
                    graph.nodes[neighbour][STATE] = NodeState.INFECTIOUS
            graph.nodes[node][STATE] = NodeState.REMOVED
        elif state == NodeState.REMOVED:
            if uniform(0, 1) < q:
                graph.nodes[node][STATE] = NodeState.SUSCEPTIBLE

    return graph


def step_forward_synchronous(graph: nx.Graph, p: float, q: float = 0.0) -> nx.Graph:
    next = graph.copy()

    for infectious in get_nodes(graph, NodeState.INFECTIOUS):
        for neighbour in get_susceptible_neighbours_of(infectious, graph):
            if uniform(0, 1) < p:
                next.nodes[neighbour][STATE] = NodeState.INFECTIOUS
        next.nodes[infectious][STATE] = NodeState.REMOVED

    for removed in get_nodes(graph, NodeState.REMOVED):
        if uniform(0, 1) < q:
            next.nodes[removed][STATE] = NodeState.SUSCEPTIBLE

    return next


def take_snapshot(graph: nx.Graph) -> Step:
    return nx.get_node_attributes(graph, STATE)


def simulate(
    graph: nx.Graph,
    max_steps: int,
    p: float,
    q: float = 0.0,
    initial_infectious: int | tuple[int, int] | None = None,
    shortcircuit: bool = False,
    step_forward: StepForward = step_forward_synchronous,
) -> Simulation:
    graph = graph.copy()
    graph = init_as_susceptible(graph)
    graph = spawn_infectious(graph, initial_infectious)

    simulation: Simulation = Simulation([take_snapshot(graph)])

    for _ in range(max_steps - 1):
        graph = step_forward(graph, p, q)
        simulation.add_step(take_snapshot(graph))

        if shortcircuit and not get_nodes(graph, NodeState.INFECTIOUS):
            break

    return simulation


def get_average_fraction_of_infected_nodes(
    graph: nx.Graph,
    p: float,
    max_steps: int,
    num_runs: int,
    initial_infectious: int | tuple[int, int],
    step_forward: StepForward = step_forward_synchronous,
) -> NDArray:
    simulations = [
        simulate(
            graph=graph,
            p=p,
            max_steps=max_steps,
            initial_infectious=initial_infectious,
            step_forward=step_forward,
        )
        for _ in range(num_runs)
    ]
    fractions = np.array([simulation.get_fraction_of_infected_nodes() for simulation in simulations])
    return fractions.mean(axis=0)


def get_average_measures(
    graph: nx.Graph,
    p: float,
    max_steps: int,
    num_runs: int = 300,
    step_forward: StepForward = step_forward_synchronous,
) -> Measures:
    list_measures = [simulate(graph, max_steps, p, shortcircuit=True, step_forward=step_forward).to_measures() for _ in range(num_runs)]
    return Measures(
        total_infected_proportion=np.mean([measure.total_infected_proportion for measure in list_measures]),
        time_to_clear=np.mean([measure.time_to_clear for measure in list_measures]),
        time_to_peak=np.mean([measure.time_to_peak for measure in list_measures]),
    )


def get_measures_per_p(
    graph: nx.Graph,
    max_steps: int,
    num_p: int = 20,
    step_forward: StepForward = step_forward_synchronous,
) -> DataFrame:
    p_list = np.linspace(0, 1, num_p)
    return DataFrame(data=[asdict(get_average_measures(graph, p, max_steps, step_forward=step_forward)) | {"p": p} for p in p_list])


def show_measures(step_forward: StepForward = step_forward_synchronous):
    twod_lattice = get_measures_per_p(nx.grid_2d_graph(10, 10), 100, step_forward=step_forward)
    random = get_measures_per_p(nx.erdos_renyi_graph(100, 0.0365), 100, step_forward=step_forward)
    watts_strogatz = get_measures_per_p(nx.watts_strogatz_graph(100, 4, 0.4), 100, step_forward=step_forward)
    barabasi_albert = get_measures_per_p(nx.barabasi_albert_graph(100, 2), 100, step_forward=step_forward)

    total_infected = DataFrame(
        data={
            "p": twod_lattice["p"],
            "twod_lattice": twod_lattice["total_infected_proportion"],
            "random": random["total_infected_proportion"],
            "watts_strogatz": watts_strogatz["total_infected_proportion"],
            "barabasi_albert": barabasi_albert["total_infected_proportion"],
        }
    )
    xp.line(
        data_frame=total_infected,
        x="p",
        y=["twod_lattice", "random", "watts_strogatz", "barabasi_albert"],
        title="Fraction of total infected",
    ).show()

    time_to_clear = DataFrame(
        data={
            "p": twod_lattice["p"],
            "twod_lattice": twod_lattice["time_to_clear"],
            "random": random["time_to_clear"],
            "watts_strogatz": watts_strogatz["time_to_clear"],
            "barabasi_albert": barabasi_albert["time_to_clear"],
        }
    )
    xp.line(
        data_frame=time_to_clear,
        x="p",
        y=["twod_lattice", "random", "watts_strogatz", "barabasi_albert"],
        title="Time to clear infection",
    ).show()

    time_to_peak = DataFrame(
        data={
            "p": twod_lattice["p"],
            "twod_lattice": twod_lattice["time_to_peak"],
            "random": random["time_to_peak"],
            "watts_strogatz": watts_strogatz["time_to_peak"],
            "barabasi_albert": barabasi_albert["time_to_peak"],
        }
    )
    xp.line(
        data_frame=time_to_peak,
        x="p",
        y=["twod_lattice", "random", "watts_strogatz", "barabasi_albert"],
        title="Time to peak number of infected",
    ).show()


def animate(g: nx.Graph, simulation: Simulation, filename: str, grid_layout: bool = False):
    # planar layout: used for 2d grid graph
    layout = {(x, y): (y, -x) for x, y in g.nodes()} if grid_layout else nx.circular_layout(g)

    fig, ax = plt.subplots()

    def animate(n: int):
        step = simulation.steps[n]

        susceptible = [index for index, state in step.items() if state == NodeState.SUSCEPTIBLE]
        infectious = [index for index, state in step.items() if state == NodeState.INFECTIOUS]
        removed = [index for index, state in step.items() if state == NodeState.REMOVED]

        ax.clear()
        nx.draw_networkx_nodes(g, layout, nodelist=susceptible, node_color="green")
        nx.draw_networkx_nodes(g, layout, nodelist=infectious, node_color="red")
        nx.draw_networkx_nodes(g, layout, nodelist=removed, node_color="black")
        nx.draw_networkx_edges(g, layout)

    print("saving the animation...")
    animation.FuncAnimation(
        fig=fig,
        func=animate,  # type: ignore
        frames=len(simulation.steps),
    ).save(
        filename=filename,
        writer=animation.PillowWriter(fps=FPS, bitrate=BITRATE),
    )
    plt.close()


def main():
    graph = nx.grid_2d_graph(6, 6)
    simulation = simulate(
        graph=graph,
        max_steps=36,
        p=0.5,
        shortcircuit=True,
    )
    animate(graph, simulation, "2d_lattice.gif", grid_layout=True)


if __name__ == "__main__":
    main()
