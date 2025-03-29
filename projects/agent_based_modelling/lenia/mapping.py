from dataclasses import dataclass

import numpy as np
from base import Array, Func
from kernel import Kernel
from matplotlib import pyplot as plt
from world import World


class Growth:
    func: Func

    def __init__(self, func: Func):
        self.func = func

    def apply(self, arr: Array) -> Array:
        return self.func(arr)


@dataclass
class Map:
    kernel: Kernel
    growth: Growth


@dataclass
class Mapping:
    maps: list[Map]
    use_fft: bool = True

    def apply(self, world: World) -> World:
        arr = np.fft.fft2(world.arr) if self.use_fft else world.arr
        convolved = [_map.kernel.apply(arr[_map.kernel.from_chan], use_fft=self.use_fft) for _map in self.maps]
        growth = [_map.growth.apply(conv) for conv, _map in zip(convolved, self.maps)]
        h = [sum(g for g, _map in zip(growth, self.maps) if _map.kernel.to_chan == chan) for chan in range(len(arr))]
        return World(arr=np.array(h))

    def show(self, _from: int, _to: int):
        fig, (ax1, ax2, ax3) = plt.subplots(
            nrows=1,
            ncols=3,
            figsize=(14, 3),
            constrained_layout=True,
            gridspec_kw={"width_ratios": [1, 2, 2]},
        )
        arrays = np.asarray([_map.kernel.arr for _map in self.maps])

        ax1.imshow(np.dstack(arrays[:3, _from:_to, _from:_to]), cmap="viridis", interpolation="nearest", vmin=0)
        ax1.set_title("kernel matrix")

        ax2.plot(arrays[:, arrays.shape[1] // 2, _from:_to].T)
        ax2.set_title("kernel cross section")

        x = np.linspace(0, 1, 1000)
        g = np.asarray([_map.growth.apply(x) for _map in self.maps]).T
        ax3.plot(x, g)
        ax3.axhline(y=0, color="grey", linestyle="dotted")
        ax3.set_title("growth mapping")

        plt.show()
