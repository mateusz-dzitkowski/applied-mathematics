import time

import numpy as np

from base import Array
from kernel import Kernel
from lenia import Lenia
from mapping import Map, Mapping, Growth
from base import bell, bcs_wall
from world import World


def main():
    aquarium = World.load("aquarium").zoomed(9)
    world = (
        World.empty((3, 1000, 1000))
        .embed(aquarium, at=(400, 400))
    )

    lenia = Lenia.aquarium(initial=world, common_r=100)
    lenia.bcs = bcs_wall(20)
    # lenia.show()
    lenia.animate(steps=1000)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Done! It took only {end-start} seconds")
