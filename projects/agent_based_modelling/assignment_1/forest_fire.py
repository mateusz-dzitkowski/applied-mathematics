from enum import StrEnum, auto
from itertools import product
from typing import Iterator

import numpy as np
from mesa import Agent, DataCollector, Model
from mesa.batchrunner import batch_run
from mesa.space import Position, SingleGrid
from pandas import DataFrame
from scipy.ndimage import measurements

Wind = tuple[int, int]


class TreeState(StrEnum):
    FINE = auto()
    BURNING = auto()
    BURNED_DOWN = auto()

    def color(self) -> str:
        return {
            TreeState.FINE: "#00AA00",
            TreeState.BURNING: "#880000",
            TreeState.BURNED_DOWN: "#000000",
        }[self]


class Tree(Agent):
    state: TreeState
    model: "ForestFire"

    def __init__(self, unique_id: int, model: "ForestFire"):
        super().__init__(unique_id=unique_id, model=model)
        self.state = TreeState.FINE

    def step(self) -> None:
        if self.state != TreeState.BURNING:
            return

        for pos in self._custom_neighborhood_plus_wind():
            if self.model.grid.out_of_bounds(pos) or pos == self.pos:
                continue

            if neighbor := self.model.grid[pos]:
                if neighbor.state == TreeState.FINE:
                    neighbor.state = TreeState.BURNING

        self.state = TreeState.BURNED_DOWN

    def _custom_neighborhood_plus_wind(self) -> Iterator[Position]:
        base_x_shift = [-1, 0, 1]
        base_y_shift = [-1, 0, 1]
        x_shift = [x + self.model.wind[0] for x in base_x_shift]
        y_shift = [y + self.model.wind[1] for y in base_y_shift]

        for x, y in product(x_shift, y_shift):
            yield self.pos[0] + x, self.pos[1] + y


class ForestFire(Model):
    grid: SingleGrid
    wind: Wind

    def __init__(self, size: int, p: float, wind_x: int = 0, wind_y: int = 0):
        super().__init__()
        self.grid = SingleGrid(width=size, height=size, torus=False)
        self.wind = wind_x, wind_y
        self._init_trees(p)
        self.datacollector = DataCollector(model_reporters=model_reporters)
        self.running = True

    @classmethod
    def batch_run(
        cls,
        size: int | Iterator[int] = 100,
        wind_x: int = 0,
        wind_y: int = 0,
        iterations: int = 1000,
    ) -> DataFrame:
        return DataFrame(
            data=batch_run(
                model_cls=cls,
                parameters=dict(
                    size=size,
                    p=np.arange(start=0, stop=1, step=0.01),
                    wind_x=wind_x,
                    wind_y=wind_y,
                ),
                iterations=iterations,
                number_processes=None,
            )
        )

    def step(self) -> None:
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
        self.running = self._is_burning

    def _init_trees(self, p: float):
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < p:
                tree = Tree(unique_id=self.next_id(), model=self)

                if x == 0:
                    tree.state = TreeState.BURNING

                self.grid.place_agent(tree, (x, y))

    @property
    def _is_burning(self) -> bool:
        return any([tree.state == TreeState.BURNING for tree in self.agents])


def opposite_edge_hit(model: ForestFire) -> bool:
    return any(tree.state != TreeState.FINE for tree in model.agents if tree.pos[0] == model.grid.width - 1)


def biggest_burned_cluster(model: ForestFire) -> int:
    burned_down = np.zeros((model.grid.width, model.grid.height), dtype=np.integer)
    for tree in model.agents:
        if tree.state == TreeState.BURNED_DOWN:
            burned_down[tree.pos[0], tree.pos[1]] = 1

    labels, num = measurements.label(burned_down)
    cluster_sizes = measurements.sum(burned_down, labels, index=range(num + 1))
    return int(max(cluster_sizes))


model_reporters = {
    "opposite_edge_hit": opposite_edge_hit,
    "biggest_burned_cluster": biggest_burned_cluster,
}