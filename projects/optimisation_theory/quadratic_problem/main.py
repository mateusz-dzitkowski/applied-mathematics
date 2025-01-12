from matplotlib import pyplot as plt

from projects.optimisation_theory.quadratic_problem.problem import Problem, Plant


def main():
    problem = Problem(
        beets_per_day=800,
        num_days=20,
        plants=[
            Plant(
                capacity=220,
                coefficient=0.00006,
            ),
            Plant(
                capacity=160,
                coefficient=0.00002,
            ),
            Plant(
                capacity=180,
                coefficient=0.00003,
            ),
        ],
    )

    fig, ax = plt.subplots(figsize=(10, 10))
    problem.plot_solution(ax)
    ax.set_title("$x_i^j$")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
