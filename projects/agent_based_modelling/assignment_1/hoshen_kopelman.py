from collections import Counter
from itertools import product
from typing import Protocol

import numpy as np

from projects.agent_based_modelling.lib import Grid, Pos


class _Tree(Protocol):
    state: str


class HoshenKopelman:
    def __init__(self, grid: Grid[_Tree]):
        self.grid: Grid = grid
        self.labels: np.ndarray = np.zeros((grid.width, grid.height), dtype=int)
        self.next_label = 1
        self.label_map: dict[int, int] = {}

    def biggest_cluster_size(self) -> int:
        for i, j in product(range(self.grid.width), range(self.grid.height)):
            if self._occupied(Pos(i, j)):
                neighbors: list[int] = []

                if i > 0 and self.labels[i - 1, j] > 0:
                    neighbors.append(int(self.labels[i - 1, j]))
                if j > 0 and self.labels[i, j - 1] > 0:
                    neighbors.append(int(self.labels[i, j - 1]))
                if i > 0 and j > 0 and self.labels[i - 1, j - 1] > 0:
                    neighbors.append(int(self.labels[i - 1, j - 1]))
                if i > 0 and j < self.grid.height - 1 and self.labels[i - 1, j + 1] > 0:
                    neighbors.append(int(self.labels[i - 1, j + 1]))

                if not neighbors:
                    self.labels[i, j] = self.next_label
                    self.label_map[self.next_label] = self.next_label
                    self.next_label += 1
                else:
                    min_label = min(neighbors)
                    self.labels[i, j] = min_label
                    for label in neighbors:
                        self._union(label, min_label)

        for i, j in product(range(self.grid.width), range(self.grid.height)):
            if self.labels[i, j] > 0:
                self.labels[i, j] = self._find(int(self.labels[i, j]))

        no_zeros = self.labels.flatten()[self.labels.flatten() != 0].tolist()
        if no_zeros:
            return Counter(no_zeros).most_common()[0][1]
        return 0

    def _find(self, x: int) -> int:
        root = x
        while self.label_map[root] != root:
            root = self.label_map[root]
        while x != root:
            parent = self.label_map[x]
            self.label_map[x] = root
            x = parent
        return root

    def _union(self, x: int, y: int):
        root_x = self._find(x)
        root_y = self._find(y)
        if root_x != root_y:
            self.label_map[root_y] = root_x

    def _occupied(self, pos: Pos) -> bool:
        if tree := self.grid.get(pos):
            if tree.state == "black":
                return True
        return False
