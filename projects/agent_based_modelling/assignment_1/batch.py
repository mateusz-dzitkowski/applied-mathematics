import os
from mesa.batchrunner import batch_run
import numpy as np

from projects.agent_based_modelling.assignment_1.forest_fire import Tree, ForestFire, TreeState


if __name__ == "__main__":
    for item in batch_run(
        model_cls=ForestFire,
        parameters={
            "width": 100,
            "height": 100,
            "p": np.arange(start=0, stop=1, step=0.1),
        },
        iterations=2,
        number_processes=None,
    ):
        print(item)
