from typing import Protocol

from nptyping import NDArray
import numpy as np

from plots import (
    animate_random_walk,
    plot_random_walk,
    plot_histograms,
)


rng = np.random.default_rng()


RandomWalk = tuple[NDArray, NDArray]


class RandomWalkGenerator(Protocol):
    def __call__(self, steps: int, walks: int = ..., /) -> RandomWalk: ...


def square_lattice_walk(steps: int, walks: int = 1) -> RandomWalk:
    axis = 0 if walks > 1 else None
    phi = rng.choice([0, 0.5, 1, 1.5], size=(steps, walks)) * np.pi
    return (
        np.cumsum(np.round(np.cos(phi)), axis=axis),
        np.cumsum(np.round(np.sin(phi)), axis=axis),
    )


def pearson_walk(steps: int, walks: int = 1) -> RandomWalk:
    axis = 0 if walks > 1 else None
    phi = rng.uniform(high=2 * np.pi, size=(steps, walks))
    return (
        np.cumsum(np.cos(phi), axis=axis),
        np.cumsum(np.sin(phi), axis=axis),
    )


def animate(walk_generator: RandomWalkGenerator, n: int):
    animate_random_walk(*walk_generator(n))


def plot_trajectory(walk_generator: RandomWalkGenerator, steps: int):
    plot_random_walk(*walk_generator(steps))


def plot_hist(walk_generator: RandomWalkGenerator, steps: int, walks: int):
    plot_histograms(*walk_generator(steps, walks))


def main():
    walk_gen = pearson_walk

    # plot_trajectory(walk_gen, 10_000)
    animate(walk_gen, 10_000)
    # plot_hist(walk_gen, 1000, 10000)


if __name__ == "__main__":
    main()
