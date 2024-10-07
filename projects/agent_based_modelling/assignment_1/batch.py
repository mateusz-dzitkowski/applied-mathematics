import numpy as np
from matplotlib import pyplot as plt
from mesa.batchrunner import batch_run
from pandas import DataFrame

from projects.agent_based_modelling.assignment_1.forest_fire import (
    ForestFire,
    TreeState,
)

if __name__ == "__main__":
    results = batch_run(
        model_cls=ForestFire,
        parameters={
            "width": 100,
            "height": 100,
            "p": np.arange(start=0, stop=1, step=0.01),
        },
        iterations=10,
        number_processes=None,
    )

    df = DataFrame(data=results)
    df[["p", TreeState.FINE, TreeState.BURNED_DOWN]].groupby("p").mean().plot()
    plt.show()
