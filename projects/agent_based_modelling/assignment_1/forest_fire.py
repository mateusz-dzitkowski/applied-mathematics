from enum import StrEnum, auto
from itertools import product
from typing import Any, Iterator

from mesa import Agent, DataCollector, Model
from mesa.space import Position, SingleGrid
from mesa.batchrunner import batch_run
from numpy import arange
from pandas import DataFrame


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

    def __init__(self, width: int, height: int, p: float, wind_x: int = 0, wind_y: int = 0):
        super().__init__()
        self.grid = SingleGrid(width=width, height=height, torus=False)
        self.wind = wind_x, wind_y
        self._init_trees(p)

        self.datacollector = DataCollector(
            {
                "opposite_edge_hit": opposite_edge_hit,
            }
        )
        self.running = True

    @classmethod
    def batch_run(
        cls,
        width: int,
        height: int,
        wind_x: int,
        wind_y: int,
        iterations: int,
    ) -> DataFrame:
        return DataFrame(
            data=batch_run(
                model_cls=cls,
                parameters=dict(
                    width=width,
                    height=height,
                    p=arange(start=0, stop=1, step=0.01),
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
