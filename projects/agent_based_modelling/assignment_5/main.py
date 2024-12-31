from projects.agent_based_modelling.assignment_5.rule import Rule, RULES
from projects.agent_based_modelling.assignment_5.automaton import Automaton, StartPosition
from matplotlib import pyplot as plt


SIZE = 100
RUN_LENGTH = 100
COLUMNS = 4


def plot():
    fig, axes = plt.subplots(RULES, COLUMNS, figsize=(COLUMNS * SIZE, RULES * RUN_LENGTH))
    for i, (evolution_dot, evolution_random, timeseries_dot, timeseries_random) in enumerate(axes):
        print(i)
        dot = Automaton(
            rule=Rule(number=i),
            size=SIZE,
            run_length=RUN_LENGTH,
            start_position=StartPosition.DOT,
        )
        dot.plot_evolution(evolution_dot)
        dot.plot_timeseries(timeseries_dot)

        random = Automaton(
            rule=Rule(number=i),
            size=SIZE,
            run_length=RUN_LENGTH,
            start_position=StartPosition.RANDOM,
        )
        random.plot_evolution(evolution_random)
        random.plot_timeseries(timeseries_random)

    fig.savefig("test.png")


if __name__ == "__main__":
    plot()
