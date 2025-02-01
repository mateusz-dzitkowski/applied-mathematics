from dataclasses import dataclass
from typing import Self

from matplotlib import animation
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm

from base import h, bell
from world import World
from mapping import Mapping, Map, Growth
from kernel import Kernel


@dataclass
class Lenia:
    world: World
    mapping: Mapping
    dt: float

    def step(self):
        self.world.arr[:, :] = np.clip(self.world.arr + self.dt * self.mapping.apply(self.world.arr), 0, 1)

    def show(self):
        self.world.show()
        self.mapping.show()

    def animate(self, *, steps: int = 50, filename: str = "test.gif", fps: int = 50):
        fig, ax = plt.subplots(figsize=(8, 8), constrained_layout=True)
        ax.set_aspect("equal")

        img = ax.imshow(self.world.arr)

        def update(_: int):
            self.step()
            img.set_data(self.world.arr)

        def init():
            img.set_data(self.world.arr)

        animation.FuncAnimation(
            fig=fig,
            func=update,  # type: ignore
            init_func=init,  # type: ignore
            frames=tqdm(range(steps)),
            cache_frame_data=False,
        ).save(
            filename=filename,
            writer=animation.PillowWriter(fps=fps),
        )
        plt.close()

    @classmethod
    def game_of_life(cls, initial: World) -> Self:
        return cls(
            world=initial,
            mapping=Mapping(
                maps=[
                    Map(
                        kernel=Kernel.from_func(
                            func=lambda x: x > 0,
                            radius_cells=1,
                            radius_xy=2,
                            midpoint=True,
                        ),
                        growth=Growth(lambda x: h(x - 1) + h(x - 2) - 2 * h(x - 3) - 1),
                    ),
                ],
            ),
            dt=1,
        )

    @classmethod
    def geminium(cls, initial: World) -> Self:
        return cls(
            world=initial,
            dt=0.1,
            mapping=Mapping(
                maps=[
                    Map(
                        kernel=Kernel.from_func(
                            func=bell(0.5, 0.15),
                            radius_cells=initial.arr.shape[0] // 2,
                            radius_xy=18,
                            peaks=[0.5, 1, 0.667],
                        ),
                        growth=Growth(func=lambda x: bell(0.26, 0.036)(x)*2 - 1),
                    ),
                ],
            ),
        )

    @classmethod
    def fish(cls, initial: World) -> Self:
        return cls(
            world=initial,
            dt=0.2,
            mapping=Mapping(
                maps=[
                    Map(
                        kernel=Kernel.from_func(
                            func=bell(0.5, 0.15),
                            radius_cells=initial.arr.shape[0] // 2,
                            radius_xy=10,
                            peaks=[1, 5/12, 2/3],
                        ),
                        growth=Growth(func=lambda x: bell(0.156, 0.0118)(x) * 2 - 1),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=bell(0.5, 0.15),
                            radius_cells=initial.arr.shape[0] // 2,
                            radius_xy=10,
                            peaks=[1/12, 1],
                        ),
                        growth=Growth(func=lambda x: bell(0.193, 0.049)(x) * 2 - 1),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=bell(0.5, 0.15),
                            radius_cells=initial.arr.shape[0] // 2,
                            radius_xy=10,
                        ),
                        growth=Growth(func=lambda x: bell(0.342, 0.0891)(x) * 2 - 1),
                    ),
                ],
            ),
        )
