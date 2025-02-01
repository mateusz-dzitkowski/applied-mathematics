import numpy as np

from kernel import Kernel
from lenia import Lenia
from mapping import Map, Mapping, Growth
from base import bell
from world import World


def main():
    fish = World.load("fish")
    world = World.new(100, 100)
    world.embed(fish.flipped_vertical, at=(10, 10))
    world.embed(fish.rotated, at=(70, 70))

    lenia = Lenia.fish(initial=world)
    lenia.show()
    lenia.animate(steps=500)


if __name__ == "__main__":
    main()
