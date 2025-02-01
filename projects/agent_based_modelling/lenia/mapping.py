from dataclasses import dataclass

from matplotlib import pyplot as plt
import numpy as np

from base import Func, Array
from kernel import Kernel


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

    def apply(self, arr: Array) -> Array:
        convolved = [_map.kernel.apply(arr) for _map in self.maps]
        growth = np.asarray([_map.growth.apply(conv) for conv, _map in zip(convolved, self.maps)])
        return growth.mean(axis=0)

    def show(self):
        fig, (ax1, ax2, ax3) = plt.subplots(
            nrows=1,
            ncols=3,
            figsize=(14, 3),
            constrained_layout=True,
            gridspec_kw={"width_ratios": [1, 2, 2]},
        )
        arrays = np.asarray([_map.kernel.arr for _map in self.maps])

        ax1.imshow(np.dstack(arrays), cmap="viridis", interpolation="nearest", vmin=0)
        ax1.set_title("kernel matrix")

        ax2.plot(arrays[:, arrays.shape[1] // 2, :].T)
        ax2.set_title("kernel cross section")

        x = np.linspace(0, 1, 1000)
        g = np.asarray([_map.growth.apply(x) for _map in self.maps]).T
        ax3.plot(x, g)
        ax3.axhline(y=0, color="grey", linestyle="dotted")
        ax3.set_title("growth mapping")

        plt.show()