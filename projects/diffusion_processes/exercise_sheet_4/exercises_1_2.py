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
    phi = rng.choice([0, 0.5, 1, 1.5], size=(steps - 1, walks)) * np.pi
    return (
        np.concatenate([np.zeros(1 if walks == 1 else (1, walks)), np.cumsum(np.round(np.cos(phi)), axis=axis)]),
        np.concatenate([np.zeros(1 if walks == 1 else (1, walks)), np.cumsum(np.round(np.sin(phi)), axis=axis)]),
    )


def pearson_walk(steps: int, walks: int = 1) -> RandomWalk:
    axis = 0 if walks > 1 else None
    phi = rng.uniform(high=2 * np.pi, size=(steps - 1, walks))
    return (
        np.concatenate([np.zeros(1 if walks == 1 else (1, walks)), np.cumsum(np.cos(phi), axis=axis)]),
        np.concatenate([np.zeros(1 if walks == 1 else (1, walks)), np.cumsum(np.sin(phi), axis=axis)]),
    )


def animate(walk_generator: RandomWalkGenerator, steps: int, filename: str):
    x, y = walk_generator(steps)
    animate_random_walk(x, y, filename)


def plot_trajectory(walk_generator: RandomWalkGenerator, steps: int):
    plot_random_walk(*walk_generator(steps))


def plot_hist(walk_generator: RandomWalkGenerator, steps: int, walks: int):
    plot_histograms(*walk_generator(steps, walks))


def main():
    walk_gen = pearson_walk

    # plot_trajectory(walk_gen, 1000)
    animate(walk_gen, 100_000)
    # plot_hist(walk_gen, 1_000, 10_000)


if __name__ == "__main__":
    main()
