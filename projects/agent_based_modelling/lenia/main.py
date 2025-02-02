import numpy as np

from kernel import Kernel
from lenia import Lenia
from mapping import Map, Mapping, Growth
from base import bell
from world import World


def main():
    aquarium = World.load("aquarium").zoom(0.9)
    world = World.new((3, 64, 64))
    world.embed(aquarium, at=(20, 20))

    lenia = Lenia.aquarium(initial=world)
    lenia.show()
    lenia.animate(steps=10)


if __name__ == "__main__":
    main()
