import time

import numpy as np

from base import Array
from kernel import Kernel
from lenia import Lenia
from mapping import Map, Mapping, Growth
from base import bell
from world import World


def main():
    aquarium = World.load("aquarium").zoomed(2)
    world = (
        World(arr=np.zeros((3, 500, 500)))
        .embed(aquarium, at=(10, 10))
        .embed(aquarium.rotated.rotated, at=(30, 60))
        .embed(aquarium.flipped_horizontal, at=(300, 60))
        .embed(aquarium, at=(200, 450))
        .embed(aquarium.rotated, at=(300, 450))
        .embed(aquarium.rotated, at=(250, 250))
    )
    lenia = Lenia.aquarium(initial=world, common_r=30)
    lenia.show(_from=200, _to=300)
    # lenia.animate(steps=1500)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Done! It took only {end-start} seconds")
