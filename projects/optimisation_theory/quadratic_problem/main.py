from matplotlib import pyplot as plt

from projects.optimisation_theory.quadratic_problem.problem import Problem


def main():
    problem = Problem.main_problem()

    fig, ax = plt.subplots(figsize=(10, 10))
    problem.plot_solution(ax)
    ax.set_title("$x_i^j$")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
