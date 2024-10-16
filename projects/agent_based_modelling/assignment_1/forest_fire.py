from itertools import product
from random import random
from typing import Iterator

import numpy as np
from scipy.ndimage import measurements

from projects.agent_based_modelling.lib import Agent, Grid, Model, Pos
from projects.agent_based_modelling.assignment_1.hoshen_kopelman import HoshenKopelman

Wind = tuple[int, int]

FINE = "green"
BURNING = "red"
BURNED_DOWN = "black"


class Tree(Agent):
    state: str
    model: "ForestFire"

    def __init__(self, model: "ForestFire"):
        super().__init__(model=model)
        self.state = FINE

    def step(self) -> None:
        if self.state != BURNING:
            return

        for pos in self._custom_neighborhood_plus_wind():
            if self.model.grid.out_of_bounds(pos) or pos == self.pos:
                continue

            if neighbor := self.model.grid.get(pos):
                if neighbor.state == FINE:
                    neighbor.state = BURNING

        self.state = BURNED_DOWN

    def _custom_neighborhood_plus_wind(self) -> Iterator[Pos]:
        base_x_shift = [-1, 0, 1]
        base_y_shift = [-1, 0, 1]
        x_shift = [x + self.model.wind[0] for x in base_x_shift]
        y_shift = [y + self.model.wind[1] for y in base_y_shift]

        for x, y in product(x_shift, y_shift):
            yield Pos(self.pos.x + x, self.pos.y + y)


class ForestFire(Model):
    wind: Wind

    def __init__(self, size: int, p: float, wind_x: int = 0, wind_y: int = 0):
        super().__init__(
            grid=Grid(width=size, height=size),
            data_collectors={
                "opposite_edge_hit": opposite_edge_hit,
                "biggest_burned_cluster": biggest_burned_cluster,
            },
        )
        self.wind = wind_x, wind_y
        self._init_trees(p)

    def step(self) -> None:
        fires = [tree for tree in self.agents if tree.state == BURNING]
        for fire in fires:
            fire.step()

        self.running = self._is_burning

    def _init_trees(self, p: float):
        for pos in self.grid.coord_iter():
            if random() < p:
                tree = Tree(model=self)

                if pos.x == 0:
                    tree.state = BURNING

                self.grid.set(pos, tree)

    @property
    def _is_burning(self) -> bool:
        return any([tree.state == BURNING for tree in self.agents])


def opposite_edge_hit(model: ForestFire) -> bool:
    return any(tree.state != FINE for tree in model.agents if tree.pos[0] == model.grid.width - 1)


def biggest_burned_cluster(model: ForestFire) -> int:
    return HoshenKopelman(grid=model.grid).biggest_cluster_size()
