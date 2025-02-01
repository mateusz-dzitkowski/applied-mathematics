import numpy as np

from kernel import Kernel
from lenia import Lenia
from mapping import Map, Mapping, Growth
from base import bell
from world import World
from animate import animate_lenia


def fish():
    size = 200

    world = World.new(size, size)
    fish = World.load("organisms/fish.npy")

    for f, at in [
        (fish.flipped_vertical, (20, 20)),
        (fish.flipped_horizontal.flipped_vertical, (40, 50)),
        (fish.flipped_horizontal.rotated, (70, 130)),
        (fish.rotated, (20, 167)),
        (fish.flipped_vertical, (150, 160)),
    ]:
        world.embed(f, at=at)

    lenia = Lenia(
        world=world,
        mapping=Mapping(
            maps=[
                Map(
                    kernel=Kernel.from_func(
                        func=lambda x: bell(0.2, 0.05)(x) + 0.4 * bell(0.5, 0.05)(x) + 0.5 * bell(1, 0.05)(x),
                        radius_cells=size // 2,
                        radius_xy=10,
                    ),
                    growth=Growth(func=lambda x: 2 * bell(0.156, 0.0118)(x) - 1),
                ),
                Map(
                    kernel=Kernel.from_func(
                        func=lambda x: 1 / 12 * bell(0.4, 0.5)(x) + 0.8 * bell(0.8, 0.08)(x),
                        radius_cells=size // 2,
                        radius_xy=10,
                    ),
                    growth=Growth(func=lambda x: 2 * bell(0.183, 0.049)(x) - 1),
                ),
                Map(
                    kernel=Kernel.from_func(
                        func=bell(0.5, 0.15),
                        radius_cells=size // 2,
                        radius_xy=10,
                    ),
                    growth=Growth(func=lambda x: 2 * bell(0.342, 0.0891)(x) - 1),
                ),
            ],
        ),
        dt=0.2,
    )
    lenia.mapping.show()
    animate_lenia(lenia, 1500, "test.gif", fps=50)


def game_of_life():
    init = World(np.random.randint(0, 2, (101, 101)))
    gol = Lenia.game_of_life(initial=init)
    gol.mapping.show()
    animate_lenia(gol, 200, "test.gif", fps=50)


def main():
    game_of_life()


if __name__ == "__main__":
    main()
