import numpy as np

from projects.agent_based_modelling.lenia.lenia import World, Lenia, Kernel, GrowthMapping, bell
from projects.agent_based_modelling.lenia.animate import animate_lenia


def main():
    world = World.new(100, 100)
    world.arr = np.random.uniform(size=(100, 100))

    lenia = Lenia(
        world=world,
        kernel=Kernel.from_func(
            func=bell(0.5, 0.15),
            radius_cells=50,
            radius_xy=13,
        ),
        growth_mapping=GrowthMapping(func=lambda x: 2*bell(0.15, 0.015)(x) - 1),
        dt=0.1,
    )
    animate_lenia(lenia, 300, "random.gif")


if __name__ == "__main__":
    main()
