from types import SimpleNamespace

import numpy as np
from hypothesis import given, settings, strategies
from hypothesis.extra.numpy import array_shapes, arrays
from scipy.ndimage import measurements

from projects.agent_based_modelling.assignment_1.forest_fire import BURNED_DOWN, Pos
from projects.agent_based_modelling.assignment_1.hoshen_kopelman import Grid, HoshenKopelman

TREE = SimpleNamespace(state=BURNED_DOWN)


def expected(arr: np.ndarray):  # assume that this algorithm is correct
    labels, num = measurements.label(arr, structure=[[1] * 3] * 3)
    cluster_sizes = measurements.sum(arr, labels, index=range(num + 1))
    return int(max(cluster_sizes))


@given(
    arrays(
        dtype=int,
        shape=array_shapes(min_dims=2, max_dims=2),
        elements=strategies.integers(0, 1),
    ),
)
@settings(max_examples=20_000)
def test_hoshen_kopelman(grid_items):
    grid = Grid(*grid_items.shape)
    for i, row in enumerate(grid_items):
        for j, item in enumerate(row):
            if item == 1:
                grid.set(Pos(i, j), TREE)
    assert HoshenKopelman(grid).biggest_cluster_size() == expected(grid_items)
