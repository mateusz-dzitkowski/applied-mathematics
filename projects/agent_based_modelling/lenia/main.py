import time

import numpy as np

from kernel import Kernel
from lenia import Lenia
from mapping import Map, Mapping, Growth
from base import bell
from world import World


def main():
    world = World(arr=np.zeros((3, 200, 200))).embed(World.load("aquarium"), at=(100, 100))
    lenia = Lenia.aquarium(initial=world)
    # lenia.show()
    lenia.animate(steps=1000)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Done! It took only {end-start} seconds")
