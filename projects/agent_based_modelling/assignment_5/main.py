from projects.agent_based_modelling.assignment_5.rule import Rule
from projects.agent_based_modelling.assignment_5.automaton import Automaton, StartPosition
from matplotlib import pyplot as plt


SIZE = 200
RUN_LENGTH = 200
GRID_SIDE_LENGTH = 16


def plot_all_rules(start_position: StartPosition):
    fig, axes = plt.subplots(GRID_SIDE_LENGTH, GRID_SIDE_LENGTH, figsize=(SIZE, RUN_LENGTH))
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            automaton = Automaton(
                rule=Rule(number=GRID_SIDE_LENGTH*i + j),
                size=SIZE,
                run_length=RUN_LENGTH,
                start_position=start_position,
            )
            automaton.run()
            automaton.plot(ax)

    fig.savefig("test.png")


if __name__ == "__main__":
    plot_all_rules(StartPosition.RANDOM)
