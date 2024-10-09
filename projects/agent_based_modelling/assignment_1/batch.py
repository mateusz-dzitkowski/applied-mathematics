from matplotlib import pyplot as plt

from projects.agent_based_modelling.assignment_1.forest_fire import ForestFire


def run_and_plot(
    width: int,
    height: int,
    wind_x: int,
    wind_y: int,
    iterations: int,
):
    (
        ForestFire.batch_run(
            width=width,
            height=height,
            wind_x=wind_x,
            wind_y=wind_y,
            iterations=iterations,
        )[["p", "opposite_edge_hit"]]
        .groupby("p")
        .mean()
        .plot()
    )
    plt.show()


if __name__ == "__main__":
    run_and_plot(
        width=100,
        height=100,
        wind_x=0,
        wind_y=0,
        iterations=100,
    )
