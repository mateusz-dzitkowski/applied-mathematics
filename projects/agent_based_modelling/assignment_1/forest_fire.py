from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Callable

from mesa import Agent, Model, DataCollector
from mesa.space import SingleGrid


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


Wind = tuple[int, int]


class Tree(Agent):
    state: TreeState

    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id=unique_id, model=model)
        self.state = TreeState.FINE

    def step(self) -> None:
        if self.state == TreeState.BURNING:
            grid: SingleGrid = self.model.grid  # type: ignore
            # TODO: wind
            for neighbor in grid.iter_neighbors(self.pos, moore=True):
                if neighbor.state == TreeState.FINE:
                    neighbor.state = TreeState.BURNING

            self.state = TreeState.BURNED_DOWN


class ForestFire(Model):
    grid: SingleGrid
    wind: Wind

    def __init__(self, width: int, height: int, p: float, wind_x: int, wind_y: int):
        super().__init__()
        self.grid = SingleGrid(width=width, height=height, torus=False)
        self.wind = wind_x, wind_y
        self._init_trees(p)

        self.datacollector = DataCollector({
            TreeState.FINE: state_counter(TreeState.FINE),
            TreeState.BURNING: state_counter(TreeState.BURNING),
            TreeState.BURNED_DOWN: state_counter(TreeState.BURNED_DOWN),
        })
        self.running = True

    def _init_trees(self, p: float):
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < p:
                tree = Tree(unique_id=self.next_id(), model=self)

                if x == 0:
                    tree.state = TreeState.BURNING

                self.grid.place_agent(tree, (x, y))

    def step(self) -> None:
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
        if state_counter(TreeState.BURNING)(self) == 0:
            self.running = False


def state_counter(state: TreeState) -> Callable[[Model], int]:
    def inner(model: Model):
        return len([tree for tree in model.agents if tree.state == state])

    return inner
