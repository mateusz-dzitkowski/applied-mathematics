import numpy as np

from projects.agent_based_modelling.lenia.animate import animate_lenia
from projects.agent_based_modelling.lenia.lenia import Lenia, World


def main():
    size = 100
    initial = np.zeros((size, size))
    initial[size // 2, size // 2] = 1
    initial[size // 2 + 1, size // 2] = 1
    initial[size // 2 - 1, size // 2] = 1
    initial[size // 2, size // 2 - 1] = 1
    initial[size // 2 + 1, size // 2 + 1] = 1

    gol = Lenia.game_of_life(initial=World(initial))
    animate_lenia(gol, 300, "gol.gif")


if __name__ == "__main__":
    main()
