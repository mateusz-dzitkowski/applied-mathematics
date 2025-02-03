import time

import numpy as np

from base import Array
from kernel import Kernel
from lenia import Lenia
from mapping import Map, Mapping, Growth
from base import bell
from world import World


def main():
    def bcs(arr: Array):
        arr[:, :5, :] = 0
        arr[:, -5:, :] = 0
        arr[:, :, :5] = 0
        arr[:, :, -5:] = 0
        arr[1, 40:60, 40:60] = 0

    aquarium = World.load("aquarium")
    world = (
        World(arr=np.zeros((3, 100, 100)))
        .embed(aquarium, at=(10, 10))
        .embed(aquarium.rotated.rotated, at=(70, 70))
    )
    lenia = Lenia.aquarium(initial=world)
    lenia.bcs = bcs
    # lenia.show()
    lenia.animate(steps=1000)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Done! It took only {end-start} seconds")
