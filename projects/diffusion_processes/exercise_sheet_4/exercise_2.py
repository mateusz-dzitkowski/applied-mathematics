from nptyping import NDArray
import numpy as np

from projects.diffusion_processes.exercise_sheet_4.exercise_1 import animate_random_walk


def generate_random_walk(n: int) -> tuple[NDArray, NDArray]:
    phi = np.random.uniform(size=n) * 2 * np.pi
    return np.cumsum(np.cos(phi)), np.cumsum(np.sin(phi))


def main():
    x, y = generate_random_walk(100)
    animate_random_walk(x, y)


if __name__ == "__main__":
    main()
