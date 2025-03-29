from dataclasses import dataclass
from functools import cached_property
from typing import Self

import numpy as np
from base import Array, Func
from scipy.signal import convolve2d


@dataclass
class Kernel:
    arr: Array
    from_chan: int = 0
    to_chan: int = 0

    @classmethod
    def from_func(
        cls,
        func: Func,
        radius_cells: int,
        radius_xy: float,
        midpoint: bool = False,
        peaks: Array | list[float] | None = None,
        from_chan: int = 0,
        to_chan: int = 0,
    ) -> Self:
        if peaks is None:
            peaks = [1]
        peaks = np.asarray(peaks)

        if midpoint:
            x, y = np.meshgrid(*np.ogrid[-radius_cells : radius_cells + 1, -radius_cells : radius_cells + 1])
        else:
            x, y = np.meshgrid(*np.ogrid[-radius_cells:radius_cells, -radius_cells:radius_cells])
        x, y = x / radius_xy * len(peaks), y / radius_xy * len(peaks)
        r = np.sqrt(x**2 + y**2)
        return cls(
            arr=(r < len(peaks)) * peaks[np.minimum(r.astype(int), len(peaks) - 1)] * func(r % 1),
            from_chan=from_chan,
            to_chan=to_chan,
        )

    @cached_property
    def fft(self) -> Array:
        return np.fft.fft2(np.fft.fftshift(self.arr / self.arr.sum()))

    def apply(self, arr: Array, use_fft: bool = True) -> Array:
        if use_fft:
            return np.real(np.fft.ifft2(self.fft * arr))
        else:
            return convolve2d(arr, self.arr, mode="same", boundary="wrap")
