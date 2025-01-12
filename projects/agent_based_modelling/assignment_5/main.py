from typing import Iterable
import networkx as nx
from matplotlib import pyplot as plt

from projects.agent_based_modelling.assignment_5.automaton import Automaton, StartPosition
from projects.agent_based_modelling.assignment_5.rule import Rule, CUSTOM_STEP_FUNCTIONS

SIZE = 100
RUN_LENGTH = 100
COLUMNS = 4


def plot_rules(rules: Iterable[int] = CUSTOM_STEP_FUNCTIONS):
    for rule_number in rules:
        print(rule_number)
        rule = Rule(number=rule_number)
        fig, ((evolution_dot, evolution_rand), (time_series_dot, time_series_rand)) = plt.subplots(2, 2, figsize=(15, 15), layout="tight")

        dot = Automaton(
            rule=rule,
            size=SIZE,
            run_length=RUN_LENGTH,
            start_position=StartPosition.DOT,
        )
        dot.plot_evolution(evolution_dot)
        dot.plot_timeseries(time_series_dot)
        evolution_dot.set_title(f"Rule {rule_number} starting dot")
        time_series_dot.set_title(f"Time series of rule {rule_number} starting dot")

        rand = Automaton(
            rule=rule,
            size=SIZE,
            run_length=RUN_LENGTH,
            start_position=StartPosition.RANDOM,
        )
        rand.plot_evolution(evolution_rand)
        rand.plot_timeseries(time_series_rand)
        evolution_rand.set_title(f"Rule {rule_number} starting random")
        time_series_rand.set_title(f"Time series of rule {rule_number} starting random")

        fig.savefig(f"plots/rule_{rule_number:03}.png")
        plt.close(fig)


def plot_graphs(rules: Iterable[int] = CUSTOM_STEP_FUNCTIONS):
    for rule_number in rules:
        print(rule_number)
        g = Rule(number=rule_number).configuration_space_diagram
        pos = nx.spring_layout(g, k=0.5)

        fig, ax = plt.subplots(layout="tight")
        ax.set_title(f"Configuration space diagram of rule {rule_number}")
        nx.draw_networkx(
            g,
            pos=pos,
            ax=ax,
            with_labels=True,
            arrows=True,
            font_weight="normal",
            node_color="skyblue",
        )
        fig.savefig(f"graphs/rule_{rule_number:03}.png")
        plt.close(fig)


if __name__ == "__main__":
    plot_rules()
    plot_graphs()
