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
        self.world.arr = np.clip(self.world.arr + self.dt * self.mapping.apply(self.world).arr, 0, 1)
        print(self.world.arr.sum())

    def show(self):
        self.world.show()
        self.mapping.show()

    def animate(self, *, steps: int = 50, filename: str = "test.gif", fps: int = 50):
        fig, ax = plt.subplots(figsize=(8, 8), constrained_layout=True)
        ax.set_aspect("equal")

        img = ax.imshow(np.dstack(self.world.arr))

        def update(_: int):
            self.step()
            img.set_data(np.dstack(self.world.arr))

        def init():
            img.set_data(np.dstack(self.world.arr))

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

    @classmethod
    def aquarium(cls, initial: World) -> Self:
        common_bell = bell(0.5, 0.15)
        common_r = 12 * 0.9
        common_r_cells = initial.arr.shape[1] // 2

        def growth(_m, _s, _h):
            def inner(x):
                return _h*(bell(_m, _s)(x) * 2 - 1)
            return inner

        return cls(
            world=initial,
            dt=0.5,
            mapping=Mapping(
                maps=[
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.91,
                            peaks=[1],
                            from_chan=0,
                            to_chan=0,
                        ),
                        growth=Growth(func=growth(0.272, 0.0595, 0.138)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.62,
                            peaks=[1],
                            from_chan=0,
                            to_chan=0,
                        ),
                        growth=Growth(func=growth(0.349, 0.1585, 0.48)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.5,
                            peaks=[1, 1/4],
                            from_chan=0,
                            to_chan=0,
                        ),
                        growth=Growth(func=growth(0.2, 0.0332, 0.284)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.97,
                            peaks=[0, 1],
                            from_chan=1,
                            to_chan=1,
                        ),
                        growth=Growth(func=growth(0.114, 0.0528, 0.256)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.72,
                            peaks=[1],
                            from_chan=1,
                            to_chan=1,
                        ),
                        growth=Growth(func=growth(0.447, 0.0777, 0.5)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.622,
                            peaks=[5/6, 1],
                            from_chan=1,
                            to_chan=1,
                        ),
                        growth=Growth(func=growth(0.247, 0.0342, 0.622)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.96,
                            peaks=[1],
                            from_chan=2,
                            to_chan=2,
                        ),
                        growth=Growth(func=growth(0.21, 0.0617, 0.35)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.56,
                            peaks=[1],
                            from_chan=2,
                            to_chan=2,
                        ),
                        growth=Growth(func=growth(0.462, 0.1192, 0.218)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.78,
                            peaks=[1],
                            from_chan=2,
                            to_chan=2,
                        ),
                        growth=Growth(func=growth(0.446, 0.1793, 0.556)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.79,
                            peaks=[11/12, 1],
                            from_chan=0,
                            to_chan=1,
                        ),
                        growth=Growth(func=growth(0.327, 0.1408, 0.344)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.5,
                            peaks=[3/4, 1],
                            from_chan=0,
                            to_chan=2,
                        ),
                        growth=Growth(func=growth(0.476, 0.0995, 0.456)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.72,
                            peaks=[11/12, 1],
                            from_chan=1,
                            to_chan=0,
                        ),
                        growth=Growth(func=growth(0.379, 0.0697, 0.67)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.68,
                            peaks=[1],
                            from_chan=1,
                            to_chan=2,
                        ),
                        growth=Growth(func=growth(0.262, 0.0877, 0.42)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.43,
                            peaks=[1/6, 1, 0],
                            from_chan=2,
                            to_chan=0,
                        ),
                        growth=Growth(func=growth(0.412, 0.1101, 0.43)),
                    ),
                    Map(
                        kernel=Kernel.from_func(
                            func=common_bell,
                            radius_cells=common_r_cells,
                            radius_xy=common_r * 0.82,
                            peaks=[1],
                            from_chan=2,
                            to_chan=1,
                        ),
                        growth=Growth(func=growth(0.201, 0.0786, 0.278)),
                    ),
                ],
            ),
        )
